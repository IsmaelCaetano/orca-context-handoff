# Limites globais de contexto — v3.0

Aplicar a TODOS os agentes registrados: Claude, Codex, Gemini/Antigravity com adaptador, maestro, workers e subagentes. Os limites são preferências do usuário, não limites oficiais do provedor.

| Marco | Teto em contexto corrente |
| --- | --- |
| Checkpoint | 400.000 |
| Preparação e pedido automático de handoff | 450.000 |
| Alvo de transferência | 500.000 |
| Teto absoluto da política | 600.000 |

A solicitação ocorre na preparação, para que a gravação e o handshake terminem próximo de 500 mil. Não continuar desenvolvimento normal esperando 600 mil. O tempo da troca depende dos agentes, ferramentas e processos; não existe garantia matemática de não ultrapassar o teto entre respostas da API.

Para capacidade efetiva C confirmada e reserva configurada, usar R = max(15.000, 10% de C, reserva_configurada):

- handoff = max(0, min(500.000, 85% de C, C − R, 600.000 − R));
- preparação = min(450.000, 75% de C, handoff);
- checkpoint = min(400.000, 60% de C, preparação).

| C | Checkpoint | Solicitar transição | Alvo de handoff |
| --- | --- | --- | --- |
| 128.000 | 76.800 | 96.000 | 108.800 |
| 200.000 | 120.000 | 150.000 | 170.000 |
| 400.000 | 240.000 | 300.000 | 340.000 |
| 1.000.000 | 400.000 | 450.000 | 500.000 |

Se uma próxima operação puder expandir muito o contexto, aumentar reserve_tokens ou solicitar handoff antes. Uma ocupação acima do teto dispara recuperação, não autorização para continuar produto. Não matar processos nem fechar toda a aplicação para cumprir o limiar.

## Telemetria

- Claude statusline: somar input_tokens + cache_read_input_tokens + cache_creation_input_tokens de context_window.current_usage. Capacidade: context_window.context_window_size. Null significa desconhecido; invalidar a amostra anterior.
- Codex rollout: usar info.last_token_usage.total_tokens do evento token_count, que no código upstream representa o contexto ativo; não usar total_token_usage nem somar cache novamente. Capacidade: model_context_window.
- Outro host: publicar JSON normalizado com session_id, tokens, capacity e source e vínculo explícito à sessão. Não usar contadores de cota como contexto.

Amostras ausentes/antigas bloqueiam gate para trabalho normal, sem inventar consumo e sem fechar a origem. A supervisão automática exige atualização pelo host. Observe manual não transforma host sem telemetria em integração validada.

Créditos, rate limit e cota por período são diferentes. Trocar conversa não restaura assinatura. Os limites anteriores exclusivos Claude e a regra que deixava outros provedores somente em percentuais ficam substituídos pela fórmula global acima.
