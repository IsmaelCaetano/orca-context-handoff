#!/usr/bin/env python3
"""ORCA handoff controller. Python 3.10+, standard library only.

One daemon in a dedicated terminal; cooperative source/destination handshake.
No shell commands supplied by a model are executed by the controller.
"""
from __future__ import annotations
import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import time
import uuid

VERSION = '3.0.0'
STATES = {'RUNNING', 'CHECKPOINT_REQUESTED', 'HANDOFF_REQUESTED', 'SOURCE_READY',
          'LAUNCHING', 'WAIT_ACK', 'ACKED', 'CLOSING', 'CLOSED', 'FAILED', 'WAIT_RELEASE'}


def now():
    return time.time()


def utc():
    return datetime.now(timezone.utc).isoformat()


def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with tmp.open('w', encoding='utf-8', newline='\n') as f:
            f.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def integer(x, minimum=0):
    if isinstance(x, bool) or not isinstance(x, int) or x < minimum:
        raise ValueError('Expected integer >= ' + str(minimum))
    return x


def thresholds(capacity, reserve=15000):
    c = integer(capacity, 1)
    r = max(integer(reserve, 1), math.ceil(.1 * c))
    handoff = max(0, min(500000, int(.85*c), c-r, 600000-r))
    prepare = min(450000, int(.75*c), handoff)
    checkpoint = min(400000, int(.6*c), prepare)
    return {'checkpoint': checkpoint, 'prepare': prepare, 'handoff': handoff, 'ceiling': min(c, 600000)}


def command(args, cwd, timeout=20):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=timeout, shell=False)
    if p.returncode:
        # Raw terminal/tool output can contain credentials; never copy it into audit logs.
        raise RuntimeError('Command failed (exit %d)' % p.returncode)
    return p.stdout


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.directory = self.root / '.orca' / 'handoff'
        self.directory.mkdir(parents=True, exist_ok=True)
        self.config_path = self.directory / 'config.json'

    @contextmanager
    def lock(self):
        path = self.directory / 'controller.lock'
        with path.open('a+b') as f:
            if os.name == 'nt':
                import msvcrt
                if path.stat().st_size == 0:
                    f.write(b'0'); f.flush()
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl
                fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield
            finally:
                if os.name == 'nt':
                    f.seek(0); msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(f, fcntl.LOCK_UN)

    def config(self):
        c = json.loads(self.config_path.read_text(encoding='utf-8'))
        if c.get('version') != 1:
            raise ValueError('Unsupported config schema')
        if not c.get('agents'):
            raise ValueError('Configure at least one agent argv before registration')
        for a in c['agents'].values():
            argv = a.get('argv')
            if not isinstance(argv, list) or not argv or not all(isinstance(v, str) for v in argv):
                raise ValueError('Agent argv must be a nonempty string array')
            if sum(v.count('{prompt}') for v in argv) != 1:
                raise ValueError('Agent argv must contain one {prompt}')
            forbidden = ('dangerously-skip-permissions', 'danger-full-access', '--yolo', 'bypasspermissions', 'gpt-6.2', 'gpt6.2', 'gpt-6-2')
            if any(s in v.lower() for v in argv for s in forbidden):
                raise ValueError('Permission bypass flags or prohibited model are not supported')
            cli=Path(argv[0]).name.lower()
            if any(cli.startswith(name) for name in ('claude','codex','gemini')):
                if any(v in ('--resume','--continue','-r','-c','resume') for v in argv[1:]):
                    raise ValueError('Successor must start a fresh conversation')
        return c

    def path(self, sid):
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', sid):
            raise ValueError('Invalid session id')
        return self.directory / 'sessions' / (sid + '.json')

    def get(self, sid):
        s = json.loads(self.path(sid).read_text(encoding='utf-8'))
        if s['state'] not in STATES:
            raise ValueError('Unknown state')
        return s

    def put(self, s):
        s['updated_at'] = now()
        atomic(self.path(s['id']), s)

    def sessions(self):
        return [json.loads(p.read_text(encoding='utf-8'))
                for p in sorted((self.directory/'sessions').glob('*.json'))]

    def event(self, sid, kind, **fields):
        entry = {'at': utc(), 'session': sid, 'event': kind, **fields}
        p = self.directory/'events.jsonl'
        with p.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False)+'\n'); f.flush(); os.fsync(f.fileno())
        index=self.root/'.orca/audit/handoffs/CONTROLLER.md'
        index.parent.mkdir(parents=True,exist_ok=True)
        if not index.exists(): atomic(index,'# Handoffs do controlador\n\n| UTC | Sessão | Evento |\n| --- | --- | --- |\n')
        with index.open('a',encoding='utf-8') as f:
            f.write('| '+entry['at']+' | '+sid+' | '+kind+' |\n')


