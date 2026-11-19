# Integrar e criar commit

- Papel: integracao
- Executor preferido: claude
- Modelo candidato: `claude-opus-5-5`
- Esforço solicitado: `medium`; confirmar o valor efetivo no executor.
- Alternativas: nenhuma automática.
- Ferramentas necessárias: git, terminal.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Executar como fase do maestro. Inspecionar status/diff, preservar trabalho do usuário, integrar sequencialmente e rodar checks obrigatórios. Selecionar somente escopo sem segredos. Commit/push/merge/deploy conforme autorização efetiva. Nunca apresentar hash sem sucesso observado.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Diff integrado, checks, hash se realizado e pendências. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
