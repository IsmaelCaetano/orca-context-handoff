# Controlador automático — instalação e operação

## Conteúdo

- Requisitos e alcance
- Configuração inicial
- Telemetria por host
- Registrar sessões e iniciar o vigia
- Transição e auditoria
- Falhas e validação

## Requisitos e alcance

Python 3.10+ disponível como `python`, Git local e Orca CLI. O runtime usa apenas biblioteca padrão. Configurar no MESMO computador/worktree dos agentes. Não depende de LLM ou API paga para vigiar. O workspace precisa ter Git local para validar arquivos, incluindo alterações sem commit. Submódulos/diretórios especiais exigem adaptador e bloqueiam o modo automático atual.

O controlador executa `orca terminal show/send/create/close --json`, com base no código público do Orca. Versões antigas podem divergir: conferir `orca --help`, `orca terminal create --help`, `orca terminal send --help` e `orca terminal close --help` na máquina de instalação. Não usar `agent launch` nem flags que eliminem aprovações.

Modo implementado: terminal interativo no Orca, mesma pasta de trabalho, próximo agente/configuração igual ao da origem, modelo/esforço determinados pela configuração local. O controlador não implementa compra de créditos nem seleção automática de provedor por cota. A skill maestro continua responsável por planejar rotas por cota.

A transição é automática depois da instalação/registro, mas o salvamento é cooperativo: a origem precisa responder ao pedido e liberar o trabalho, e o destino precisa aceitar. O runtime não pode extrair decisões sem acesso à conversa nem garantir encerramento se um agente não responder. Para não perder trabalho, falhas bloqueiam a transferência em vez de matar a origem.

## Configuração inicial

Use a pasta completa da skill instalada no projeto. Nos comandos abaixo, substitua `<PROJETO>` pela raiz absoluta, `<HELPER>` pelo caminho absoluto de `scripts/handoff.py`, `<ID>` pelo ID devolvido pelo helper e os terminais pelos handles reais listados pelo Orca. No PowerShell, mantenha os caminhos entre aspas.

```powershell
python "<HELPER>" --root "<PROJETO>" init
```

Isso cria `.orca/handoff/config.json`, sem substituir um arquivo existente, e acrescenta exclusões dos registros locais ao .gitignore sem remover regras existentes. Preencha `agents` antes de registrar:

```json
{
  "version": 1,
  "orca": "orca",
  "reserve_tokens": 15000,
  "max_generations": 20,
  "handoff_timeout_seconds": 300,
  "ack_timeout_seconds": 180,
  "agents": {
    "claude": {"argv": ["claude", "--model", "MODELO_REAL_VALIDADO", "{prompt}"]},
    "codex": {"argv": ["codex", "--model", "MODELO_REAL_VALIDADO", "{prompt}"]},
    "gemini": {"argv": ["gemini", "--model", "MODELO_REAL_VALIDADO", "--prompt-interactive", "{prompt}"]}
  }
}
```

Use o modelo/esforço e as flags de execução já validados no agente de origem. Os identificadores acima são placeholders para preencher, não modelos existentes. Não usar GPT-6.2 se estiver proibido no projeto. Não incluir `--resume`/`--continue` que reutilizem o contexto antigo. `{prompt}` é substituído pelo controlador em um único argumento. A configuração não contém credenciais. `orca` também aceita um array de argumentos para executáveis wrappers locais.

A abertura usa um bootstrap Python com payload base64, evitando interpolar caminhos/prompt no shell. Base64 não é criptografia: ele transporta apenas comandos locais e caminhos, nunca segredos. Em Windows, confirmar que `python` e as CLIs funcionam no shell padrão do Orca.

## Telemetria por host

### Claude Code

```powershell
python "<HELPER>" --root "<PROJETO>" install-claude
```