def workspace_digest(root):
    """Detect changed files/HEAD, including staged and untracked files; never upload them."""
    raw = subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],
                         cwd=root, capture_output=True, check=True, timeout=20).stdout
    h = hashlib.sha256()
    head = subprocess.run(['git','rev-parse','HEAD'], cwd=root, capture_output=True, timeout=10)
    h.update(head.stdout)
    for name in sorted(set(os.fsdecode(v) for v in raw.split(b'\0') if v)):
        if name.startswith(('.context-handoff/', '.orca/handoff/', '.orca/audit/')):
            continue
        path = Path(root)/name
        h.update(name.encode('utf-8', errors='surrogateescape'))
        if path.is_symlink():
            h.update(b'LINK'+os.readlink(path).encode())
        elif path.is_file():
            with path.open('rb') as f:
                for chunk in iter(lambda: f.read(1024*1024), b''):
                    h.update(chunk)
        elif path.is_dir():
            raise ValueError('Submodule/directory requires explicit handoff adapter')
        else:
            h.update(b'MISSING')
    return h.hexdigest()


def checkpoint_files(store, s):
    base = store.root/'.context-handoff'/s['id']
    out = {}
    for name in ('STATUS.md', 'RESUME.md'):
        p = base/name
        if not p.is_file() or p.is_symlink():
            raise ValueError('Missing regular checkpoint file: '+name)
        # Also reject a symlinked parent escaping the workspace.
        if not p.resolve().is_relative_to(store.root):
            raise ValueError('Checkpoint escapes project')
        data = p.read_bytes()
        if not data.strip():
            raise ValueError('Empty checkpoint: '+name)
        out[name] = hashlib.sha256(data).hexdigest()
    return out


class Orca:
    def __init__(self, store):
        self.store = store
        self.binary = store.config().get('orca', 'orca')
        if isinstance(self.binary, str): self.binary = [self.binary]

    def call(self, *args):
        data = json.loads(command([*self.binary, *args, '--json'], self.store.root))
        if data.get('ok') is False or data.get('error'):
            raise RuntimeError('Orca reported an error')
        return data.get('result', data)

    def identity(self, terminal):
        t = self.call('terminal', 'show', '--terminal', terminal)['terminal']
        if Path(t['worktreePath']).resolve() != self.store.root or not t.get('ptyId'):
            raise ValueError('Terminal project/process could not be verified')
        if not t.get('connected'):
            raise ValueError('Terminal disconnected')
        return t['ptyId']

    def send(self, s, prompt):
        if self.identity(s['terminal']) != s['pty_id']:
            raise ValueError('Source terminal process changed')
        result = self.call('terminal','send','--terminal',s['terminal'],'--text',prompt,'--enter')
        if not result.get('send', {}).get('accepted'):
            raise RuntimeError('Prompt was not accepted')

    def create(self, title, shell_command):
        t = self.call('terminal','create','--worktree','path:'+str(self.store.root),
                      '--title',title,'--command',shell_command,'--focus')['terminal']
        return t['handle']

    def close(self, s):
        if self.identity(s['terminal']) != s['pty_id']:
            raise ValueError('Source terminal process changed')
        c = self.call('terminal','close','--terminal',s['terminal'])['close']
        # Closing a terminal can otherwise return successfully without proof of PTY death.
        if c.get('ptyKilled') is not True:
            raise RuntimeError('Orca did not confirm source process termination')


