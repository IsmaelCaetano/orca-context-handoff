# Preparar um projeto novo ou existente

1. Ler AGENTS.md e instruções atuais; localizar branch/worktree, alterações do usuário e processos ativos. Se já existe projeto, mapear o que existe antes de alterar stack ou recriar estrutura.
2. Definir objetivo, público/problema quando aplicável, menor entrega útil e critérios de aceite. Resolver escolhas reversíveis com contexto; perguntar somente dado que realmente bloqueia execução.
3. Criar mapa curto com pontos de entrada, módulos, persistência, integrações e checks. Atualizar por mudanças relevantes, sem documentação duplicada.
4. Confirmar Opus 5.5/medium e rotas de contingência em outra plataforma. Registrar quais acessos, modelos, ferramentas e pools foram confirmados versus apenas candidatos. Manter GPT-6.2 excluído.
5. Registrar modo de continuidade automático validado ou assistido, concorrência, orçamento e política de troca. Não anunciar monitoramento de cota se o host não o oferece.
6. Registrar plano, inventário, mapa, tarefas e checkpoint em .orca/maestro/<sessao>/. Manter dados privados do projeto fora da skill pública no GitHub; não publicar logs, checkpoints ou dados de clientes por padrão.
7. Para tarefas, registrar task_id, papel, modelo solicitado/efetivo, sessão, branch/worktree, dependências, dono da escrita, início/fim, estado e evidência. Estados mínimos: pending, running, paused_quota, handoff_pending, completed, blocked.
8. Antes de trabalho longo, fazer ensaio sem efeito externo: gerar checkpoint e preparar retomada em outra plataforma. Só marcar troca real validada se a sessão sucessora realmente leu o estado e o controle de escrita foi transferido. Não consumir nova API ou interromper trabalho real só para simular falha.
9. Iniciar a menor equipe necessária depois da preparação, quando execução fizer parte do pedido. Manter revisões independentes e testes proporcionais. Não esperar documentação perfeita para começar.

Prompt de preparação:

“Leia skills/orca-maestro/SKILL.md e prepare este projeto, preservando o que já existir. Maestro principal Opus 5.5/medium; GPT-6.2 excluído. Confirme Codex e Gemini disponíveis, incluindo alternativas por papel e pools de cota. Habilite a política de continuidade autorizada usando apenas recursos existentes; se não houver controlador real, declare modo assistido e deixe o RESUME pronto. Salve mapa, plano, inventário, registro de tarefas e checkpoint. Não contrate API, altere permissões nem comece funcionalidades do produto nesta etapa. Depois informarei o escopo do projeto.”
