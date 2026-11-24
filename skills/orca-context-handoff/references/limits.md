# Política de limites

Valores de operação propostos, sem alegação de serem limites oficiais ou uma garantia de qualidade.

| Contexto efetivo ocupado | Ação |
| --- | --- |
| Menos de 60% | Trabalhar; salvar em marcos relevantes |
| 60% | Salvar checkpoint e continuar |
| 75% | Preparar próxima sessão; evitar iniciar frente grande |
| 85% | Concluir entrega de contexto no primeiro ponto seguro |

## Perfil Claude — preferência do usuário, 24/11/2026

Aplicar a qualquer sessão que use modelo Claude, inclusive maestro e workers, independentemente da interface. Os números são tokens de contexto corrente, não créditos, consumo acumulado ou cota. Outros provedores mantêm a política geral.

| Marco | Teto específico Claude |
| --- | --- |
| Salvar checkpoint | 300.000 tokens |
| Preparar troca, sem iniciar frente grande | 350.000 tokens |
| Iniciar handoff e cessar trabalho de produto na origem | 400.000 tokens |
| Teto absoluto de contexto permitido pela política | 600.000 tokens |

**400.000 é o alvo de troca; 600.000 não é uma meta de trabalho nem autorização para continuar desenvolvendo.** Entre o handoff e o teto, realizar apenas o mínimo necessário para salvar/verificar estado, acompanhar ou transferir processos e entregar a retomada. Não esperar chegar a 600.000 para salvar.

Para capacidade efetiva C confirmada e reserva R = max(15.000, 10% de C, estimativa conservadora de expansão da próxima ação), calcular:
- checkpoint = min(60% de C, 300.000);
- preparação = min(75% de C, 350.000);
- handoff = min(85% de C, C − R, 400.000, 600.000 − R).

Antecipar checkpoint e preparação se a reserva reduzir o limiar de handoff abaixo deles. Se o limiar já foi cruzado, executar a ação correspondente imediatamente no próximo controle, sem esperar novo cruzamento. Ao projetar estouro de C ou de 600.000, não iniciar a chamada; usar o checkpoint disponível para retomada. Se a medição já ultrapassou o teto, registrar o incidente e não fazer outra chamada normal de desenvolvimento na origem. Um limiar não autoriza matar processos ou fechar terminais.

Exemplos com reserva inicial (antes de considerar expansão adicional):
| C | Checkpoint | Preparação | Handoff |
| --- | --- | --- | --- |
| 200.000 | 120.000 | 150.000 | 170.000 |
| 400.000 | 240.000 | 300.000 | 340.000 |
| 1.000.000 | 300.000 | 350.000 | 400.000 |

Registrar no checkpoint modelo, capacidade, ocupação observada, origem da medição e limiares efetivos. Se houver controlador local, atualizar sua configuração separadamente e testar os cruzamentos e a reserva antes de afirmar que o teto está sendo aplicado. Alterar esta skill não reconfigura um vigia já instalado.

Sem telemetria confiável, não é possível assegurar o teto numérico: registrar essa limitação e salvar ao iniciar/retomar, após entregas e etapas relevantes e antes de trocar sessão. A regra em Markdown não intercepta chamadas nem impede sozinha que uma resposta grande ultrapasse o teto. Não alegar bloqueio automático sem controlador validado.

Esta é uma preferência operacional para antecipar a troca por consumo percebido pelo usuário. Não comprova economia financeira, não pressupõe cobrança extra acima de 400.000 e não renova cotas de uso.

## Exemplos gerais (Codex e outros provedores)

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
