# Adaptar ao executor e ao ORCA

O ORCA lança executores de terminal; os controles disponíveis variam por versão. Conferir ajuda e documentação antes de editar configuração. Não supor uma API universal de maestro.

## Descoberta

No Windows, usar `Get-Command orca,codex,claude,gemini -ErrorAction SilentlyContinue` no PowerShell ou `where` no CMD. No Linux/macOS, usar `command -v` para cada executável. Consultar `--version` e `--help` individualmente. Não ler ou imprimir arquivos de credenciais. Confirmar o modelo selecionado pela UI ou metadados da sessão, nunca apenas pelo texto que o agente afirma.

## Codex

Exemplo de lançamento candidato, depois de confirmar ajuda, ID e acesso:

```sh
codex --model gpt-6.1-sol -c 'model_reasoning_effort="medium"'
```

PowerShell também aceita a string entre aspas simples; no CMD ajustar a citação conforme a ajuda e verificar o valor recebido. Não executar exemplos com placeholders não resolvidos. Conferir se a versão aceita `model_reasoning_effort`; não presumir que todo nível existe em todo modelo. Usar `/model` ou seletor quando a versão instalada oferecer. Assinatura ChatGPT é um método possível de acesso ao Codex; o aplicativo ChatGPT não é um executável chamado `chatgpt`.

## Claude Code

Após confirmar ID e acesso, o formato documental é:

```sh
claude --model claude-opus-5-5 --effort medium
```

O comando acima é o lançamento preferido do maestro, condicionado ao suporte da versão instalada. Conferir `/model`, `/effort`, ajuda e configuração de esforço na versão instalada antes de fixar medium/high. Não enviar parâmetros TOML do Codex ao Claude. Se o parâmetro não existir, registrar esforço como padrão/não configurável. Alias como `sonnet` pode mudar de versão; registrar ID efetivo.

## Gemini CLI e Antigravity

Usar `/model` para descobrir acesso; o formato do Gemini CLI é `gemini --model ID_CONFIRMADO`. Substituir o placeholder antes de executar. Os IDs da API no catálogo são candidatos; usar somente os reconhecidos pelo executor e conta. Configuração de modelo da sessão principal pode não afetar subagentes nativos: confirmar cada sessão filha.

Antigravity tem integração e seletor próprios. Não tratá-lo como sinônimo do Gemini CLI. Identificar versão e mecanismos existentes; sem documentação suficiente, preparar orientação de seleção e declarar aplicação pendente.

## Transporte da skill ao projeto

Conservar esta pasta como fonte. No projeto ORCA, usar mecanismo de skills suportado pelo executor. Para Codex/Claude, copiar para `.agents/skills/orca-maestro/` e `.claude/skills/orca-maestro/` apenas onde esses locais forem suportados pela versão. Para Gemini, usar extensão/skill nativa documentada ou referência explícita em `GEMINI.md` ao caminho relativo `skills/orca-maestro/SKILL.md`; para outros hosts, referência em `AGENTS.md`. Não afirmar reconhecimento automático sem verificar.

Ao acrescentar instruções, preservar conteúdo existente. Um fallback portátil é armazenar a pasta em `skills/orca-maestro/` e enviar explicitamente: “Leia skills/orca-maestro/SKILL.md e use para montar a equipe deste projeto”. Isso disponibiliza instruções; não instala executores nem cria sessões sozinho.

## Cota e falhas

Não equivaler assinatura a API gratuita. Não inventar limites de cinco horas, saldo ou reset; usar somente UI/metadados observados com horário. Em rate limit, preservar trabalho, registrar estado e escolher alternativa confirmada dentro do orçamento. Se não houver alternativa, informar bloqueio. Não repetir autenticação automaticamente nem expor tokens nos logs.

## Distribuição

Manter a versão fonte no GitHub. Não instalar esta skill na conta ChatGPT. Instalar no projeto ORCA apenas quando solicitado. Fichas em `references/agentes/` são contratos portáteis; não copiar como agentes nativos Claude sem converter o frontmatter segundo a documentação da versão.

## Troca entre executores

Usar continuidade.md e gemini.md. Conferir no host se há controlador de processos/sessões independente do maestro. Não inventar flags ORCA de fallback. Sem controlador, gerar RESUME em disco e comandos confirmados para retomada assistida. Confirmar a parada de processos escritores antes de passar a tarefa; worktrees distintos não tornam segura a duplicação de uma ação externa. Não mudar credencial, conta ou habilitar faturamento para resolver cota. A política permite substituto temporário do maestro por cota, preservando Opus 5.5/medium como preferência.
