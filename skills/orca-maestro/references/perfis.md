# Perfis prontos

O maestro principal é Opus 5.5/medium; contingência temporária segue continuidade.md. Usar os IDs, esforços e alternativas em `assets/roteamento.json`, com confirmação no host. Fichas são papéis disponíveis; abrir somente os necessários e respeitar o teto do modo.

| Demanda | Especialistas por ordem de necessidade | Validação mínima |
|---|---|---|
| Landing page | pesquisa → copy/UX → frontend → validação visual → revisão | CTA, mobile, acessibilidade e estados pertinentes |
| Site com login | arquitetura → frontend/backend → segurança → testes → visual → revisão | Login, sessão, autorização e fluxo principal |
| SaaS/CRM | arquitetura → backend/dados + frontend → segurança → testes → revisão | Tenant/acesso por recurso, persistência, integrações e regressão |
| Chatbot | pesquisa → arquitetura → backend → segurança/testes → revisão | Qualidade da conversa, limites de ferramenta, acesso e repetição |
| Dados/BI | pesquisa quando necessária → backend/dados → testes → revisão | Chaves, nulos, contagens, totais e reconciliação com fonte |
| Automação | pesquisa → arquitetura quando necessária → backend → segurança/testes → revisão | Duplicatas, falha parcial, retries e efeitos externos |
| Pesquisa/negócios | pesquisa → arquitetura/análise somente se necessário → maestro | Fontes, fatos versus inferências, demanda e validação mais barata |
| Correção pequena | frontend ou backend → teste pertinente → revisão se risco justificar | Reproduzir, corrigir, verificar regressão sem ampliar escopo |

Em paralelo, usar worktrees separados para escritores; pesquisa pode ocorrer independentemente, mas revisão final depende do diff concluído e visual depende de versão executável. Commit/integrar é fase do maestro, após checks e inspeção de segredos.

Segurança e revisão devem usar sessão limpa, preferindo outro modelo/executor do autor. Se Astra tiver desenvolvido, usar Opus especialista para revisar; se Sonnet ou Sol tiver desenvolvido, Astra é preferência para revisão complexa. Opus especialista/high não altera o maestro/medium. Sem outro executor, usar sessão limpa e registrar menor independência.

Para chatbot em produção, avaliar modelo de resposta separadamente da equipe de construção. Não prometer custo zero pela assinatura dos executores. Para landing, não criar backend desnecessário. Para dados, não executar escrita em produção só para validar.

Modo crítico acrescenta revisão e especialistas, preservando o maestro preferido e a política de contingência. Tarefas simples não exigem equipe inteira. Modelo com bom posicionamento oficial continua sujeito à evidência real e às ferramentas disponíveis.

Para cada perfil, preparar rota Gemini elegível: Carbon/Neon para engenharia complexa e revisão; Hydrogen para pesquisa, conteúdo e tarefas delimitadas; Argon como alternativa confirmada quando adequado. Não trocar revisão de acesso/tenant por Flash-Lite só porque há cota. Validar ferramentas e capacidade do destino antes de confirmar retomada.