def launch_command(store, sid, argv):
    """Only the Python bootstrap reaches the terminal shell; paths/prompts stay base64."""
    body = ('import os,subprocess;'
            'os.environ["ORCA_HANDOFF_ID"]='+repr(sid)+';'
            'raise SystemExit(subprocess.call('+repr(argv)+',cwd='+repr(str(store.root))+'))')
    encoded = base64.b64encode(body.encode()).decode('ascii')
    # `python` is checked during setup. Quoting a stable expression works in cmd, PS and POSIX.
    return 'python -c "import base64;exec(base64.b64decode(\''+encoded+'\'))"'


def source_prompt(store, s, final=False):
    folder = store.root/'.context-handoff'/s['id']
    helper = Path(__file__).resolve()
    if not final:
        return (f'ORCA checkpoint solicitado ({s["id"]}). Use orca-context-handoff. '
                f'Salve e releia STATUS.md e RESUME.md em {folder}. '
                'Continue somente se o gate do controlador autorizar. Não encerre processos.')
    return (f'ORCA HANDOFF {s["request_id"]}: pare novas alterações de produto. '
            f'Salve e releia STATUS.md e RESUME.md em {folder}, com objetivo, decisões, '
            'arquivos pendentes, evidências e próximo passo exato. '
            'Confira jobs, agentes e processos dependentes deste terminal e efeitos externos. '
            'Aguarde-os ou transfira a supervisão antes de liberar. Não mate processos. '
            f'Quando não houver dependentes nem efeitos incertos, execute python "{helper}" '
            f'--root "{store.root}" release --session {s["id"]} '
            f'--request {s["request_id"]} --no-dependent-processes. '
            'Depois desse comando, não edite nem inicie ferramentas de trabalho; finalize sua resposta. '
            'O controlador abrirá o sucessor e fechará este terminal após a confirmação.')


def destination_prompt(store, s, child):
    folder = store.root/'.context-handoff'/s['id']
    return (f'ORCA retomada {s["request_id"]}. Trabalhe inicialmente somente em leitura. '
            f'Leia {folder/"STATUS.md"} e {folder/"RESUME.md"} e as instruções atuais do projeto. '
            'Confira workspace e próximo passo. Não repita ações externas incertas. '
            f'Execute python "{Path(__file__).resolve()}" --root "{store.root}" '
            f'accept --session {child["id"]} --request {s["request_id"]}. '
            'Esse comando valida hashes e aguarda a confirmação do encerramento da origem. '
            'Só continue editando se ele retornar CONTINUAR (código zero). '
            'Se retornar erro ou PARAR, permaneça sem escrever e informe o bloqueio. '
            'Em cada etapa/antes de mutar, consulte gate desta sessão; ao receber PARAR, '
            'execute o protocolo de handoff. Mantenha checkpoints após entregas. '
            'A cota do plano não é renovada por esta troca.')


def register(store, terminal, agent, native_id=None, telemetry=None):
    c = store.config()
    if agent not in c['agents']:
        raise ValueError('Unknown configured agent')
    if terminal==c.get('controller_terminal'):
        raise ValueError('Controller terminal cannot be registered as worker')
    api = Orca(store)
    pty_id = api.identity(terminal)
    for old in store.sessions():
        if old['terminal'] == terminal and old['state'] not in ('CLOSED','FAILED'):
            raise ValueError('Terminal already registered')
    s = {'id': uuid.uuid4().hex, 'state':'RUNNING','terminal':terminal,
         'pty_id':pty_id,'agent':agent,'native_id':native_id,'generation':0,
         'parent':None,'writer':True,'created_at':now(),'telemetry_file':telemetry}
    store.put(s); store.event(s['id'],'REGISTERED',agent=agent)
    return s