Mescla um guard PreToolUse e uma statusLine em `.claude/settings.local.json`, preserva hooks/permissions existentes e cria backup se havia arquivo. Se já houver statusLine, recusa substituí-la. Nesse caso, integrar manualmente a publicação: enviar a MESMA entrada JSON do host ao comando `python "<HELPER>" --root "<PROJETO>" claude-status` e preservar o renderizador anterior; não reinstalar às cegas.

Conferir confiança do workspace, `/hooks` e statusline na sessão real. O guard só afeta sessões registradas. Durante transferência, permite leituras nativas, gravação dos dois checkpoints e comandos exatos de controle; nega novas mutações de produto. Não é isolamento do sistema operacional: tarefas já executando continuam e precisam ser conferidas pela origem antes de release.

O statusline publica contexto real e vincula a sessão nativa. Sucessores criados pelo controlador herdam ORCA_HANDOFF_ID; o statusline os reconhece sem registro manual adicional.

### Codex CLI

Registrar com a session-id nativa e vincular o rollout JSONL exato desta conversa:

```powershell
python "<HELPER>" --root "<PROJETO>" bind-codex --session <ID> --rollout "<ROLLOUT_EXATO.jsonl>"
```

O vigia lê o contexto corrente do rollout; não soma consumo acumulado. Em sucessores, procura o ID de handoff explícito no prompt inicial de arquivos recentes do mesmo projeto. Não escolhe apenas o arquivo mais recente. Ambiguidade bloqueia.

O guard de ferramentas do Claude não se aplica ao Codex: o agente deve cumprir o protocolo de escritor único e consultar gate antes de mutar. Não afirmar bloqueio técnico universal. A sessão sucessora só recebe CONTINUAR após a confirmação de parada da origem.

### Gemini CLI / Antigravity / outros hosts

O controlador aceita qualquer comando de agente configurado e telemetria normalizada. Esta versão NÃO contém leitor nativo de tokens da interface Antigravity ou um medidor Gemini validado. O adaptador local do host precisa produzir um arquivo por sessão:

```json
{"session_id":"ID_RETORNADO_POR_REGISTER","tokens":490000,"capacity":1000000,"source":"NOME_DO_MEDIDOR_REAL"}
```

Registrar com `--telemetry-file "<ARQUIVO.json>"`. Atualizar atomicamente com dados do host; o arquivo não pode ficar velho. Cada sucessor precisa de publicação com seu ID próprio. O launcher exporta ORCA_HANDOFF_ID ao processo sucessor para um hook local identificar esse ID sem intervenção manual. Não reutilizar a medição do pai. Alternativamente um hook do host pode chamar:

```powershell
python "<HELPER>" --root "<PROJETO>" observe --session <ID> --tokens 490000 --capacity 1000000 --source "HOST_REAL"
```

Esses números são somente um exemplo de formato. Não publicar valores inventados para forçar a troca. Sem integração real, esse host permanece assistido e não há transição garantida por tokens. Gemini CLI e interface Antigravity não são intercambiáveis só por usar modelos Gemini.

## Registrar sessões e iniciar o vigia

1. Listar `orca terminal list --json`; identificar terminais dos agentes e abrir um terminal EXCLUSIVO para o controlador.
2. Registrar cada escritor (maestro e cada worker). Não registrar o terminal do controlador como agente:

```powershell
python "<HELPER>" --root "<PROJETO>" register --terminal "<TERMINAL_AGENTE>" --agent claude --native-session "<SESSION_ID_CLAUDE>"
```

Use `--agent codex` com seu ID nativo e depois bind-codex, ou agente/telemetry-file correspondente ao host. Guardar o ID interno retornado por register. Trabalhos já abertos podem ser registrados sem reiniciar. Native session-id é a da conversa real, não um ID aleatório criado pelo instalador.

3. No terminal exclusivo do controlador, executar:

```powershell
python "<HELPER>" --root "<PROJETO>" watch --terminal "<TERMINAL_CONTROLADOR>"
```

