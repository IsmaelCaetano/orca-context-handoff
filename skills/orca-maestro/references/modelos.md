# Catálogo por demanda

Conferência documental: 24/11/2026. Acesso no host do usuário não verificado. Escolhas são hipóteses operacionais fundamentadas no posicionamento oficial e no tipo de trabalho; não são um ranking medido entre marcas. Verificar no projeto antes de confirmar. O catálogo é subordinado às restrições do proprietário.

## Regras fixas

- Maestro: `claude-opus-5-5`, `medium`, Claude Code. Não elevar esforço; permitir substituto temporário por cota/indisponibilidade conforme continuidade.md.
- Família excluída: `gpt-6.2*`, inclusive alternativas e rotas Auto. Só o usuário pode remover essa restrição.
- Assinatura não comprova acesso a API, cota ou disponibilidade no CLI.
- Pin concreto confirmado vale durante a tarefa; atualizar somente com decisão registrada. Não escolher o lançamento mais novo apenas por ser novo.

## Preferências de partida

| Demanda | Executor/modelo | Esforço desejado | Alternativa elegível | Justificativa operacional |
|---|---|---|---|---|
| Orquestração | Claude Code / Opus 5.5 | medium principal | Sol/medium → Carbon → Neon, elegíveis | Contingência autorizada, com retorno ao Opus |
| Arquitetura e regras difíceis | Codex / GPT-6 Astra | high | Opus 5.5/high em sessão especialista | Raciocínio multietapa; separar coordenação de análise profunda |
| Frontend e UX | Claude Code / Sonnet 5.5 | high | GPT-6.1 Sol/high | Implementação de componentes e refinamento iterativo |
| Backend, APIs, SQL e pipelines | Codex / GPT-6.1 Sol | high | Sonnet 5.5/high | Código recorrente com checks e custo de coordenação controlado |
| Pesquisa e documentação atual | Gemini CLI / Gemini 4 Hydrogen | padrão do executor | Sonnet 5.5/medium com web | Coleta e síntese rápidas; web real é requisito |
| Corpus extenso ou pesquisa difícil | Gemini CLI / Gemini 4 Carbon | padrão do executor | GPT-6 Astra/high | Capacidade multimodal e raciocínio sobre material extenso; verificar orçamento |
| Segurança | Codex / GPT-6 Astra | high | Opus 5.5/high em sessão limpa | Revisão adversarial; exigir evidências de acesso e servidor |
| Testes e regressão | Codex / GPT-6.1 Sol | high | Sonnet 5.5/high | Criar/executar verificações de comportamento com terminal |
| Validação visual | Codex / GPT-6.1 Terra | medium | Sonnet 5.5/medium com navegador | Leitura de telas e interação; browser é requisito |
| Revisão de código | Outro modelo/executor elegível diferente do autor, pela complexidade | high | Sessão limpa no mesmo executor | Reduzir viés da autoria; isolamento de contexto obrigatório |
| Copy e conteúdo | Claude Code / Sonnet 5.5 | medium | Gemini 4 Hydrogen/padrão | Iteração com público, voz e ação principal claros |
| Commit e integração | Maestro Opus 5.5 | medium principal | Coordenador temporário elegível | Operação rotineira, sem agente caro adicional |

`high`/`medium` são intenções por executor, não valores equivalentes de computação. Confirmar suporte antes de aplicar. Não enviar `reasoning_effort` do Codex a Gemini. Registrar configuração efetiva ou “não configurável”. Gemini 4 Neon é um candidato recém-publicado; não substituir os pins sem acesso confirmado e evidência na demanda real.

## Fontes primárias

- OpenAI perfis e acesso: https://learn.chatgpt.com/docs/models
- OpenAI seleção: https://learn.chatgpt.com/docs/model-selection
- Claude catálogo: https://platform.claude.com/docs/en/models/overview
- Claude Opus 5.5: https://platform.claude.com/docs/en/models/opus-5-5/overview
- Claude Code esforço e modelos: https://code.claude.com/docs/en/model-config
- Google catálogo: https://aistudio.google.com/docs/models
- Google seleção no CLI: https://geminicli.com/docs/cli/model/
- ORCA executores: https://github.com/stablyai/orca/blob/main/docs/site/content/docs/agents/supported.mdx

Atualizar a evidência ao iniciar projeto, após indisponibilidade ou pedido de atualização. Nunca adicionar modelo excluído porque uma fonte recomenda. Comparar entrega aceita, correções necessárias, duração e consumo observado na mesma classe de tarefa; não inventar notas ou percentuais de qualidade.

## Catálogo Gemini e continuidade

Ler [gemini.md](gemini.md) para Carbon, Neon, Argon, Hydrogen, Flash e compatibilidade Pro. As rotas em assets/roteamento.json incluem candidatos Gemini por papel; todos exigem confirmação real no CLI/Antigravity. Usar [continuidade.md](continuidade.md) para esgotamento de cota, troca de plataforma, escritor único, checkpoint e retomada sem repetir efeitos externos. Excluir todo pool esgotado antes de seguir a ordem das alternativas.