def observe(store, sid, tokens, capacity, source):
    s = store.get(sid)
    integer(tokens); integer(capacity,1)
    s['observation'] = {'tokens':tokens,'capacity':capacity,'source':source,'at':now()}
    store.put(s)


def read_telemetry(store, s):
    if s.get('agent') == 'codex' and not s.get('telemetry_file'):
        discover_codex(store, s)
        s = store.get(s['id'])
    if s.get('telemetry_kind') == 'codex':
        codex_rollout(store, s)
        return
    path = s.get('telemetry_file')
    if not path:
        return
    p = Path(path)
    # Caller binds one explicit JSON observation to one registered session.
    if not p.is_file() or now()-p.stat().st_mtime > 60:
        return
    d = json.loads(p.read_text(encoding='utf-8'))
    if d['session_id'] != s['id']:
        raise ValueError('Telemetry belongs to another session')
    observe(store,s['id'],d['tokens'],d['capacity'],d['source'])


def tick(store, api=None):
    api = api or Orca(store)
    config = store.config()
    for current in store.sessions():
        sid = current['id']
        s = store.get(sid)
        if s['state']=='WAIT_RELEASE' and s.get('parent'):
            parent=store.get(s['parent'])
            if parent['state']=='CLOSED' and parent.get('successor')==sid and s.get('terminal'):
                if api.identity(s['terminal'])==s.get('pty_id'):
                    s.update(state='RUNNING',writer=True);store.put(s)
                    store.event(sid,'TRANSFER_RECOVERED',origin=parent['id'])
            continue
        if s['state'] in ('CLOSED','FAILED','WAIT_RELEASE'):
            continue
        try:
            read_telemetry(store,s); s = store.get(sid)
            if s['state'] in ('LAUNCHING','CLOSING'):
                # A crash after the RPC might already have performed the action.
                raise RuntimeError('Uncertain external action; inspect before manual recovery')
            if s['state'] in ('RUNNING','CHECKPOINT_REQUESTED'):
                o = s.get('observation')
                if not o or now()-o['at'] > 60:
                    continue  # Never infer that missing telemetry means zero or 500k.
                lim = thresholds(o['capacity'], config.get('reserve_tokens',15000))
                s['limits'] = lim
                if o['tokens'] >= lim['prepare']:
                    s.update(state='HANDOFF_REQUESTED',request_id=uuid.uuid4().hex,
                             requested_at=now(),deadline=now()+config.get('handoff_timeout_seconds',300))
                    store.put(s); store.event(sid,'HANDOFF_REQUESTED',tokens=o['tokens'],limits=lim)
                    # Ask early enough to finish the checkpoint by the target (~500k).
                    api.send(s,source_prompt(store,s,True))
                elif o['tokens'] >= lim['checkpoint'] and s['state']=='RUNNING':
                    s['state']='CHECKPOINT_REQUESTED'; store.put(s)
                    store.event(sid,'CHECKPOINT_REQUESTED',tokens=o['tokens'])
                    api.send(s,source_prompt(store,s))
                else:
                    store.put(s)
            elif s['state']=='HANDOFF_REQUESTED':
                if now() > s['deadline']:
                    raise TimeoutError('Source did not release; origin preserved')
            elif s['state']=='SOURCE_READY':
                if checkpoint_files(store,s)!=s['manifest'] or workspace_digest(store.root)!=s['workspace_digest']:
                    raise ValueError('Source checkpoint/workspace changed after release')
                if s['generation'] >= config.get('max_generations',20):
                    raise ValueError('Generation limit reached')
                # A declared process check is cooperative, never pretend it is OS isolation.
                if not s.get('no_dependent_processes'):
                    raise ValueError('Dependent processes are not cleared')
                child = {'id':uuid.uuid4().hex,'state':'WAIT_RELEASE','terminal':'',
                         'agent':s['agent'],'generation':s['generation']+1,'parent':sid,
                         'writer':False,'created_at':now()}
                store.put(child)
                prompt = destination_prompt(store,s,child)
                argv = [v.replace('{prompt}',prompt) for v in config['agents'][s['agent']]['argv']]
                s.update(state='LAUNCHING',successor=child['id']); store.put(s)
                store.event(sid,'LAUNCH_INTENT',successor=child['id'])
                handle = api.create('handoff-'+child['id'][:8],launch_command(store,child['id'],argv))
                if handle == s['terminal']:
                    raise ValueError('Successor must have its own terminal')
                child['terminal']=handle; child['pty_id']=api.identity(handle); store.put(child)
                s.update(state='WAIT_ACK',deadline=now()+config.get('ack_timeout_seconds',180))
                store.put(s); store.event(sid,'SUCCESSOR_OPENED',successor=child['id'],terminal=handle)
            elif s['state']=='WAIT_ACK':
                if now()>s['deadline']:
                    raise TimeoutError('Successor did not acknowledge; origin preserved')
            elif s['state']=='ACKED':
                if checkpoint_files(store,s)!=s['manifest'] or workspace_digest(store.root)!=s['workspace_digest']:
                    raise ValueError('Workspace/checkpoint changed before transfer')
                child=store.get(s['successor'])
                if api.identity(child['terminal'])!=child['pty_id']:
                    raise ValueError('Successor disappeared before transfer')
                s['state']='CLOSING'; store.put(s); store.event(sid,'CLOSE_INTENT')
                api.close(s)
                s.update(state='CLOSED',writer=False); store.put(s)
                child.update(state='RUNNING',writer=True); store.put(child)
                store.event(sid,'TRANSFER_COMPLETE',successor=child['id'])
        except Exception as exc:
            s=store.get(sid); s.update(state='FAILED',writer=False,error=type(exc).__name__)
            store.put(s); store.event(sid,'FAILED',reason=type(exc).__name__)
            # No retries of uncertain launch/close and no automatic reopening of the origin.


