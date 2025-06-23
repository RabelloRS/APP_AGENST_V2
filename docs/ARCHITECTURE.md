# Arquitetura do Sistema de Agentes

## Visão Geral

O sistema foi refatorado para seguir as melhores práticas do CrewAI, utilizando arquivos YAML para configuração de agentes e tarefas. Isso torna o sistema mais organizado, escalável e fácil de manter.

## Estrutura de Arquivos

```
app/
├── config/
│   ├── agents.yaml      # Configurações dos agentes
│   └── tasks.yaml       # Configurações das tarefas
├── agents/
│   └── agent_manager.py # Gerenciador de agentes
├── crews/
│   ├── task_manager.py  # Gerenciador de tarefas
│   └── crew_manager.py  # Gerenciador de crews
└── main.py              # Interface Streamlit
```

## Componentes Principais

### 1. AgentManager
- **Responsabilidade**: Gerenciar agentes do sistema
- **Funcionalidades**:
  - Carregar configurações de agentes do YAML
  - Criar instâncias de agentes
  - Gerenciar ciclo de vida dos agentes
  - Recarregar configurações dinamicamente

### 2. TaskManager
- **Responsabilidade**: Gerenciar tarefas do sistema
- **Funcionalidades**:
  - Carregar configurações de tarefas do YAML
  - Criar tarefas com parâmetros dinâmicos
  - Associar tarefas a agentes específicos
  - Recarregar configurações dinamicamente

### 3. CrewManager
- **Responsabilidade**: Gerenciar crews (equipes de agentes)
- **Funcionalidades**:
  - Criar crews com agentes e tarefas
  - Executar crews completas
  - Gerenciar ciclo de vida das crews
  - Coordenar execução de tarefas

## Configuração YAML

### agents.yaml
```yaml
researcher:
  name: "Pesquisador"
  role: "Pesquisador especializado"
  goal: "Realizar pesquisas detalhadas e coleta de informações"
  backstory: "Especialista em pesquisa com vasta experiência"
  tools: []
  verbose: true
  allow_delegation: false
```

### tasks.yaml
```yaml
research_task:
  description: "Realizar pesquisa detalhada sobre {topic}"
  expected_output: "Relatório completo com informações coletadas"
  agent: "researcher"
  context: "Pesquisa inicial para coleta de informações"
```

## Vantagens da Nova Arquitetura

### 1. Separação de Responsabilidades
- Configuração separada da lógica de negócio
- Fácil manutenção e atualização
- Código mais limpo e organizado

### 2. Flexibilidade
- Adicionar novos agentes sem recompilar
- Modificar configurações em tempo de execução
- Reutilização de configurações

### 3. Escalabilidade
- Fácil adição de novos tipos de agentes
- Configuração de tarefas complexas
- Suporte a múltiplos workflows

### 4. Manutenibilidade
- Configurações centralizadas
- Versionamento de configurações
- Debugging mais fácil

## Fluxo de Trabalho

1. **Configuração**: Definir agentes e tarefas em YAML
2. **Inicialização**: Carregar configurações nos gerenciadores
3. **Criação**: Criar agentes e tarefas baseados nas configurações
4. **Composição**: Montar crews com agentes e tarefas
5. **Execução**: Executar crews completas ou tarefas individuais

## Exemplo de Uso

```python
# Inicializar gerenciadores
agent_manager = AgentManager()
task_manager = TaskManager()
crew_manager = CrewManager(agent_manager, task_manager)

# Criar crew com tarefas
crew = crew_manager.create_crew_with_tasks(
    name="Crew de Pesquisa",
    agent_types=["researcher", "analyst", "writer"],
    task_types=["research_task", "analysis_task", "writing_task"],
    topic="inteligência artificial"
)

# Executar crew
result = crew_manager.execute_crew("Crew de Pesquisa")
```

## Persistência de Crews

A partir da refatoração, **todas as informações de crews são armazenadas exclusivamente no banco de dados SQLite (`app/data/crews_database.db`)**. Não há mais leitura ou escrita de crews em arquivos JSON para persistência principal.

- Criação, edição, exclusão e listagem de crews são feitas via banco de dados.
- O arquivo `crews_db_resumido.json` pode ser gerado apenas para exportação/visualização, mas não é fonte de verdade.
- Para exportar um resumo das crews para JSON, utilize a função utilitária disponível no sistema.

## Estrutura Recomendada

```text
app/
├── data/
│   └── crews_database.db   # Banco de dados principal das crews
├── crews/
│   └── crew_manager.py     # Toda lógica de manipulação de crews
```

## Migração

Se você utilizava arquivos JSON para crews, basta rodar o sistema normalmente: crews existentes serão migradas para o banco na primeira execução. Após a migração, remova arquivos JSON antigos para evitar confusão.

## Melhorias Futuras

1. **Validação de Schema**: Validar YAML contra schemas
2. **Configuração Dinâmica**: Interface para editar YAML
3. **Templates**: Templates de crews pré-definidas
4. **Monitoramento**: Logs e métricas de execução
5. **Cache**: Cache de configurações para performance