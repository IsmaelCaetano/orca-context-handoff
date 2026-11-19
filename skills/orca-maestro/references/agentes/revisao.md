# Revisar código independentemente

- Papel: revisao
- Executor preferido: codex
- Modelo candidato: `gpt-6-astra`
- Esforço solicitado: `high`; confirmar o valor efetivo no executor.
- Alternativas: claude-opus-5-5/high.
- Ferramentas necessárias: ler diff.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Escolher sessão limpa e modelo/executor diferente do autor quando disponível. Se autor Astra, usar Opus especialista; caso contrário preferir Astra para revisão difícil. Priorizar falhas concretas, contratos e regressões, citando linhas. Não editar nem aprovar por relato do autor.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Achados por impacto e critérios ainda não comprovados. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