Deixar esse processo rodando. Ele não deve ser filho do agente cujo terminal será fechado. Vários watchers são serializados por lock local, mas operar um só evita supervisão confusa.

4. Peça ao agente registrado para salvar o checkpoint inicial e consultar antes de cada mutação:

```powershell
python "<HELPER>" --root "<PROJETO>" gate --session <ID>
```

CONTINUAR/código zero permite seguir sujeito às permissões normais. PARAR/código 2 significa parar trabalho normal; no handoff, apenas salvar/liberar; sem telemetria, corrigir integração. Um hook/guard pode aplicar isso tecnicamente por host. Não interpretar código 2 como tarefa concluída.

## Transição e auditoria

O vigia envia o pedido de checkpoint no primeiro marco. No marco de preparação, envia HANDOFF com request-id e instruções exatas. A origem escreve STATUS.md e RESUME.md, verifica dependentes/efeitos externos e executa release. Só usar `--no-dependent-processes` se de fato não houver dependentes.

Após release, a origem fica sem autoridade de escrita. O controlador calcula hashes e fingerprint do workspace, cria uma nova aba com o agente configurado e prompt de retomada. O destino lê o estado e executa accept, que aguarda. O controlador fecha somente o terminal da origem e exige confirmação `ptyKilled: true` do Orca antes de liberar o destino. Accept retorna CONTINUAR; a nova sessão retoma o próximo passo.

A contagem de gerações impede uma cadeia infinita de lançamentos, padrão 20 por linhagem. Cada sessão tem ID/pasta próprios. O controlador conserva os checkpoints originais e registra transferência fora deles.

```powershell
python "<HELPER>" --root "<PROJETO>" status
```

- `.context-handoff/<ID>/STATUS.md` e RESUME.md: estado escrito pelo agente.
- `.orca/handoff/sessions/<ID>.json`: máquina de estados e hashes.
- `.orca/handoff/events.jsonl`: eventos duráveis com horários e IDs.
- `.orca/audit/handoffs/CONTROLLER.md`: índice legível de eventos.

Não versionar esses registros de execução no repositório público. Eles são locais ao projeto. O fingerprint pode ler arquivos pendentes/credenciais localmente para detectar mudanças, mas só persiste o hash agregado, nunca o conteúdo desses arquivos.

## Falhas e validação

Sem checkpoint, com processos dependentes, ACK ausente, hash divergente ou identidade de terminal alterada, não fechar a origem nem liberar o destino. Em timeout/crash depois de intenção de criação ou fechamento, marcar FAILED, não repetir a ação. Consultar terminais e eventos reais antes de recuperar manualmente. Não apagar lock de processo ativo nem mudar writer para true manualmente sem reconciliação.

O fingerprint é conservador e abrange todo o worktree: outro agente independente alterando arquivos pode bloquear a transferência. Para paralelismo com menos falsos bloqueios, preferir um worktree por escritor e transportar alterações explicitamente na integração. A verificação de dependentes é cooperativa, não prova de OS.

Testes locais desta versão:

```powershell
python -m unittest discover -s tests -v
```

Os testes exercitam filesystem, checkpoints, estados, integração de telemetria, quoting e processo real de accept. As respostas do Orca e a LLM são simuladas. Isso NÃO prova funcionamento na versão do Orca/Windows instalada no usuário. Validar ali com telemetria sintética em projeto descartável, nunca registrando valores sintéticos em sessão real de produção. Só chamar `automatic_validated` após observar SOURCE_RELEASED → SUCCESSOR_OPENED → DESTINATION_ACK → TRANSFER_COMPLETE no host real.

Fontes verificadas: código https://github.com/stablyai/orca/tree/main/src/cli/terminals ; https://code.claude.com/docs/en/statusline ; https://code.claude.com/docs/en/hooks ; https://github.com/openai/codex/blob/main/codex-rs/tui/src/token_usage.rs ; https://geminicli.com/docs/reference/configuration/ .