def release(store,sid,request,no_dependents):
    s=store.get(sid)
    if s['state']!='HANDOFF_REQUESTED' or s.get('request_id')!=request:
        raise ValueError('No matching active handoff request')
    if not no_dependents:
        raise ValueError('Check dependent processes first')
    base=store.root/'.context-handoff'/sid
    if any((base/name).stat().st_mtime < s['requested_at'] for name in ('STATUS.md','RESUME.md') if (base/name).exists()):
        raise ValueError('Checkpoint predates handoff request; rewrite and reread both files')
    s.update(manifest=checkpoint_files(store,s),workspace_digest=workspace_digest(store.root),
             no_dependent_processes=True,writer=False,state='SOURCE_READY')
    store.put(s); store.event(sid,'SOURCE_RELEASED',request=request)


def acknowledge(store,sid,request):
    child=store.get(sid); s=store.get(child['parent'])
    if s['state']!='WAIT_ACK' or s.get('request_id')!=request or s.get('successor')!=sid:
        raise ValueError('No matching successor request')
    if checkpoint_files(store,s)!=s['manifest'] or workspace_digest(store.root)!=s['workspace_digest']:
        raise ValueError('Checkpoint/workspace mismatch')
    s['state']='ACKED'; store.put(s); store.event(s['id'],'DESTINATION_ACK',successor=sid)


def gate(store,sid):
    s=store.get(sid)
    if not s.get('writer') or s['state'] not in ('RUNNING','CHECKPOINT_REQUESTED'):
        return False
    o=s.get('observation')
    if not o or now()-o['at']>60:
        return False  # Explicit PARAR on stale/missing telemetry.
    lim=thresholds(o['capacity'],store.config().get('reserve_tokens',15000))
    return o['tokens'] < lim['prepare']


