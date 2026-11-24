# ORCA Context Handoff 3.0

Salvamento e retomada de projetos entre sessões de agentes no Orca, agora com **controlador Python executável**. O objetivo é salvar o trabalho, abrir o próximo agente, confirmar a leitura do estado e encerrar exclusivamente o terminal da origem.

## O que mudou

A versão anterior era somente instrução. Esta versão adiciona scripts de monitoramento, máquina de estados durável, verificação de checkpoints/workspace, abertura pelo Orca, confirmação do sucessor e fechamento condicionado da origem. Não usa LLM para vigiar.

**Implementado e testado localmente; ainda exige instalação e teste na sua versão do Orca.** Os testes simulam Orca/LLM, sem chamadas pagas. Não afirmar que seu PC já foi atualizado pelo simples push no GitHub.

## Limites para todos os agentes

| Contexto corrente | Procedimento |
| --- | --- |
| 400 mil | Pedir checkpoint |
| 450 mil | Solicitar handoff e parar novas alterações de produto |
| Por volta de 500 mil | Alvo para completar a transferência |
| 600 mil | Teto absoluto da política |

Mesma regra para Claude, Codex, Gemini, maestro, workers e subagentes registrados. Janelas menores e reserva de execução antecipam esses valores. O pedido chega em 450 mil para haver espaço para salvar e fazer o handshake. O runtime não garante que uma resposta grande nunca ultrapasse um teto entre amostras. Cota/créditos não são contexto e não se renovam abrindo conversa nova.

[Política e fórmula](skills/orca-context-handoff/references/limits.md).

## Fluxo implementado

1. O controlador acompanha telemetria vinculada à sessão e solicita checkpoint/transição.
2. A origem grava e relê STATUS.md e RESUME.md; verifica processos e libera a escrita.
3. O controlador valida hashes e abre o próximo agente no mesmo workspace, com instruções de retomada.
4. O destino lê o checkpoint e confirma accept, ainda sem editar.
5. O controlador confirma a identidade e fecha o terminal da origem.
6. Só após confirmação do fechamento libera o sucessor para continuar.

Se faltar checkpoint, houver dependentes, timeout, divergência ou encerramento não confirmado, mantém a transferência bloqueada. Não abre sessões repetidamente nem fecha o projeto inteiro.

## Instalar no Orca

Baixe por Code → Download ZIP. Copie a pasta completa `skills/orca-context-handoff` para:

| Host | Destino no projeto |
| --- | --- |
| Codex e Antigravity | `.agents/skills/orca-context-handoff/` |
| Claude Code | `.claude/skills/orca-context-handoff/` |

Para usar o maestro, copie também `skills/orca-maestro` para os diretórios correspondentes. Compare instalações existentes antes de substituir. Mantenha cópias da mesma skill equivalentes e escolha um caminho estável para o helper do controlador.

Depois, siga **[instalação e ativação do controlador](skills/orca-context-handoff/references/automatico.md)**. São necessários Python 3.10+, Git local, Orca CLI, configuração do modelo/argv, um terminal exclusivo para o vigia e registro dos agentes. Não existem nomes de modelos universais embutidos; use os realmente disponíveis e permitidos no seu host.

### Compatibilidade real desta versão

| Host | Medição de contexto | Controle durante a troca |
| --- | --- | --- |
| Claude Code | Adaptador statusline + registro da sessão | Guard PreToolUse e handshake |
| Codex CLI | Rollout token_count por sessão | Gate cooperativo e handshake |
| Gemini CLI / Antigravity / outros | Entrada normalizada por adaptador local | Gate cooperativo e handshake; sem medidor nativo validado neste pacote |

O launcher aceita comandos verificados de qualquer agente, mas **não inventa telemetria** nem controla uma interface Antigravity sem adaptador. Sem dados confiáveis, informar modo assistido; gate retorna PARAR. Os adaptadores precisam ser testados no host instalado.

## Pedido para instalar e ativar

```text
Instale/atualize orca-context-handoff 3.0 deste repositório neste projeto.
Leia references/automatico.md. Preserve configurações existentes.
Configure os comandos/modelos reais de cada agente, sem bypass de permissões.
Ative o controlador num terminal separado e registre maestro e workers com
telemetria real. Teste a transição em projeto descartável com limites sintéticos,
sem alterar medições do projeto real. Mostre os eventos gravados, a abertura
do sucessor, o ACK, o fechamento exclusivo da origem e a retomada.
Só declare automatic_validated após esse teste no host real.
Se um host não expuser telemetria, informe exatamente a integração faltante.
```

## Acompanhar salvamentos

- `.context-handoff/<session-id>/STATUS.md`: estado, decisões, pendências e próximo passo.
- `.context-handoff/<session-id>/RESUME.md`: instruções de retomada.
- `.orca/handoff/events.jsonl`: eventos do controlador.
- `.orca/audit/handoffs/CONTROLLER.md`: índice legível com horários.
- `handoff.py --root "<projeto>" status`: sessões e estados.

Sem controlador, ainda é possível usar a skill manualmente: `$orca-context-handoff` no Codex, `/orca-context-handoff` no Claude ou pedido explícito no Antigravity. Salvar também após entregas e etapas relevantes, sem depender só dos tokens.

## Validação

```powershell
python -m unittest discover -s tests -v
```

Testes incluem transição completa de estados, processo real aguardando liberação, falhas de criação/fechamento, ACK ausente, hashes divergentes, telemetria Claude/Codex, janelas menores e quoting de caminhos. Orca e agentes LLM são simulados. O teste não substitui homologação em Windows/Orca.

## Referências

- [Skill principal](skills/orca-context-handoff/SKILL.md)
- [Automação e instalação](skills/orca-context-handoff/references/automatico.md)
- [Limites globais](skills/orca-context-handoff/references/limits.md)
- [Detalhes por plataforma](skills/orca-context-handoff/references/platforms.md)
- [Script do controlador](skills/orca-context-handoff/scripts/handoff.py)
- [Modelo de checkpoint](skills/orca-context-handoff/assets/checkpoint.md)
- [Maestro e roteamento](ORCA_MAESTRO.md)

Inspiração: [Jhonatan-de-Souza/KillTheContext](https://github.com/Jhonatan-de-Souza/KillTheContext). Implementação escrita independentemente. Os checkpoints não substituem backup do código; permissões e credenciais não migram automaticamente.
