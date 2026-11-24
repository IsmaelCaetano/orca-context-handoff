---
name: orca-maestro
description: Escolher um agente maestro, modelos, níveis de raciocínio e especialistas para projetos no ORCA. Usar ao montar equipes com Codex/ChatGPT, Claude Code, Gemini CLI ou Antigravity; distribuir pesquisa, UX, desenvolvimento, segurança, testes, revisão e integração; escolher modelos por qualidade, cota e custo; ou transferir tarefas entre plataformas após esgotamento de cota.
---

# ORCA Maestro

Escolher a menor equipe capaz de entregar com evidência. Tratar os perfis como recomendações iniciais, nunca como ranking universal. Não confundir modelo, agente executor, ferramenta e papel.

## 1. Reconhecer o ambiente

1. Ler AGENTS.md, instruções do host, objetivo, código e checks relevantes. Identificar projeto, risco, critério de aceite e autorização já concedida.
2. Identificar quais executores estão instalados, autenticados e utilizáveis no host real do ORCA. Consultar versões, ajuda e seletor de modelos sem imprimir credenciais. O ambiente desta conversa pode ser diferente do computador do usuário.
3. Executar a verificação do maestro em [verificar-modelos.md](references/verificar-modelos.md). Consultar [modelos.md](references/modelos.md). Confirmar ID, acesso e parâmetros no executor escolhido. Modelo publicado em API não comprova disponibilidade pela assinatura ou pelo CLI.
4. Registrar inventário usando [inventario.example.json](assets/inventario.example.json): executor, modelo exato, autenticação por assinatura/API, ferramentas, nível suportado, disponibilidade, origem e data. Registrar cota desconhecida como desconhecida. Nunca inferir saldo ou janela de renovação pelo plano.
5. Não instalar executores, alterar permissões ou trocar assinatura por API paga apenas para satisfazer um preset. Aproveitar autorização existente; pedir decisão somente quando houver bloqueio real ou nova despesa necessária.

## 2. Fixar maestro e escolher modo

Usar **Claude Opus 5.5 (`claude-opus-5-5`), esforço `medium`, no Claude Code** como maestro principal. Não elevar seu esforço nem trocar por novidade ou conveniência. Por autorização do proprietário, permitir substituto TEMPORÁRIO de outra plataforma quando houver cota esgotada ou indisponibilidade comprovada, seguindo [continuidade.md](references/continuidade.md) e a ordem em `assets/roteamento.json`. Manter a preferência original e devolver a coordenação em ponto seguro após recuperação confirmada. Se o esforço medium não for suportado, não usar outro esforço silenciosamente.

**Excluir toda a família GPT-6.2 (`gpt-6.2*`) de qualquer papel, alternativa, subagente nativo ou roteamento automático.** Atualização do catálogo não remove esta exclusão. Não afirmar que a família é universalmente ruim: respeitar a restrição do usuário sem inventar evidência comparativa.

Confirmar modelo e esforço efetivos na sessão principal e em cada filho. Conferir ambiente, configurações e eventuais fallbacks automáticos sem expor segredos. Não usar Auto/alias que possa resolver para modelo excluído. Preferir IDs concretos verificados. Caso o host não permita confirmar a exclusão e o modelo efetivo, marcar sessão pendente/bloqueada em vez de iniciá-la como confirmada.

Usar modo equilibrado por padrão. Todos os modos preservam a preferência Opus 5.5/medium e a política de contingência.

| Modo | Política operacional inicial |
|---|---|
| Econômico | Maestro e no máximo um especialista simultâneo. Revezar especialistas. |
| Equilibrado | Maestro e até dois especialistas simultâneos. Separar implementação e revisão por fase. |
| Crítico | Maestro e até três especialistas simultâneos. Usar especialistas fortes e revisão independente nas fronteiras críticas. |

São tetos de coordenação configuráveis, não limites dos produtos. Tarefa pequena: uma sessão e verificação proporcional. Não abrir todos os agentes por existirem fichas prontas.

## 3. Distribuir papéis

Ler [perfis.md](references/perfis.md) para selecionar site, SaaS/CRM, dados/BI, chatbot, automação ou manutenção. Ler [papeis.md](references/papeis.md) para o contrato comum. Consultar [roteamento.json](assets/roteamento.json) e a ficha individual em `references/agentes/` indicada ali. As fichas são prompts portáteis, não registros instalados no ORCA.

Escolher nesta ordem: capacidade e ferramentas necessárias → acesso confirmado → evidência no projeto → custo/cota → preferência do preset. Sem ferramenta de web, não atribuir pesquisa atual; sem navegador, não declarar validação visual; sem terminal, não declarar testes executados.

Priorizar sessão limpa para revisão; preferir outro modelo/executor quando disponível e útil. Independência não garante segurança. Delegar operações Git rotineiras ao maestro, sem criar agente premium apenas para escrever commit.

Quando o pedido for somente montar equipe/configuração, entregar o plano e os prompts. Iniciar agentes e código apenas quando execução fizer parte do pedido. Não criar tarefas fictícias para demonstrar a skill.

