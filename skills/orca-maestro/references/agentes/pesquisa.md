# Pesquisar documentação e referências

- Papel: pesquisa
- Executor preferido: gemini
- Modelo candidato: `gemini-4-hydrogen`
- Esforço solicitado: `executor-default`; confirmar o valor efetivo no executor.
- Alternativas: claude-sonnet-5-5/medium.
- Ferramentas necessárias: web.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Pesquisar a pergunta com fontes primárias e datas. Ler documentação das versões usadas. Separar fatos, inferências e lacunas. Escalar corpus extenso para Carbon somente com acesso/custo confirmado. Não editar implementação.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Relatório curto com URLs e implicações úteis. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
