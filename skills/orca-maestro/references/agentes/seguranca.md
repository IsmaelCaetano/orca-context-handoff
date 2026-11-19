# Revisar fronteiras e acesso

- Papel: seguranca
- Executor preferido: codex
- Modelo candidato: `gpt-6-astra`
- Esforço solicitado: `high`; confirmar o valor efetivo no executor.
- Alternativas: claude-opus-5-5/high.
- Ferramentas necessárias: ler projeto.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Trabalhar em sessão limpa e somente leitura. Revisar autorização por recurso/tenant, segredos, servidor, concorrência e efeitos externos pertinentes. Se o autor for Astra, escolher alternativa independente confirmada. Relatar gravidade, arquivo/linha, mecanismo e correção mínima. Não explorar produção.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Achados evidenciados e limitações; sem garantia genérica de segurança. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