## 4. Tornar o plano verificável

Produzir uma tabela com papel, executor, ID do modelo, esforço efetivamente suportado, ferramenta, justificativa, alternativa e estado (proposto/confirmado/iniciado/concluído/bloqueado). Distinguir preset documental de configuração aplicada.

Criar ou atualizar `.orca/maestro/<sessao>/plano.md` no projeto somente quando houver autorização para escrever. Incluir objetivo, critérios de aceite, inventário sem segredos, decisões, dependências, responsáveis e arquivos de saída. Manter as evidências no projeto; preservar a skill genérica sem dados de cliente.

Fixar modelos confirmados durante a tarefa normal. Aplicar contingência registrada quando necessário, sem nova confirmação para cada troca já autorizada. Para cota de plataforma, excluir todo o pool afetado; trocar Sonnet por Opus pode continuar no mesmo limite. Para nome inválido, consultar o seletor uma vez; para auth/permissão/erro de código, tratar a causa sem rotação cega. Se todos os candidatos elegíveis falharem, salvar estado e marcar bloqueado.

## 5. Executar pelo mecanismo real

Ler [adaptadores.md](references/adaptadores.md). Usar a interface, CLI ou API documentada da versão instalada. Não inventar comandos `orca agents create`, arquivos de importação ou chaves de configuração. Esta pasta é uma skill instrucional; seus JSONs são modelos de registro, não configurações nativas do ORCA.

Antes de delegar, passar um contrato com objetivo, entradas, escopo de escrita, exclusões, dependências, critério de aceite e evidência esperada. Separar worktrees para escritores simultâneos; manter revisão somente leitura. Worktree não é sandbox nem fronteira de acesso.

Executar em paralelo apenas tarefas independentes. Integrar mudanças sequencialmente. Não permitir dois agentes alterando os mesmos arquivos na mesma árvore. Usar [plano-template.md](assets/plano-template.md) para registrar a coordenação.

Se não houver controle real de sessões, entregar comandos/prompts revisáveis e marcar pendente de aplicação; não declarar que o ORCA está configurado. Não habilitar bypass de permissões para resolver uma falha de coordenação.

## 6. Preparar continuidade antes de executar

Ler [continuidade.md](references/continuidade.md). No início, confirmar pelo menos uma alternativa em outra plataforma para papéis críticos, quando houver acesso. Criar checkpoints após marcos, antes de efeitos externos e antes de troca planejada. Usar [checkpoint-template.md](assets/checkpoint-template.md) e [evento-template.json](assets/evento-template.json). Não depender de uma última resposta do agente já sem cota para salvar o estado.

Manter apenas um dono ativo de escrita por tarefa e coordenação; confirmar parada/revogação do anterior antes de transferir. Se o host não conseguir controlar sessões ou observar erros sem LLM, registrar **continuidade assistida**, preparar a retomada e explicar a ação manual necessária. Uma skill instrucional não implementa monitor, wrapper de processos nem troca automática de terminal. Não afirmar failover automático testado apenas pela existência do JSON.

Para projeto novo, usar [inicio-projeto.md](references/inicio-projeto.md) para verificar ferramentas, permissões, mapa mínimo, critérios de aceite e retomada. Não instalar esta skill na conta ChatGPT; manter a fonte no GitHub.

## 7. Exigir evidência e concluir

- Definir testes a partir de comportamento e risco. Exigir checks do projeto e testes proporcionais, sem criar suítes que apenas copiem implementação.
- Para login, pagamentos, dados pessoais, autorização ou estado concorrente, revisar servidor, acesso por recurso, segredos, idempotência e integridade. Aplicar codigo-confiavel quando disponível.
- Não aceitar “seguro” ou “testado” sem comandos, resultados, arquivos e limitações. Registrar severidade e evidência dos achados.
- Após correção, repetir somente os checks afetados e os obrigatórios. Não iniciar ciclos ilimitados de revisão; após duas rodadas sem progresso, reavaliar causa, escopo ou capacidade.
- Antes do commit, inspecionar status/diff e selecionar apenas arquivos da tarefa, sem segredos. Commit local se autorizado pelo escopo; respeitar instruções existentes. Publicar, fazer push, merge ou deploy conforme autorização real, sem exigir confirmação repetida nem inferir autorização de publicação a partir de um pedido só de planejamento.
- Usar orca-context-handoff quando disponível e necessário; não confundir consumo de contexto com cota. Sem medição confiável, não fabricar percentuais.
- Entregar resultado, modelos efetivos, checks, alterações, pendências e próximo passo. Declarar custos e cotas desconhecidos quando não observáveis.

## Invocação

“Use orca-maestro. Projeto: site Next.js com Supabase. Modo: equilibrado. Priorizar minhas assinaturas existentes. Manter Opus 5.5/medium como maestro, excluir GPT-6.2, verificar modelos e preparar os especialistas antes de executar.”
