# ORCA Context Handoff

Skill em português para salvar o estado de um projeto e continuar em uma conversa nova no Codex, Claude Code ou Antigravity, incluindo projetos abertos no Orca.

**Estado desta versão:** protocolo de continuidade, templates e instruções de instalação. Não contém monitor em segundo plano, hook instalado, bloqueio automático de ferramentas ou controlador que abre e fecha sessões.

## O que faz

- Salva objetivo, decisões, alterações pendentes, verificações e próximo passo.
- Registra processos em execução e ações externas com resultado pendente.
- Prepara STATUS.md e RESUME.md em `.context-handoff/<session-id>/` no projeto de destino.
- Orienta a nova sessão a conferir o estado real antes de continuar.
- Permite trocar entre as três ferramentas quando elas acessam o mesmo workspace e seus arquivos.
- Evita assumir que a troca de conversa concluiu a tarefa ou transferiu código entre máquinas.

## Limites recomendados

| Ocupação da capacidade efetiva | Ação |
| --- | --- |
| 60% | Salvar checkpoint e continuar |
| 75% | Preparar troca; concluir etapa atual |
| 85% | Passar o trabalho para uma sessão nova em um ponto seguro |

São heurísticas ajustáveis, não limites oficiais. A reserva necessária para salvar e gerar saída pode antecipar a troca. A skill não mede tokens por conta própria: usa somente telemetria confiável do ambiente. Sem ela, salva por marcos e registra contexto desconhecido.

Com capacidade efetiva confirmada de 200.000 tokens: 120.000 / 150.000 / 170.000. **Não confundir tokens acumulados faturados com ocupação atual.** Abrir uma conversa nova não renova cotas de assinatura, créditos ou limites por período.

Veja [política completa de limites](skills/orca-context-handoff/references/limits.md).

## Instalar no projeto do Orca

O Orca é o ambiente onde você abre o projeto. Instale a skill nos caminhos lidos pelo agente usado dentro dele; não é uma extensão do Orca.

1. Baixe este repositório por **Code → Download ZIP** e extraia.
2. Localize a pasta `skills/orca-context-handoff`.
3. Copie a pasta completa, com seus arquivos e subpastas, para os destinos abaixo na raiz do projeto em que vai trabalhar.
4. Se o destino já existir, compare as versões antes de substituir.

| Agente | Pasta de destino |
| --- | --- |
| Codex CLI/IDE | `.agents/skills/orca-context-handoff/` |
| Antigravity | `.agents/skills/orca-context-handoff/` |
| Claude Code local | `.claude/skills/orca-context-handoff/` |

Codex e Antigravity podem compartilhar a mesma pasta. Se usar Claude também, mantenha as duas cópias atualizadas juntas. Esta instalação é por projeto; não modifica configurações globais. Versões do host podem ter diferenças; consulte [adaptadores e fontes](skills/orca-context-handoff/references/platforms.md).

## Como usar

No Codex:

```text
$orca-context-handoff Salve o estado deste projeto e prepare uma retomada.
```

No Claude Code:

```text
/orca-context-handoff Salve o estado deste projeto e prepare uma retomada.
```

No Antigravity, peça explicitamente; use o slash da skill se disponível na versão:

```text
Use orca-context-handoff para salvar um checkpoint deste projeto e preparar a próxima sessão.
```

### Ativar o protocolo durante o trabalho

```text
Use orca-context-handoff neste projeto. Leia a skill e suas referências.
Adote checkpoint em 60%, preparação em 75% e transição em 85% da capacidade
real disponível, antecipando se a reserva exigir. Sem telemetria confiável,
salve por etapas concluídas e não invente percentuais.
Acrescente uma referência curta ao protocolo nas instruções existentes do
projeto, preservando o conteúdo atual. Demonstre uma gravação e leitura de
checkpoint. Não instale hooks nem altere permissões como parte deste pedido.
```

A ativação é orientada pelo agente, não um watchdog que monitora cada chamada. Depois de compactação, pode ser necessário voltar a invocar a skill.

### Encerrar a etapa e abrir a próxima sessão

1. Peça para salvar o checkpoint e gerar RESUME.md.
2. Confira a confirmação de gravação e os processos pendentes. Não feche terminais que sustentam trabalho em execução.
3. Pare a escrita da sessão anterior; abra uma conversa nova no mesmo projeto.
4. Envie o conteúdo do RESUME.md gerado. A nova sessão lê STATUS.md e valida arquivos e processos antes de continuar.

Exemplo de primeira mensagem:

```text
Use orca-context-handoff. Leia o STATUS.md no caminho exato indicado no
RESUME.md que estou fornecendo. Confira instruções do projeto, workspace,
alterações e processos. A sessão anterior parou de editar. Continue do
próximo passo registrado sem repetir ações externas de resultado desconhecido.
```

Para trocar de máquina ou worktree, transportar também o código pendente. O checkpoint resume o trabalho; ele não substitui backup, commit ou transferência das alterações.

## Como conferir que funcionou

Em um projeto de teste, peça para salvar um checkpoint. Confirme que foram criados STATUS.md e RESUME.md na pasta específica da sessão. Abra uma conversa nova, envie RESUME.md e confira se o agente identifica corretamente uma alteração pendente e o próximo passo antes de editar. Isso verifica continuidade; não demonstra monitoramento automático de tokens.

## O que falta para automatizar a troca

Um controlador específico por ambiente, validado na versão instalada, precisa obter telemetria, solicitar checkpoint, verificar a gravação, controlar processos, abrir apenas uma sessão nova e transferir o direito de escrita. Um arquivo SKILL.md sozinho não garante essas ações. Não usar flags que removam proteções para facilitar a abertura.

## Arquivos

- [Skill principal](skills/orca-context-handoff/SKILL.md)
- [Limites e exemplos](skills/orca-context-handoff/references/limits.md)
- [Codex, Claude, Antigravity e Orca](skills/orca-context-handoff/references/platforms.md)
- [Modelo de checkpoint](skills/orca-context-handoff/assets/checkpoint.md)

## Origem da ideia

Inspirado no fluxo descrito por [Jhonatan-de-Souza/KillTheContext](https://github.com/Jhonatan-de-Souza/KillTheContext). Esta skill foi escrita independentemente como protocolo portátil. O projeto de inspiração apresenta um prompt para gerar hooks Claude/Orca; este projeto não afirma que esses hooks foram implementados ou testados aqui.
