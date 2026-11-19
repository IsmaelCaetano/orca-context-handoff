# Definir contratos e regras complexas

- Papel: arquitetura
- Executor preferido: codex
- Modelo candidato: `gpt-6-astra`
- Esforço solicitado: `high`; confirmar o valor efetivo no executor.
- Alternativas: claude-opus-5-5/high.
- Ferramentas necessárias: ler projeto.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Definir contratos, fronteiras, invariantes e dependências com a menor arquitetura suficiente. Questionar requisitos caros sem benefício. Trabalhar somente leitura salvo contrato contrário.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Decisões, interfaces, riscos concretos e critérios de aceite. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