def claude_status(store,data):
    w=data.get('workspace',{})
    if Path(w.get('project_dir') or data.get('cwd') or '').resolve()!=store.root:
        raise ValueError('Claude workspace mismatch')
    cw=data.get('context_window',{}); usage=cw.get('current_usage')
    if not usage:  # null before first call/after compaction means unknown.
        session=matching_session(store,data)
        if session:
            session.pop('observation',None); store.put(session)
        return
    fields=('input_tokens','cache_read_input_tokens','cache_creation_input_tokens')
    if not all(k in usage for k in fields):
        return
    tokens=sum(integer(usage[k]) for k in fields)
    native=data.get('session_id'); inherited=os.environ.get('ORCA_HANDOFF_ID')
    candidates=[s for s in store.sessions() if (s.get('native_id')==native and native)
                or (inherited and s['id']==inherited)]
    if len(candidates)!=1:
        return
    s=candidates[0]
    if native and not s.get('native_id'):
        s['native_id']=native; store.put(s)
    observe(store,s['id'],tokens,integer(cw['context_window_size'],1),'claude-statusline')


def matching_session(store, data):
    native=data.get('session_id'); inherited=os.environ.get('ORCA_HANDOFF_ID')
    candidates=[s for s in store.sessions() if (s.get('native_id')==native and native)
                or (inherited and s['id']==inherited)]
    return candidates[0] if len(candidates)==1 else None


def claude_hook(store, data):
    """Defer normal permissions; deny only work that violates a registered handoff."""
    s=matching_session(store,data)
    if not s: return {}
    tool=data.get('tool_name'); inp=data.get('tool_input') or {}
    paused=not gate(store,s['id'])
    if not paused: return {}
    # Read-only native tools never gain extra permission from this hook.
    if tool in ('Read','Glob','Grep','TaskOutput','TaskGet','TaskList'): return {}
    if tool in ('Write','Edit') and s['state'] in ('HANDOFF_REQUESTED','CHECKPOINT_REQUESTED','RUNNING'):
        path=Path(inp.get('file_path','')).resolve()
        base=(store.root/'.context-handoff'/s['id']).resolve()
        if path.is_relative_to(base) and path.name in ('STATUS.md','RESUME.md'):
            return {}
    if tool=='Bash':
        try:
            argv=shlex.split(inp.get('command',''))
            # Exact helper commands only; shell chaining and extra operands cannot pass.
            if (len(argv)>=7 and argv[0] in ('python','python3',sys.executable)
                and Path(argv[1]).resolve()==Path(__file__).resolve()
                and argv[2:4]==['--root',str(store.root)]):
                expected = None
                if argv[4]=='release' and s['state']=='HANDOFF_REQUESTED':
                    expected=['--session',s['id'],'--request',s['request_id'],'--no-dependent-processes']
                elif argv[4]=='accept' and s['state']=='WAIT_RELEASE' and s.get('parent'):
                    parent=store.get(s['parent'])
                    expected=['--session',s['id'],'--request',parent['request_id']]
                elif argv[4]=='gate': expected=['--session',s['id']]
                if expected is not None and argv[5:]==expected: return {}
        except (ValueError,OSError): pass
    return {'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny',
            'permissionDecisionReason':'ORCA PARAR: salvar checkpoint/liberar ou aguardar retomada; consultar controlador.'}}


