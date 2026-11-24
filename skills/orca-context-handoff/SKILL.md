---
name: orca-context-handoff
description: Salvar checkpoints verificáveis e executar handoff entre sessões de agentes no Orca com controlador Python, incluindo Codex, Claude Code e hosts com telemetria normalizada.
---

# ORCA Context Handoff 3.0

Preservar trabalho no projeto e transferir a execução para uma conversa nova. Para instalar e ativar a automação, ler [references/automatico.md](references/automatico.md). A automação depende do controlador em execução, de telemetria real e de dois agentes que cumpram o handshake. Não afirmar que está ativa apenas porque SKILL.md está instalado.

## Limites globais

Aplicar a todos os provedores, modelos e papéis, incluindo maestro, workers e subagentes registrados: salvar até 400.000 tokens, preparar/solicitar transição até 450.000 e realizar o handoff por volta de 500.000. Teto da política: 600.000 tokens de contexto corrente. Janelas menores e reserva antecipam os valores; consultar [references/limits.md](references/limits.md). Essa política substitui o perfil exclusivo Claude e os tetos anteriores de 300k/350k/400k.

Não confundir tokens de contexto com consumo acumulado, créditos ou cota de assinatura. Não inventar medição. A habilidade de bloquear ferramentas depende do adaptador; uma saída grande pode cruzar o limiar entre medições.

## Registrar antes de trabalhar

No modo automático, registrar cada sessão escritora com terminal Orca, papel/configuração de agente e vínculo à sua telemetria. Preservar modelo/esforço e permissões configurados no host; não selecionar modelo proibido nem introduzir flags de bypass. Não instalar esta skill na conta ChatGPT quando o destino pedido for o repositório/projeto.

O controlador deve estar num terminal separado que não será fechado com o agente. Se ele não estiver rodando ou o adaptador não produzir telemetria válida, declarar modo assistido. No Claude, instalar statusline e guard PreToolUse usando o helper quando não houver configuração conflitante; em outros hosts, consultar gate antes de mutações e respeitar PARAR.

## Salvar sempre por eventos

Salvar ao começar/retomar, após entrega de agente ou etapa relevante e antes de trocar sessão/provedor/worktree, mesmo sem contador de tokens. Cada escritor deve ter seu próprio session-id. Se já existir protocolo de continuidade no projeto, preservar e reconciliar o conteúdo.

Usar `.context-handoff/<session-id>/STATUS.md` e `RESUME.md`. No modo automático, usar exatamente o ID retornado por register e repetir o request-id recebido no pedido do controlador ao executar release.

Usar [assets/checkpoint.md](assets/checkpoint.md) como estrutura. Registrar:
- Objetivo, decisões e restrições vigentes do usuário.
- Concluído, pendências, tentativas malsucedidas e próximo passo executável.
- Raiz/worktree, branch/HEAD quando disponíveis, arquivos sem commit e verificações com resultado/horário.
- Agentes/jobs/processos em andamento, dependência do terminal e efeitos externos incertos.
- Modelo, sessão, contexto observado ou desconhecido, origem da medição e limites efetivos.

Não incluir credenciais, cookies, .env ou dumps extensos. Não fazer commit, reset, stash, deploy ou envio externo apenas para salvar contexto. O resumo não transporta código não commitado para outro workspace.

Gravar primeiro num temporário, substituir atomicamente quando possível e reler os dois arquivos. Só afirmar que salvou após confirmar o conteúdo no disco. Informar caminho absoluto, horário e session-id. O controlador registra seus eventos em `.orca/handoff/events.jsonl` e `.orca/audit/handoffs/CONTROLLER.md`.

## Executar a transição automática

1. Ao receber HANDOFF, cessar novas alterações de produto e preparar os arquivos do checkpoint. O pedido chega cedo, normalmente em 450k, para completar a troca próximo de 500k.
2. Conferir agentes, processos dependentes do terminal e efeitos externos. Aguardar conclusão ou transferir supervisão de modo comprovável. Não matar processos para atingir o limite. Se houver pendência incerta, informar bloqueio e não liberar.
3. Executar o comando release com request-id correto e --no-dependent-processes apenas após essa conferência. A flag é uma declaração do agente, não prova de inventário do SO.
4. Após release, parar de escrever e finalizar a resposta. O gate da origem permanece PARAR. O controlador valida arquivos/estado, abre uma única sessão sucessora e fornece o prompt de retomada com caminhos exatos.
5. O sucessor lê STATUS.md, RESUME.md e instruções atuais, confirma workspace e pendências, e executa accept. Permanecer sem editar enquanto accept aguarda.
6. O controlador verifica o ACK, checkpoint, estado do projeto e identidade dos terminais; fecha exclusivamente o terminal da origem. Só após confirmar a parada libera o destino. Retomar apenas se accept retornar CONTINUAR com código zero. Reabastecer telemetria da nova sessão; sem ela, gate retorna PARAR.

Nunca repetir uma abertura após timeout de resultado incerto. O controlador fica FAILED e exige reconciliação. Não marcar retomada por sucesso de criação de aba apenas. Verificar status e os eventos reais; não gerar um registro fictício de TRANSFER_COMPLETE.

## Recuperar ou trabalhar em modo assistido

Se não houver adaptador validado, salvar por eventos e entregar RESUME.md para uma conversa nova no mesmo projeto. Na retomada, confirmar origem sem escrita, workspace, alterações e processos antes de continuar. Reconciliar divergências e não repetir efeitos externos de resultado desconhecido.

Após compactação ou interrupção, ler o checkpoint específico da sessão; não escolher o arquivo de outro agente só porque é mais recente. Respeitar decisões atuais do usuário acima do checkpoint. Não prometer que nova conversa renova cotas ou reduz custos sem medição.

Para detalhes por host e fontes, consultar [references/platforms.md](references/platforms.md).
