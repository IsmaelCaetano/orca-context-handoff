# Continuidade entre plataformas

## Distinguir o sinal

| Sinal observado | Tratamento |
|---|---|
| Cota/limite da assinatura, créditos esgotados ou limite diário explícito | Marcar pool afetado como quota_exhausted e tentar próxima plataforma elegível |
| 429 ou rate limit sem escopo explícito | Não concluir que acabou a cota; respeitar Retry-After, fazer no máximo uma nova tentativa controlada, então usar alternativa como contingência transitória |
| Contexto cheio, compactação ou limite de saída | Fazer handoff/compactação na mesma plataforma; isso não renova cota |
| 401, 403, credencial expirada, política de acesso | Registrar problema de acesso; não trocar contas nem credenciais automaticamente; continuar apenas por alternativa já autorizada com permissões equivalentes |
| Timeout/5xx | Conferir processos/efeitos pendentes; uma tentativa controlada se segura, depois outra plataforma elegível |
| Teste ou compilação falhou | Diagnosticar implementação; não atribuir automaticamente a cota |

Pool = provedor + conta autorizada + produto + agrupamento de limite efetivamente observado. Na dúvida, registrar escopo desconhecido; não presumir que outro modelo, API ou CLI renova saldo. Gemini CLI e Antigravity podem ter pools distintos ou compartilhados: verificar, nunca deduzir pelo nome.

## Preparar antes da falha

1. Confirmar inventário e alternativas de cada papel sem chamadas caras de benchmark. Modelo listado na API é somente candidato até confirmado no host.
2. Manter checkpoint após cada entrega/etapa e antes de operação externa. Registrar logs já produzidos, branch, worktree, arquivos alterados e processos ativos. Não manter segredos no checkpoint.
3. Separar estado durável do contexto da conversa. Se houver orca-context-handoff, reutilizar STATUS/RESUME e referenciar os caminhos reais; não manter cópias conflitantes. Sem essa skill, usar o template deste pacote.
4. Declarar o modo observado: automatic_validated somente com controlador já existente testado no host; assisted quando depender de usuário/maestro vivo para abrir a nova sessão. Não instalar daemon nem remover proteções só para obter automação.

## Transferir uma tarefa

1. Capturar o sinal real, horário e escopo de cota sem expor credenciais ou logs sensíveis. Marcar somente a tarefa/pool afetados; não parar especialistas independentes saudáveis.
2. Suspender novas ações desse escritor. Conferir terminal/processo e ações em andamento. Processo sem saída pode continuar executando: confirmar parada ou isolamento/revogação do direito de escrita antes da retomada. Se não for possível, bloquear aquela tarefa para evitar dois escritores.
3. Recuperar o último checkpoint e reconciliar com arquivos, diff, status e logs REAIS. Se o agente morreu antes de salvar, usar checkpoint anterior e estado observado. Não pedir uma resposta final a um agente já bloqueado por cota.
4. Para efeito externo de resultado incerto (envio, deploy, pagamento, commit/push remoto), consultar identificador/estado no destino antes de repetir. Sem reconciliação, deixar essa ação bloqueada e continuar só tarefas independentes seguras. Timeout não prova falha.
5. Excluir modelo proibido, pool esgotado, candidato sem ferramentas necessárias, custo novo ou acesso não confirmado. Escolher próxima plataforma na rota do papel. Não diminuir qualidade de revisão crítica nem aceitar só nome de modelo como capacidade comprovada.
6. Aplicar no máximo uma abertura por candidato; no máximo três tentativas de candidatos por incidente. Registrar erro e seguir para outro pool. Não circular A→B→A nem gastar tentando modelos do mesmo pool esgotado. Respeitar Retry-After sem consultas repetidas.
7. Gerar evento com origem/destino, motivo, modelos/esforços efetivos, pool, tarefa, checkpoint, processos, efeito externo pendente e estado de escrita. Confirmar leitura do checkpoint e validação do estado pelo sucessor antes de continuar.
8. Retomar do próximo passo real, sem repetir etapas concluídas. Ferramentas, permissões e segredos não migram automaticamente: usar integrações previamente autorizadas no destino. Compartilhar só contexto necessário entre as plataformas autorizadas, nunca .env, credenciais ou dumps de clientes.

## Se o maestro ficar sem cota

Preferência normal: Opus 5.5/medium. Contingência: Codex GPT-6.1 Sol/medium → Gemini 4 Carbon (padrão do executor) → Gemini 4 Neon (padrão), somente entre disponíveis e adequados. Se o pool Gemini Carbon estiver esgotado, não tentar Neon do mesmo pool; se for apenas modelo indisponível, Neon pode ser candidato.

O sucessor assume a coordenação TEMPORÁRIA, com checkpoint, tarefa, critérios e registro de autoridade. A regra anterior de nunca trocar o maestro por cota fica substituída por esta política. A preferência Opus não muda. Também transferir a fase de integração se o maestro original não puder executá-la.

Se o host não tiver supervisor independente de LLM, ninguém garante abrir o sucessor depois que o maestro bloqueia. Preparar RESUME e comando de retomada antecipadamente; o usuário pode colá-lo em sessão já aberta na outra plataforma. Informar essa limitação antes de iniciar projeto longo.

## Recuperar e retornar

Marcar pool em cooldown até reset informado ou, sem ele, até verificação manual/intervalo configurável (padrão local: 15 minutos; não é limite oficial). Registrar horário absoluto e fuso. Reexaminar somente no próximo ponto seguro; esta skill não agenda verificações sozinha. Não alternar a cada chamada. Confirmar que o serviço voltou antes de devolver a coordenação; transferir a autoridade com o mesmo protocolo de escritor único.

Se todas as plataformas elegíveis acabarem, salvar estado, informar bloqueio e reset apenas quando observado. Não contratar API, comprar créditos, trocar conta ou contornar limite automaticamente.

## Fontes e limites

- Google cota por método de autenticação: https://geminicli.com/docs/resources/quota-and-pricing/
- Google modelo da sessão não impõe modelo de subagentes: https://geminicli.com/docs/cli/model/

Este protocolo é instrução operacional, não implementação de um supervisor. Teste de mesa prova coerência da política; somente teste no host prova troca real.


## Controlador por contexto (3.0, todos os agentes)

Para contexto corrente, usar orca-context-handoff/scripts/handoff.py com política global 400k checkpoint / 450k preparação / alvo 500k handoff / teto 600k, antecipada em janelas menores. Essa regra vale para maestro e todos os workers/subagentes, sem exceção por provedor.

Antes de iniciar trabalho longo, configurar e testar a supervisão em terminal separado. Registrar cada escritor pelo terminal real e vincular sua telemetria; incluir gate e o protocolo release/accept no despacho. No Claude, usar adaptador statusline/PreToolUse; Codex usa rollout; Antigravity/outros exigem adaptador normalizado real. A existência da skill não prova registro nem publicação de tokens.

O controlador abre o sucessor e fecha a origem somente após ACK e validação. Ele preserva a configuração de agente registrada; a rota por cota continua sob responsabilidade do maestro. Não prometer failover por cota com esse controlador de contexto. Consultar a referência automatico.md da instalação de orca-context-handoff quando ela estiver disponível; não presumir dependência instalada.