def install_claude(store):
    settings=store.root/'.claude'/'settings.local.json'
    cfg=json.loads(settings.read_text(encoding='utf-8')) if settings.exists() else {}
    # Do not silently replace an existing user's status bar or hooks.
    if cfg.get('statusLine'):
        raise ValueError('Existing statusLine preserved; compose adapter manually as documented')
    script=str(Path(__file__).resolve())
    def cmd(mode):
        # A quoted -c bootstrap keeps Windows project paths out of the shell parser.
        body='import runpy,sys;sys.argv='+repr([script,'--root',str(store.root),mode])+';runpy.run_path('+repr(script)+',run_name="__main__")'
        b=base64.b64encode(body.encode()).decode()
        return 'python -c "import base64;exec(base64.b64decode(\''+b+'\'))"'
    cfg['statusLine']={'type':'command','command':cmd('claude-status')}
    cfg.setdefault('hooks',{}).setdefault('PreToolUse',[]).append(
        {'matcher':'','hooks':[{'type':'command','command':cmd('claude-hook'),'timeout':15}]})
    if settings.exists():
        atomic(settings.with_name(settings.name+'.backup-'+uuid.uuid4().hex),settings.read_text(encoding='utf-8'))
    atomic(settings,cfg)
    store.event('setup','CLAUDE_ADAPTER_INSTALLED')


def codex_rollout(store, s):
    p=Path(s['telemetry_file'])
    if not p.is_file() or now()-p.stat().st_mtime>60: return
    with p.open('rb') as f:
        first=json.loads(f.readline())
        meta=first.get('payload',{})
        if first.get('type')!='session_meta' or Path(meta.get('cwd','')).resolve()!=store.root:
            raise ValueError('Codex rollout workspace mismatch')
        if s.get('native_id') and meta.get('id')!=s['native_id']:
            raise ValueError('Codex rollout session mismatch')
        # Seek bytes, discard the partial first line BEFORE decoding UTF-8.
        offset=max(0,p.stat().st_size-1024*1024)
        f.seek(offset)
        if offset: f.readline()
        latest=None
        for line in f:
            try: row=json.loads(line)
            except (ValueError,UnicodeError): continue
            payload=row.get('payload',{})
            if row.get('type')=='event_msg' and payload.get('type')=='token_count' and payload.get('info'):
                latest=payload['info']
        if latest:
            # last.total_tokens is active context in upstream TokenUsage; never use accumulated total.
            observe(store,s['id'],integer(latest['last_token_usage']['total_tokens']),
                    integer(latest['model_context_window'],1),'codex-rollout')


