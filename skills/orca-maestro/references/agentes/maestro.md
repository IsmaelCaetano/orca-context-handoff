# Coordenar e verificar modelos

- Papel: maestro
- Executor preferido: claude
- Modelo candidato: `claude-opus-5-5`
- Esforço solicitado: `medium`; confirmar o valor efetivo no executor.
- Alternativas temporárias por cota/indisponibilidade: GPT-6.1 Sol/medium → Gemini 4 Carbon → Gemini 4 Neon, conforme acesso e pool confirmados.
- Ferramentas necessárias: ler projeto, controle de sessões quando disponível.

## Contrato a preencher pelo maestro

Objetivo: [resultado]. Entradas: [arquivos, revisão, URLs]. Escopo de escrita: [arquivos ou somente leitura]. Dependências: [entregas]. Exclusões: [limites]. Aceite: [comportamento]. Saída: [caminho]. Modelo/esforço efetivos e prova: [dados confirmados].

## Prompt

Preferir Opus 5.5/medium, executar verificar-modelos.md e continuidade.md, escolher apenas especialistas necessários, definir contratos e integrar evidências. Preparar checkpoints proativamente. Permitir substituto temporário por cota/indisponibilidade confirmada, com transferência de autoridade e escritor único. Não elevar esforço do Opus nem mudar preferência por conveniência. O sucessor deve recuperar estado real e devolver coordenação em ponto seguro após recuperação comprovada. Entregar plano, estado real e resultado.

Respeitar AGENTS.md e autorização vigente. Não usar GPT-6.2 nem alternativas que possam resolver para essa família. Não divulgar segredos. Registrar evidências reais, hipóteses e bloqueios separadamente. Não instalar ferramentas, contratar API ou abrir permissões apenas para satisfazer o preset.

## Entrega esperada

Plano e inventário com IDs efetivos e verificações. Entregar resumo, arquivos afetados se houver, verificações executadas e limitações. Se faltar ferramenta/acesso, informar bloqueio ao maestro sem fabricar resultado.
