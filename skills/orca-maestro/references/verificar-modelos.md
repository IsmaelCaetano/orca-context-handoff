# Verificação obrigatória pelo maestro

Executar no começo do projeto, após falha de acesso e antes de mudar um pin.

1. Ler restrições: Opus 5.5/medium como maestro; GPT-6.2 excluído; orçamento e autorizações existentes.
2. Confirmar host real, executores, versões e autenticação sem revelar credenciais. Instalação de CLI não significa conta autenticada.
3. Consultar catálogos oficiais e seletores disponíveis; registrar URLs e data. Se fontes divergirem, usar seletor/metadados reais para acesso e documentação compatível com a versão para parâmetros. Sem web, declarar catálogo não atualizado e usar somente modelos confirmados no host; não alegar pesquisa realizada.
4. Confirmar Opus 5.5 e esforço efetivo medium. Variáveis de ambiente, políticas e configurações por agente podem sobrepor o pedido; verificar o valor efetivo sem imprimir arquivos com segredos. Se não puder confirmar, marcar pendente; não prometer aplicação.
5. Para cada papel necessário, verificar executor, ID, ferramentas, esforço, acesso por assinatura ou API e cota se observável. Conferir se subagentes nativos herdam o modelo correto; não assumir herança.
6. Filtrar a família excluída ANTES de comparar candidatos, inclusive em alternativas, aliases e fallback automático. Usar ID concreto e conferir metadados da primeira resposta. Se fallback automático não puder ser restringido ou observado, não usar essa rota para delegação.
7. Selecionar pela capacidade necessária e evidência no projeto. Para papel difícil sem histórico, usar uma primeira tarefa real pequena, reversível e já autorizada como avaliação; não criar benchmarks caros nem efeitos externos só para comparar modelos.
8. Registrar modelo solicitado, modelo efetivo, esforço solicitado/efetivo, ferramentas, origem, horário, razão e alternativa em `.orca/maestro/<sessao>/`. Ausência de dado deve ficar explícita. Texto do próprio modelo não é prova de identidade.
9. Manter maestro fixo. Para especialista indisponível, escolher alternativa elegível confirmada e registrar motivo, sem nova cobrança não autorizada. Após uma alternativa falhar, reavaliar; evitar loop de nomes inventados.
10. Informar a equipe confirmada e as pendências. “Escolhido no plano”, “sessão aberta” e “entrega validada” são estados diferentes.

Para modelo do chatbot em produção, avaliar separadamente qualidade em casos anonimizados, chamadas de ferramenta, latência, privacidade e preço atual por volume. Não usar assinatura pessoal como orçamento de API de produção.
