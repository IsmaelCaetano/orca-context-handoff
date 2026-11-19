# Validar telas e interações

- Papel: visual
- Executor preferido: codex
- Modelo candidato: `gpt-6.1-terra`
- Esforço solicitado: `medium`; confirmar o valor efetivo no executor.
- Alternativas: claude-sonnet-5-5/medium.
- Ferramentas necessárias: navegador.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Inspecionar versão executável com navegador. Testar viewport mobile/desktop, fluxo principal, teclado e estados pertinentes. Registrar screenshots e erros observados. Não afirmar validação visual por leitura de código.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Viewport, ações, screenshots e defeitos reproduzíveis. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
