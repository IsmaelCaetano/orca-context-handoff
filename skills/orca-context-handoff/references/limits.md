# Política de limites

Valores de operação propostos, sem alegação de serem limites oficiais ou uma garantia de qualidade.

| Contexto efetivo ocupado | Ação |
| --- | --- |
| Menos de 60% | Trabalhar; salvar em marcos relevantes |
| 60% | Salvar checkpoint e continuar |
| 75% | Preparar próxima sessão; evitar iniciar frente grande |
| 85% | Concluir entrega de contexto no primeiro ponto seguro |

Exemplos aritméticos, somente quando a capacidade efetiva for confirmada:

| Capacidade efetiva | Checkpoint 60% | Preparar 75% | Transição 85% |
| --- | --- | --- | --- |
| 128.000 | 76.800 | 96.000 | 108.800 |
| 200.000 | 120.000 | 150.000 | 170.000 |
| 400.000 | 240.000 | 300.000 | 340.000 |
| 1.000.000 | 600.000 | 750.000 | 850.000 |

Considerar como reserva inicial R = max(15.000 tokens, 10% da capacidade), aumentando se a próxima resposta ou ferramenta exigir mais. Antecipar o limiar de transição para min(85% da capacidade, capacidade − R). Manter os limiares anteriores abaixo dele. Se a reserva já não couber, salvar imediatamente o mínimo verificável. Esses valores são uma heurística operacional; não há evidência de um percentual universal de degradação.

Medir contexto corrente, não consumo acumulado ou quota de assinatura. Campos de cache podem compor o contexto em alguns transcripts, mas o significado e possíveis sobreposições precisam ser verificados no adaptador de cada host. Campos ausentes ou modelo desconhecido significam medição desconhecida, nunca zero. Janela efetiva pode mudar ao trocar de modelo. Não inferir que 400k é seguro porque o modelo anuncia 1M.

Sem telemetria: salvar após concluir feature, antes de operação longa e antes de trocar ferramenta/modelo/worktree. Como lembrete inicial, revisar necessidade de checkpoint a cada 20 chamadas de ferramenta ou 30 minutos de trabalho ativo, quando essas medidas estiverem disponíveis. Isso não estima tokens, não é timer em segundo plano e não encerra sessão automaticamente.

Quota de 5 horas, limite semanal, créditos e rate limit são restrições diferentes. Abrir conversa nova não restaura essas quotas. Se a quota impedir continuar, persistir checkpoint e aguardar a liberação ou usar outro provedor autorizado.

## Exemplos de decisão

- 156k de 200k (78%): preparar troca e finalizar unidade atual.
- 172k de 200k com teste em andamento: salvar checkpoint, registrar teste e aguardar/transferir supervisão; não matar o teste.
- Modelo desconhecido e 350k tokens acumulados faturados: percentual desconhecido; não usar esse número como ocupação.
- 80k de 128k depois de compactar: 62,5%; manter checkpoint e continuar a partir de estado validado.
