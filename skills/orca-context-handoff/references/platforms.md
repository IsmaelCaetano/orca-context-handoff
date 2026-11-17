# Adaptadores e instalação local

Compatibilidade de instruções não significa telemetria ou automação idêntica. Inspecionar versão instalada e ajuda local antes de integrar comandos. Esta versão contém protocolo e templates; não instala hooks nem controlador de sessões.

## Instalar no projeto

Copiar a pasta completa desta skill para os caminhos abaixo no projeto de destino. Usar cópia idêntica para Claude; atualizar as duas cópias juntas quando necessário. Não substituir diretórios ou configurações existentes sem inspeção. Para instalação pessoal, consultar documentação da versão instalada.

| Ambiente | Caminho no projeto | Invocação |
| --- | --- | --- |
| Codex CLI/IDE | `.agents/skills/orca-context-handoff/SKILL.md` | `$orca-context-handoff` |
| Claude Code local | `.claude/skills/orca-context-handoff/SKILL.md` | `/orca-context-handoff` |
| Antigravity | `.agents/skills/orca-context-handoff/SKILL.md` | Pedido explícito; slash se suportado na versão |

Codex e Antigravity podem compartilhar a mesma pasta de skill, mas cada sessão deve escrever seu próprio checkpoint. Para ativação contínua orientada pelo modelo, acrescentar às instruções já existentes do projeto uma referência curta ao protocolo, sem substituir seu conteúdo. Uma regra persistente é um lembrete, não um medidor ou bloqueio de ferramentas.

## Codex

No CLI, `/compact` compacta a conversa; `/new` inicia chat novo. Confirmar disponibilidade em `/help`. Em IDE/app, usar nova conversa no mesmo projeto quando a interface não oferecer esses comandos. Fornecer RESUME.md como primeira mensagem. Não usar resume da conversa antiga quando o objetivo é contexto limpo.

Não presumir hooks iguais aos do Claude. Automação futura requer um adaptador que leia telemetria corrente e lance uma sessão nova por interface suportada. Não tentar ler contadores internos inexistentes ou configurar hooks Claude para Codex.

## Claude Code

Usar `/context` ou telemetria documentada da versão para observar ocupação. `/compact` resume; `/clear` limpa a conversa. Salvar e validar checkpoint antes de limpar; fornecer o prompt de retomada em seguida. Verificar comandos na versão instalada.

Para controlador por hooks, consultar a referência oficial de eventos e schemas. Mesclar configurações existentes; verificar semântica de UserPromptSubmit, PreToolUse, PostToolUse, PreCompact e Stop separadamente. Não presumir que um formato de resposta bloqueia todos os eventos. Não bloquear as ferramentas necessárias para escrever o checkpoint. Um hook não escreve um resumo sem acesso ao estado e um mecanismo para solicitar a escrita ao agente.

## Antigravity

Confirmar se é App, IDE ou CLI e a versão. `.agents/skills` é o caminho atual documentado; `.agent/skills` é legado em versões que o suportam. Criar conversa nova pelo mecanismo disponível e apontar para o checkpoint no mesmo workspace. Não presumir que comandos Claude ou Codex funcionam aqui. Sem API de telemetria/lifecycle confirmada, manter troca manual assistida.

## Orca e abertura automática — próxima camada

Validar `orca --help` e o subcomando de criação de terminal na máquina real. O repositório de inspiração sugere `orca terminal create`, mas esta skill não validou a instalação do usuário. Compor comandos com argumentos separados em vez de concatenar prompt/caminho no shell. Não copiar flags de bypass de permissões. A nova sessão deve respeitar as permissões do usuário.

Antes de habilitar abertura automática, testar em projeto descartável: abaixo dos limiares, limites cruzados, telemetria ausente, checkpoint sem gravação, processo ativo/desconhecido, caminho Windows com espaços, abertura falhando e evento Stop repetido. Exigir checkpoint válido, lock de escritor e abertura única por session-id. Para confirmação de destino, usar timeout e estado de falha, sem relançamento infinito. Erro do monitor deve gerar diagnóstico local curto sem segredos; não impedir salvar o trabalho.

## Fontes verificadas em 17/11/2026

- Inspiração analisada: https://github.com/Jhonatan-de-Souza/KillTheContext/blob/main/README.md — prompt Claude/Orca, sem implementação pronta. Não copiar código não licenciado; este protocolo foi escrito independentemente.
- Codex skills: https://learn.chatgpt.com/docs/build-skills
- Codex comandos: https://developers.openai.com/codex/cli/slash-commands
- Claude skills: https://code.claude.com/docs/en/skills
- Claude hooks: https://code.claude.com/docs/en/hooks
- Claude contexto: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- Antigravity skills: https://antigravity.google/docs/skills

Rever documentação e ajuda local ao implementar adaptadores; comandos e caminhos podem mudar.
