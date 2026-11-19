# Validar comportamento e regressão

- Papel: testes
- Executor preferido: codex
- Modelo candidato: `gpt-6.1-sol`
- Esforço solicitado: `high`; confirmar o valor efetivo no executor.
- Alternativas: claude-sonnet-5-5/high.
- Ferramentas necessárias: terminal, ambiente de teste.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Derivar verificações dos critérios de aceite. Executar checks e testes pertinentes, criando apenas testes úteis para risco real. Distinguir executado, falhou e bloqueado. Usar dados de teste.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Comandos, resultados, logs e aceite por comportamento. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
