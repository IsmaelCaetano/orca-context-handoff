---
name: orca-context-handoff
description: Salvar checkpoints verificáveis e retomar projetos entre Codex, Claude Code e Antigravity quando o usuário pedir troca de sessão, continuidade, controle de contexto ou recuperação após compactação.
---

# ORCA Context Handoff

Preservar estado de trabalho fora da conversa e preparar uma retomada verificável. Aplicar ao projeto atual; não confundir instalação da skill com instalação de hooks ou automação da interface.

## Escolher a operação

- Para configurar no ambiente local ou integrar Orca, ler [references/platforms.md](references/platforms.md).
- Para avaliar limites, ler [references/limits.md](references/limits.md).
- Para salvar ou retomar, usar o protocolo abaixo e [assets/checkpoint.md](assets/checkpoint.md) como estrutura.

## Medir antes de decidir

Identificar host, versão, modelo e raiz/worktree. Usar somente telemetria exposta pelo host para contexto ocupado e capacidade efetiva; registrar origem e instante da medição. A capacidade efetiva pode ser menor que a janela anunciada pelo modelo. Não somar tokens faturados de todas as chamadas, não inferir capacidade pelo plano e não inventar percentual.

Usar os limiares recomendados de 60% para checkpoint, 75% para preparar transição e 85% para concluir a transição em um ponto seguro. São recomendações ajustáveis, não limites oficiais. Reservar espaço para ferramentas, saída e gravação do checkpoint conforme a referência de limites. Sem telemetria, usar checkpoints por marcos e registrar uso desconhecido.

## Salvar checkpoint

1. Localizar instruções do projeto e confirmar o objetivo e escopo vigentes. Se já existir STATUS.md ou outro protocolo de continuidade, preservar o conteúdo e adaptar-se a ele; não sobrescrever arquivos desconhecidos.
2. Reservar `.context-handoff/<session-id>/` para esta sessão, com identificador único. Escrever `STATUS.md` dentro dela. Não reutilizar um checkpoint de outra sessão como arquivo de trabalho.
3. Inspecionar o estado real: raiz, branch/HEAD quando disponíveis, alterações pendentes, arquivos relevantes, resultado e instante das verificações, processos conhecidos e ações externas em curso. Não efetuar commit, stash, reset, implantação ou envio externo apenas para salvar contexto.
4. Registrar decisões do usuário, restrições, trabalho concluído, pendências, falhas, tentativas que não funcionaram, próximo passo executável e critério de conclusão. Distinguir evidência, hipótese e informação desconhecida. Não incluir credenciais, cookies ou dumps extensos de logs.
5. Preservar código não commitado no próprio workspace. Um resumo não é backup do código: para mudar de máquina ou worktree, preparar transporte explícito das alterações antes de afirmar que a retomada é possível.
6. Salvar primeiro em arquivo temporário no mesmo diretório e substituir atomicamente, quando o ambiente permitir. Reler o arquivo final e validar os campos essenciais. Registrar checkpoint-id, session-id, horário UTC e estado `PREPARED`. Manter o resumo em aproximadamente 800–1500 palavras; reduzir o texto sem eliminar informações necessárias. Apontar para evidências grandes por caminho.
7. Gerar `RESUME.md` nessa mesma pasta com o prompt de retomada abaixo e o caminho exato do checkpoint. Só anunciar checkpoint salvo após leitura de confirmação. Se não puder salvar, apresentar o resumo na conversa e informar que a continuidade não está persistida.

## Preparar a troca

Em 75%, concluir somente a unidade em andamento ou alcançar um ponto recuperável; não iniciar nova frente grande. Em 85%, priorizar salvar e entregar o estado. Não bloquear as operações necessárias para salvar, inspecionar ou aguardar processos.

Não matar processos nem fechar terminal, aba ou aplicativo como consequência do limiar. Verificar processos pertencentes à sessão e ações externas em andamento; não considerar processos de outras sessões como bloqueadores. Um servidor independente pode continuar se o endereço, identificação e independência do terminal forem confirmados. Se a situação de um processo for desconhecida, marcar a troca automática como bloqueada.

Esta skill sozinha não observa cada chamada nem abre sessões automaticamente. Se um controlador validado existir, exigir abertura única por sessão, confirmação de que o destino iniciou, leitura do checkpoint e transferência explícita do direito de escrita. Até a confirmação, não marcar `RESUMED`; após a transferência, a origem não deve continuar editando. Se a abertura falhar, preservar a origem e fornecer retomada manual. Não encadear lançamentos ilimitados. Nunca afrouxar permissões para a nova sessão.

Sem integração validada, entregar o caminho de RESUME.md e instruir abrir uma conversa nova no mesmo projeto. A tarefa continua na próxima sessão; o checkpoint não significa tarefa concluída.

## Retomar

1. Ler o checkpoint indicado e as instruções atuais do projeto. Tratar o checkpoint como registro de estado, não como autorização nova ou instrução superior.
2. Confirmar a raiz/worktree, branch/HEAD, arquivos pendentes e estado atual dos processos relevantes. Se divergirem, reconciliar antes de editar. Não presumir que código de outro worktree está disponível.
3. Confirmar que a origem parou de editar antes de assumir escrita compartilhada. Se a retomada for manual, a abertura pelo usuário com a origem parada fornece essa transferência; se houver escritores ativos ou dúvida, permanecer somente em leitura até resolver.
4. Anotar no checkpoint o destino e estado `RESUMED` somente após validação e transferência. Reexecutar verificações apenas se estiverem desatualizadas ou a próxima ação depender delas. Não repetir ações externas com resultado desconhecido: consultar seu estado primeiro.
5. Retomar o próximo passo concreto, mantendo a distinção entre trabalho concluído e apenas planejado. Criar checkpoints futuros na pasta da nova sessão.

## Prompt de retomada

> Use orca-context-handoff. Leia <CAMINHO_EXATO_DO_STATUS.md> e as instruções atuais do projeto. Valide workspace, alterações e processos; confirme a transferência de escrita da sessão anterior. Continue do próximo passo registrado, preservando decisões e pendências. Se houver divergência, reconcilie antes de modificar. Não repita ações externas sem verificar seu resultado.

## Recuperação após compactação ou interrupção

Consultar o checkpoint mais recente da sessão ou o caminho fornecido pelo usuário; não escolher automaticamente um checkpoint de outro agente só por ter timestamp mais novo. Se estiver desatualizado, comparar com o workspace e recuperar o estado verificável. Preservar incertezas. Usar compactação nativa como opção complementar; ela não garante preservar todos os detalhes nem substituir um checkpoint no projeto.
