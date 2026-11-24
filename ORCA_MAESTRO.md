# ORCA Maestro

Skill para coordenar projetos no ORCA com **Claude Opus 5.5 em medium** como principal e continuidade entre plataformas. A família GPT-6.2 está excluída de todos os papéis e alternativas.

## Usar no projeto

1. Baixar este repositório ou atualizar sua cópia.
2. Copiar a pasta completa `skills/orca-maestro` para `.claude/skills/orca-maestro` na raiz do projeto ORCA, preservando as referências e assets. Conferir se a versão do Claude Code reconhece a skill.
3. Conferir `claude --help` e iniciar o maestro com `claude --model claude-opus-5-5 --effort medium` quando esses parâmetros forem suportados.
4. Pedir: “Use orca-maestro neste projeto. Confira os modelos disponíveis, prefira Opus 5.5/medium, exclua GPT-6.2, prepare contingência entre plataformas e monte a equipe conforme a demanda. Priorize minhas assinaturas e não contrate API.”

Se o carregamento nativo não estiver disponível, manter a pasta em `skills/orca-maestro` e pedir explicitamente a leitura de `skills/orca-maestro/SKILL.md`.

## Conteúdo

- [Skill principal](skills/orca-maestro/SKILL.md)
- [Modelos por demanda e fontes](skills/orca-maestro/references/modelos.md)
- [Verificação obrigatória pelo maestro](skills/orca-maestro/references/verificar-modelos.md)
- [Fichas individuais](skills/orca-maestro/references/agentes)
- [Presets estruturados](skills/orca-maestro/assets/roteamento.json)
- [Perfis de projeto](skills/orca-maestro/references/perfis.md)

As fichas são prompts portáteis, não agentes já cadastrados no ORCA. A skill orienta o maestro a usar o controle de sessões realmente disponível. O JSON é um preset documental, não um formato nativo de importação. Sem acesso confirmado, a sessão fica pendente; sem ferramentas reais, não há alegação de pesquisa, teste ou validação visual.

Conferência documental: 24/11/2026. Preferências iniciais por tarefa, sem alegação de vencedor universal. A instalação é no projeto escolhido; não requer instalação na conta ChatGPT.

## Novo: continuidade por cota

- [Política de troca e retomada](skills/orca-maestro/references/continuidade.md)
- [Gemini por demanda](skills/orca-maestro/references/gemini.md)
- [Preparação do novo projeto e prompt](skills/orca-maestro/references/inicio-projeto.md)
- [Checkpoint/RESUME](skills/orca-maestro/assets/checkpoint-template.md)
- [Evento auditável](skills/orca-maestro/assets/evento-template.json)

Cota esgotada permite transferir tarefa e, se necessário, a coordenação temporária para outra plataforma confirmada, sem gastar com API nova. Preferência do maestro: Opus 5.5/medium; contingência: Codex Sol/medium, depois Gemini Carbon/Neon elegíveis. Não tentar outro modelo do mesmo pool esgotado. Após recuperação confirmada, retornar ao Opus em ponto seguro.

O pacote continua sendo uma skill instrucional. Troca realmente automática exige controlador existente no host que observe falhas, pare processos e abra sucessores. Sem ele, o modo é assistido, com checkpoint e RESUME preparados antecipadamente. Só instalar no projeto escolhido, não na conta ChatGPT. A preparação distingue cota, rate limit, contexto e erro de código; mantém escritor único e reconciliação de ações externas incertas.