def discover_codex(store, s):
    """Match a new rollout to its explicit handoff ID, never pick merely the newest file."""
    if not s.get('parent'): return
    home=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions'
    matches=[]
    # Inspect only recent files; raw transcript contents are never logged or transmitted.
    for p in home.glob('*/*/*/rollout-*.jsonl'):
        if p.stat().st_mtime < s['created_at']-5: continue
        with p.open('r',encoding='utf-8') as f:
            try: first=json.loads(f.readline())
            except ValueError: continue
            if Path(first.get('payload',{}).get('cwd','')).resolve()!=store.root: continue
            start=f.read(256*1024)
            if s['id'] in start and 'ORCA retomada' in start:
                matches.append((p,first['payload']['id']))
    if len(matches)==1:
        p,native=matches[0]
        s.update(telemetry_file=str(p),telemetry_kind='codex',native_id=native);store.put(s)
    elif len(matches)>1:
        raise ValueError('Ambiguous successor rollout')


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',required=True)
    sub=p.add_subparsers(dest='cmd',required=True)
    sub.add_parser('init'); sub.add_parser('status'); sub.add_parser('tick')
    watch=sub.add_parser('watch'); watch.add_argument('--interval',type=float,default=2)
    watch.add_argument('--terminal',required=True,help='Dedicated controller terminal handle')
    reg=sub.add_parser('register'); reg.add_argument('--terminal',required=True); reg.add_argument('--agent',required=True)
    reg.add_argument('--native-session'); reg.add_argument('--telemetry-file')
    obs=sub.add_parser('observe'); obs.add_argument('--session',required=True); obs.add_argument('--tokens',type=int,required=True)
    obs.add_argument('--capacity',type=int,required=True); obs.add_argument('--source',required=True)
    for name in ('release','accept','gate'):
        q=sub.add_parser(name); q.add_argument('--session',required=True)
        if name!='gate': q.add_argument('--request',required=True)
        if name=='release': q.add_argument('--no-dependent-processes',action='store_true')
        if name=='accept': q.add_argument('--timeout',type=float,default=240)
    sub.add_parser('claude-status'); sub.add_parser('claude-hook'); sub.add_parser('install-claude')
    bind=sub.add_parser('bind-codex'); bind.add_argument('--session',required=True); bind.add_argument('--rollout',required=True)
    args=p.parse_args(argv); store=Store(args.root)
    if args.cmd=='init':
        with store.lock():
            if store.config_path.exists(): raise ValueError('Config already exists; preserved')
            atomic(store.config_path,{'version':1,'orca':'orca','reserve_tokens':15000,
                   'max_generations':20,'handoff_timeout_seconds':300,'ack_timeout_seconds':180,
                   'agents':{}})
        ignore=store.root/'.gitignore'
        old=ignore.read_text(encoding='utf-8') if ignore.exists() else ''
        lines=old.splitlines()
        additions=[x for x in ('.context-handoff/','.orca/handoff/','.orca/audit/handoffs/CONTROLLER.md') if x not in lines]
        if additions: atomic(ignore,old+('\n' if old and not old.endswith('\n') else '')+'\n'.join(additions)+'\n')
        print('Created config. Configure agents with explicit validated model argv and verify Orca --help.')
    elif args.cmd=='watch':
        with store.lock():
            c=store.config()
            if any(s['terminal']==args.terminal and s['state']!='CLOSED' for s in store.sessions()):
                raise ValueError('Use a separate terminal for the controller')
            Orca(store).identity(args.terminal)
            c['controller_terminal']=args.terminal; atomic(store.config_path,c)
        if args.interval<.2: raise ValueError('Polling interval must be >= 0.2s')
        while True:
            with store.lock(): tick(store)
            time.sleep(args.interval)
    elif args.cmd=='accept':
        with store.lock(): acknowledge(store,args.session,args.request)
        deadline=now()+args.timeout
        while now()<deadline:
            with store.lock():
                s=store.get(args.session)
                if s['state']=='RUNNING' and s.get('writer'):
                    print('CONTINUAR'); return 0
                if s.get('parent') and store.get(s['parent'])['state']=='FAILED':
                    print('PARAR: source transfer failed'); return 2
            time.sleep(.5)
        print('PARAR: timeout waiting for source closure'); return 2
    else:
        with store.lock():
            if args.cmd=='register':
                print(json.dumps(register(store,args.terminal,args.agent,args.native_session,args.telemetry_file)))
            elif args.cmd=='install-claude': install_claude(store)
            elif args.cmd=='bind-codex':
                s=store.get(args.session); s.update(telemetry_file=str(Path(args.rollout).resolve()),telemetry_kind='codex'); store.put(s); codex_rollout(store,s)
            elif args.cmd=='claude-hook':
                print(json.dumps(claude_hook(store,json.load(sys.stdin))))
            elif args.cmd=='observe': observe(store,args.session,args.tokens,args.capacity,args.source)
            elif args.cmd=='tick': tick(store)
            elif args.cmd=='status': print(json.dumps(store.sessions(),ensure_ascii=False,indent=2))
            elif args.cmd=='release': release(store,args.session,args.request,args.no_dependent_processes); print('PARAR: source released')
            elif args.cmd=='gate':
                ok=gate(store,args.session); print('CONTINUAR' if ok else 'PARAR'); return 0 if ok else 2
            elif args.cmd=='claude-status':
                data=json.load(sys.stdin); claude_status(store,data)
                print('ORCA handoff: '+str((data.get('context_window') or {}).get('used_percentage','?'))+'% contexto')
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (Exception, KeyboardInterrupt) as exc:
        print('handoff: '+type(exc).__name__+'; inspect configuration/audit locally',file=sys.stderr)
        raise SystemExit(2)
