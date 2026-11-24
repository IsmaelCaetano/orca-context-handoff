"""Behavioral tests: real disk and processes; Orca/LLM are simulated, no paid calls."""
import base64
import importlib.util
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SCRIPT=Path(__file__).resolve().parents[1]/'skills/orca-context-handoff/scripts/handoff.py'
spec=importlib.util.spec_from_file_location('handoff',SCRIPT)
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class FakeOrca:
    def __init__(self):
        self.sent=[];self.created=[];self.closed=[];self.fail_create=False;self.fail_close=False
    def identity(self,t): return 'pty-'+t
    def send(self,s,p): self.sent.append((s['id'],p))
    def create(self,title,cmd):
        self.created.append((title,cmd))
        if self.fail_create: raise TimeoutError()
        return 'destination'
    def close(self,s):
        self.closed.append(s['terminal'])
        if self.fail_close: raise RuntimeError()

class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='orca project with spaces ')
        self.root=Path(self.temp.name)
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        (self.root/'app.txt').write_text('unfinished code')
        self.store=h.Store(self.root)
        h.atomic(self.store.config_path,{'version':1,'agents':{'claude':{'argv':['claude','{prompt}']},'codex':{'argv':['codex','{prompt}']},'gemini':{'argv':['gemini','-i','{prompt}']}},'max_generations':20})
        self.api=FakeOrca()
        self.s={'id':'source','state':'RUNNING','terminal':'origin','pty_id':'pty-origin',
                'agent':'claude','generation':0,'parent':None,'writer':True,'created_at':h.now(), 'native_id':'native'}
        self.store.put(self.s)
    def tearDown(self): self.temp.cleanup()
    def request(self,used=460000,capacity=1000000):
        h.observe(self.store,'source',used,capacity,'test');h.tick(self.store,self.api)
        return self.store.get('source')
    def ready(self):
        s=self.request()
        folder=self.root/'.context-handoff'/'source';folder.mkdir(parents=True,exist_ok=True)
        (folder/'STATUS.md').write_text('Goal: finish app; next: tests; pending app.txt')
        (folder/'RESUME.md').write_text('Read STATUS.md and continue tests')
        h.release(self.store,'source',s['request_id'],True)
        return self.store.get('source')
    def opened(self):
        self.ready();h.tick(self.store,self.api);return self.store.get('source')
    def test_global_thresholds_respect_small_windows(self):
        self.assertEqual(h.thresholds(1000000)['handoff'],500000)
        self.assertEqual(h.thresholds(200000)['handoff'],170000)
        self.assertEqual(h.thresholds(1000000)['prepare'],450000)
        self.assertLess(h.thresholds(9000000)['handoff'],600000)
        with self.assertRaises(ValueError):h.thresholds(True)
    def test_no_context_is_not_zero_or_trigger(self):
        h.tick(self.store,self.api);self.assertEqual(self.api.sent,[])
        self.assertFalse(h.gate(self.store,'source'))
    def test_stale_observation_does_not_trigger(self):
        h.observe(self.store,'source',510000,1000000,'test')
        s=self.store.get('source');s['observation']['at']-=120;self.store.put(s)
        h.tick(self.store,self.api);self.assertFalse(self.api.sent)
    def test_checkpoint_then_request_once(self):
        self.request(410000);self.assertEqual(self.store.get('source')['state'],'CHECKPOINT_REQUESTED')
        h.tick(self.store,self.api);self.assertEqual(len(self.api.sent),1)
        self.request(500000);h.tick(self.store,self.api);self.assertEqual(len(self.api.sent),2)
        self.assertFalse(h.gate(self.store,'source'))
    def test_no_launch_without_real_checkpoint(self):
        s=self.request()
        with self.assertRaises(ValueError):h.release(self.store,'source',s['request_id'],True)
        self.assertFalse(self.api.created);self.assertFalse(self.api.closed)
    def test_wrong_request_and_dependents_block(self):
        s=self.request()
        with self.assertRaises(ValueError):h.release(self.store,'source','stale',True)
        with self.assertRaises(ValueError):h.release(self.store,'source',s['request_id'],False)
    def test_open_ack_close_then_transfer(self):
        s=self.opened();child=self.store.get(s['successor'])
        self.assertEqual(s['state'],'WAIT_ACK');self.assertFalse(child['writer']);self.assertFalse(self.api.closed)
        h.acknowledge(self.store,child['id'],s['request_id']);h.tick(self.store,self.api)
        self.assertEqual(self.api.closed,['origin'])
        self.assertEqual(self.store.get('source')['state'],'CLOSED')
        self.assertTrue(self.store.get(child['id'])['writer'])
        h.tick(self.store,self.api);self.assertEqual(len(self.api.created),1)
    def test_launch_timeout_never_relaunches(self):
        self.ready();self.api.fail_create=True;h.tick(self.store,self.api);h.tick(self.store,self.api)
        self.assertEqual(len(self.api.created),1);self.assertFalse(self.api.closed)
        self.assertEqual(self.store.get('source')['state'],'FAILED')
    def test_ack_timeout_preserves_origin(self):
        s=self.opened();s['deadline']=0;self.store.put(s);h.tick(self.store,self.api)
        self.assertFalse(self.api.closed);self.assertFalse(self.store.get(s['successor'])['writer'])
    def test_close_failure_does_not_grant_successor(self):
        s=self.opened();h.acknowledge(self.store,s['successor'],s['request_id'])
        self.api.fail_close=True;h.tick(self.store,self.api)
        self.assertFalse(self.store.get(s['successor'])['writer'])
    def test_workspace_edit_after_release_blocks_launch(self):
        self.ready();(self.root/'app.txt').write_text('late write');h.tick(self.store,self.api)
        self.assertFalse(self.api.created);self.assertFalse(self.api.closed)
    def test_checkpoint_edit_after_open_blocks_ack(self):
        s=self.opened();(self.root/'.context-handoff/source/STATUS.md').write_text('changed')
        with self.assertRaises(ValueError):h.acknowledge(self.store,s['successor'],s['request_id'])
        self.assertFalse(self.api.closed)
    def test_crash_intent_never_duplicates_external_mutation(self):
        s=self.ready();s['state']='LAUNCHING';self.store.put(s)
        h.tick(self.store,self.api);self.assertFalse(self.api.created)
        self.assertEqual(self.store.get('source')['state'],'FAILED')
    def test_claude_current_context_not_accumulated(self):
        payload={'cwd':str(self.root),'session_id':'native','context_window':{
            'context_window_size':1000000,'total_input_tokens':99999999,
            'current_usage':{'input_tokens':20000,'cache_read_input_tokens':400000,'cache_creation_input_tokens':30000}}}
        h.claude_status(self.store,payload)
        self.assertEqual(self.store.get('source')['observation']['tokens'],450000)
        payload['context_window']['current_usage']=None
        h.claude_status(self.store,payload)
        self.assertNotIn('observation',self.store.get('source'))
    def test_codex_current_includes_output_no_cache_double_count(self):
        path=self.root/'rollout.jsonl'
        rows=[{'type':'session_meta','payload':{'cwd':str(self.root),'id':'native'}},
              {'type':'event_msg','payload':{'type':'token_count','info':{
                  'last_token_usage':{'total_tokens':450100,'input_tokens':450000,'cached_input_tokens':400000},
                  'total_token_usage':{'total_tokens':99999999},'model_context_window':1000000}}}]
        path.write_text('\n'.join(json.dumps(x) for x in rows)+'\n{')
        s=self.store.get('source');s['telemetry_file']=str(path);s['telemetry_kind']='codex';self.store.put(s)
        h.codex_rollout(self.store,s)
        self.assertEqual(self.store.get('source')['observation']['tokens'],450100)
    def test_claude_hook_denies_product_write_allows_checkpoint_and_release(self):
        s=self.request()
        data={'session_id':'native','tool_name':'Write','tool_input':{'file_path':str(self.root/'app.txt')}}
        self.assertEqual(h.claude_hook(self.store,data)['hookSpecificOutput']['permissionDecision'],'deny')
        data['tool_input']['file_path']=str(self.root/'.context-handoff/source/STATUS.md')
        self.assertEqual(h.claude_hook(self.store,data),{})
        data.update(tool_name='Bash',tool_input={'command':f'python "{SCRIPT}" --root "{self.root}" release --session source --request {s["request_id"]} --no-dependent-processes'})
        self.assertEqual(h.claude_hook(self.store,data),{})
        data['tool_input']['command']+='; echo unsafe'
        self.assertIn('hookSpecificOutput',h.claude_hook(self.store,data))
    def test_install_preserves_existing_hooks_and_refuses_existing_statusline(self):
        settings=self.root/'.claude/settings.local.json'
        h.atomic(settings,{'hooks':{'Stop':[{'hooks':[]}]},'permissions':{'deny':['Bash(rm *)']}})
        h.install_claude(self.store)
        c=json.loads(settings.read_text());self.assertIn('Stop',c['hooks']);self.assertIn('permissions',c)
        with self.assertRaises(ValueError):h.install_claude(self.store)
    def test_bootstrap_quoting(self):
        args=['python','a file.py', 'hello " & $ ` % ! \\ \n café']
        cmd=h.launch_command(self.store,'safe',args)
        code=shlex.split(cmd)[2]
        encoded=code.split("'")[1]
        body=base64.b64decode(encoded).decode()
        # Decode and execute only while subprocess.call is replaced, no shell interpolation.
        with patch('subprocess.call',return_value=0) as call,patch.dict(os.environ,{},clear=False):
            with self.assertRaises(SystemExit):exec(body,{})
            self.assertEqual(call.call_args.args[0],args)
    def test_real_successor_process_waits_for_close_confirmation(self):
        s=self.opened();child=s['successor'];request=s['request_id']
        proc=subprocess.Popen([sys.executable,str(SCRIPT),'--root',str(self.root),'accept',
                               '--session',child,'--request',request,'--timeout','8'],stdout=subprocess.PIPE,text=True)
        try:
            deadline=time.time()+4
            while time.time()<deadline and self.store.get('source')['state']!='ACKED':time.sleep(.02)
            self.assertEqual(self.store.get('source')['state'],'ACKED')
            self.assertIsNone(proc.poll())
            h.tick(self.store,self.api)
            stdout,_=proc.communicate(timeout=4)
            self.assertEqual(proc.returncode,0);self.assertIn('CONTINUAR',stdout)
            self.assertEqual(self.api.closed,['origin'])
        finally:
            if proc.poll() is None:proc.kill();proc.wait()
    def test_large_unicode_rollout_tail(self):
        path=self.root/'large.jsonl'
        meta={'type':'session_meta','payload':{'cwd':str(self.root),'id':'native'}}
        event={'type':'event_msg','payload':{'type':'token_count','info':{
            'last_token_usage':{'total_tokens':490000},'model_context_window':1000000}}}
        # Ensure the binary tail cut falls inside a UTF-8 multibyte sequence.
        data=(json.dumps(meta)+'\n'+json.dumps({'text':'á'*600000},ensure_ascii=False)+'\n'+json.dumps(event)+'\n').encode()
        while data[len(data)-1024*1024] < 128 or data[len(data)-1024*1024] >= 192:
            data+=b' '
        path.write_bytes(data)
        ss=self.store.get('source');ss['telemetry_file']=str(path)
        h.codex_rollout(self.store,ss)
        self.assertEqual(self.store.get('source')['observation']['tokens'],490000)
    def test_pending_job_can_be_inspected_during_transfer(self):
        self.request()
        for tool in ('TaskOutput','TaskGet','TaskList'):
            self.assertEqual(h.claude_hook(self.store,{'session_id':'native','tool_name':tool,'tool_input':{}}),{})
    def test_launcher_starts_real_worker_and_transfers_automatically(self):
        worker=self.root/'mock_worker.py'
        worker.write_text("import json,os,re,subprocess,sys\nfrom pathlib import Path\n"
            "prompt=sys.argv[1]\n"
            "m=re.search(r'accept --session ([a-f0-9]+) --request ([a-f0-9]+)',prompt)\n"
            "p=subprocess.run([sys.executable,"+repr(str(SCRIPT))+",'--root',os.getcwd(),'accept','--session',m[1],'--request',m[2],'--timeout','8'],capture_output=True,text=True)\n"
            "assert p.returncode==0,p.stdout+p.stderr\n"
            "Path('successor-confirmation.txt').write_text(os.environ['ORCA_HANDOFF_ID']+' CONTINUAR')\n")
        config=json.loads(self.store.config_path.read_text())
        config['agents']['claude']['argv']=[sys.executable,str(worker),'{prompt}']
        h.atomic(self.store.config_path,config)
        processes=[]
        api=self.api
        def actual_create(title,cmd):
            api.created.append((title,cmd))
            processes.append(subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True))
            return 'destination'
        api.create=actual_create
        try:
            s=self.opened()
            deadline=time.time()+5
            while time.time()<deadline and self.store.get('source')['state']!='ACKED':time.sleep(.02)
            self.assertEqual(self.store.get('source')['state'],'ACKED')
            self.assertFalse((self.root/'successor-confirmation.txt').exists())
            h.tick(self.store,api)
            out,err=processes[0].communicate(timeout=5)
            self.assertEqual(processes[0].returncode,0,out+err)
            self.assertEqual(api.closed,['origin'])
            self.assertEqual((self.root/'successor-confirmation.txt').read_text(),s['successor']+' CONTINUAR')
        finally:
            for proc in processes:
                if proc.poll() is None:proc.kill();proc.wait()

    def test_stale_checkpoint_cannot_be_released(self):
        s=self.ready()
        # Start another valid request but retain old files.
        s.update(state='HANDOFF_REQUESTED',request_id='new',requested_at=h.now()+10)
        self.store.put(s)
        with self.assertRaises(ValueError):h.release(self.store,'source','new',True)
    def test_recover_crash_after_source_closed_before_child_grant(self):
        s=self.opened();child=self.store.get(s['successor'])
        s.update(state='CLOSED',writer=False);self.store.put(s)
        self.assertEqual(child['state'],'WAIT_RELEASE')
        h.tick(self.store,self.api)
        self.assertTrue(self.store.get(child['id'])['writer'])
        self.assertEqual(self.api.closed,[])
    def test_invalid_flags_do_not_change_permissions(self):
        config=json.loads(self.store.config_path.read_text())
        config['agents']['claude']['argv']=['claude','--dangerously-skip-permissions','{prompt}']
        h.atomic(self.store.config_path,config)
        with self.assertRaises(ValueError):self.store.config()

if __name__=='__main__':unittest.main()
