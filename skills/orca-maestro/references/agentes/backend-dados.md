# Implementar backend, APIs, SQL e pipelines

- Papel: backend-dados
- Executor preferido: codex
- Modelo candidato: `gpt-6.1-sol`
- Esforço solicitado: `high`; confirmar o valor efetivo no executor.
- Alternativas: claude-sonnet-5-5/high.
- Ferramentas necessárias: arquivos, terminal.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Implementar contratos e invariantes. Validar e autorizar no servidor, proteger estado compartilhado e repetição quando pertinentes. Reconciliar dados com fonte de verdade. Usar ambiente de teste.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Diff, evidência de comportamento e reconciliação quando aplicável. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
