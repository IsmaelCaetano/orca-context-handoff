# ORCA Maestro

Skill para coordenar projetos no ORCA com **Claude Opus 5.5 em medium** fixo. A família GPT-6.2 está excluída de todos os papéis e alternativas.

## Usar no projeto

1. Baixar este repositório ou atualizar sua cópia.
2. Copiar a pasta completa `skills/orca-maestro` para `.claude/skills/orca-maestro` na raiz do projeto ORCA, preservando as referências e assets. Conferir se a versão do Claude Code reconhece a skill.
3. Conferir `claude --help` e iniciar o maestro com `claude --model claude-opus-5-5 --effort medium` quando esses parâmetros forem suportados.
4. Pedir: “Use orca-maestro neste projeto. Confira os modelos disponíveis, mantenha Opus 5.5/medium como maestro, exclua GPT-6.2 e monte a equipe conforme a demanda. Priorize minhas assinaturas e não contrate API.”

Se o carregamento nativo não estiver disponível, manter a pasta em `skills/orca-maestro` e pedir explicitamente a leitura de `skills/orca-maestro/SKILL.md`.

## Conteúdo

- [Skill principal](skills/orca-maestro/SKILL.md)
- [Modelos por demanda e fontes](skills/orca-maestro/references/modelos.md)
- [Verificação obrigatória pelo maestro](skills/orca-maestro/references/verificar-modelos.md)
- [11 fichas individuais](skills/orca-maestro/references/agentes)
- [Presets estruturados](skills/orca-maestro/assets/roteamento.json)
- [Perfis de projeto](skills/orca-maestro/references/perfis.md)

As fichas são prompts portáteis, não agentes já cadastrados no ORCA. A skill orienta o maestro a usar o controle de sessões realmente disponível. O JSON é um preset documental, não um formato nativo de importação. Sem acesso confirmado, a sessão fica pendente; sem ferramentas reais, não há alegação de pesquisa, teste ou validação visual.

Conferência documental: 19/11/2026. Preferências iniciais por tarefa, sem alegação de vencedor universal. A instalação é no projeto escolhido; não requer instalação na conta ChatGPT.
