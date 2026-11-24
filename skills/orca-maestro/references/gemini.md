# Gemini por demanda

Conferência documental: 24/11/2026. Catálogo API e disponibilidade no CLI/Antigravity são superfícies diferentes. Confirmar ID no seletor da conta, ferramentas, autenticação, custo e agrupamento de cota antes de ativar.

| Modelo candidato | ID documental | Uso inicial sugerido |
|---|---|---|
| Gemini 4 Carbon | gemini-4-carbon | Arquitetura, análise extensa, segurança, diagnóstico difícil e maestro de contingência |
| Gemini 4 Neon | gemini-4-neon | Desenvolvimento e análises complexas; candidato alternativo após confirmar acesso |
| Gemini 4 Argon | gemini-4-argon | Engenharia e raciocínio com atenção a duração/consumo; alternativa de especialista |
| Gemini 4 Hydrogen | gemini-4-hydrogen | Pesquisa com web, documentação, conteúdo, frontend delimitado e rotina |
| Gemini 3.8 Flash | gemini-3.8-flash | Triagem e tarefas delimitadas quando disponível |
| Gemini 3.5 Flash-Lite | gemini-3.5-flash-lite | Extração/classificação simples; não substituir revisor crítico apenas para manter execução |
| Gemini 3.1 Pro Preview | gemini-3.1-pro-preview | Compatibilidade em hosts que só o oferecem; usar apenas se disponível e ciclo de vida verificado |

São preferências operacionais, não ranking medido. Não presumir que todos estão no seu plano. Modelos de imagem/áudio/vídeo exigem fluxo próprio e não servem como substitutos genéricos de desenvolvimento.

Usar /model e a ajuda da versão instalada. Depois de confirmar o ID, o formato é gemini --model ID_CONFIRMADO. Usar esforço padrão do executor; configurar thinking apenas com parâmetro documentado e suportado, sem importar nomes/níveis do Codex. Conferir modelo efetivo de cada subagente: o --model principal não necessariamente o altera.

Conferir /stats model quando disponível, com horário e escopo. Tokens acumulados da sessão não são saldo de assinatura. Não fixar limites comerciais numéricos na skill: variam por plano, autenticação e serviço. Uma assinatura de app web não comprova direito de API/CLI. Trocar modelo pode continuar no mesmo pool de quota.

## Fontes

- Catálogo atual: https://aistudio.google.com/docs/models
- Seleção de modelo no Gemini CLI: https://geminicli.com/docs/cli/model/
- Cota e preços por autenticação: https://geminicli.com/docs/resources/quota-and-pricing/
