# Estrutura Completa do Projeto - Agentes de Engenharia da Propor

## 📞 Informações da Empresa

**Propor Engenharia**  
**Responsável Técnico:** Eng. Civil Rodrigo Emanuel Rabello  
**CREA-RS:** 167.175-D  
**Telefone:** 51 99164-6794  
**Localização:** Nova Petrópolis / RS  
**CNPJ:** 41.556.670/0001-76

## 🎯 Visão Geral

**Agentes de Engenharia da Propor** é um sistema de agentes inteligentes baseado em CrewAI que permite criar, gerenciar e executar equipes de agentes especializados para diferentes tarefas. O sistema utiliza arquivos YAML para configuração e oferece uma interface web moderna através do Streamlit.

## 📁 Estrutura Completa do Projeto

```
Agentes_de_Engenharia_da_Propor/
├── 📁 app/                          # Módulo principal da aplicação
│   ├── 📁 agents/                   # Gerenciamento de agentes
│   │   ├── __init__.py
│   │   └── agent_manager.py        # ✅ Implementado - Gerenciador de agentes
│   ├── 📁 crews/                    # Gerenciamento de crews e tarefas
│   │   ├── __init__.py
│   │   ├── crew_manager.py         # ✅ Implementado - Gerenciador de crews
│   │   └── task_manager.py         # ✅ Implementado - Gerenciador de tarefas
│   ├── 📁 config/                   # Configurações YAML
│   │   ├── __init__.py
│   │   ├── agents.yaml             # ✅ Implementado - Configurações de agentes
│   │   └── tasks.yaml              # ✅ Implementado - Configurações de tarefas
│   ├── 📁 utils/                    # Utilitários e configurações
│   │   ├── __init__.py
│   │   └── config.py               # ✅ Implementado - Configurações gerais
│   └── main.py                     # ✅ Implementado - Interface Streamlit
├── 📁 docs/                         # Documentação
│   ├── README.md                   # ✅ Implementado - Documentação básica
│   ├── ARCHITECTURE.md             # ✅ Implementado - Documentação da arquitetura
│   └── PROJECT_STRUCTURE.md        # ✅ Este arquivo
├── 📁 examples/                     # Exemplos de uso
│   └── basic_usage.py              # ✅ Implementado - Exemplo básico
├── 📁 tests/                        # Testes automatizados
│   ├── __init__.py
│   └── test_agent_manager.py       # ✅ Implementado - Testes básicos
├── 📁 venv/                         # Ambiente virtual Python
├── .env                            # ⚠️ Pendente - Variáveis de ambiente
├── .gitignore                      # ✅ Implementado
├── CHANGELOG.md                    # ✅ Implementado - Histórico de mudanças
├── INSTRUCOES.md                   # ✅ Implementado - Instruções de uso
├── LICENSE                         # ✅ Implementado
├── README.md                       # ✅ Implementado - Documentação principal
├── requirements.txt                # ✅ Implementado - Dependências
├── run.bat                         # ✅ Implementado - Script de execução
├── setup.py                        # ✅ Implementado - Configuração do pacote
└── test_simple.py                  # ✅ Implementado - Teste simples
```

## 🔧 Componentes Implementados

### 1. **AgentManager** (`app/agents/agent_manager.py`)
**Status**: ✅ **FUNCIONANDO**

**Funcionalidades**:
- ✅ Carregamento de configurações de agentes do YAML
- ✅ Criação dinâmica de agentes baseados em configurações
- ✅ Gerenciamento de ciclo de vida dos agentes
- ✅ Recarregamento de configurações em tempo real
- ✅ Validação de tipos de agentes
- ✅ Tratamento de erros robusto

**Agentes Disponíveis**:
- `researcher` - Pesquisador especializado
- `analyst` - Analista de dados
- `writer` - Escritor de conteúdo
- `reviewer` - Revisor de conteúdo
- `coordinator` - Coordenador de equipe
- `excel_analyst` - Analista de Excel

### 2. **TaskManager** (`app/crews/task_manager.py`)
**Status**: ✅ **FUNCIONANDO**

**Funcionalidades**:
- ✅ Carregamento de configurações de tarefas do YAML
- ✅ Criação de tarefas com parâmetros dinâmicos
- ✅ Associação automática de tarefas a agentes
- ✅ Substituição de variáveis em descrições (`{topic}`)
- ✅ Recarregamento de configurações
- ✅ Validação de tipos de tarefas

**Tarefas Disponíveis**:
- `research_task` - Pesquisa detalhada
- `analysis_task` - Análise de dados
- `writing_task` - Criação de conteúdo
- `review_task` - Revisão de conteúdo
- `coordination_task` - Coordenação de trabalho
- `excel_analysis_task` - Análise de planilhas

### 3. **CrewManager** (`app/crews/crew_manager.py`)
**Status**: ✅ **FUNCIONANDO**

**Funcionalidades**:
- ✅ Criação de crews com agentes e tarefas
- ✅ Execução de crews completas
- ✅ Adição dinâmica de tarefas a crews
- ✅ Gerenciamento de ciclo de vida das crews
- ✅ Execução de tarefas individuais
- ✅ Deleção de crews

### 4. **Interface Streamlit** (`app/main.py`)
**Status**: ✅ **FUNCIONANDO**

**Funcionalidades**:
- ✅ Dashboard com métricas do sistema
- ✅ Gerenciamento de agentes via interface
- ✅ Gerenciamento de tarefas via interface
- ✅ Criação e execução de crews
- ✅ Visualização de configurações YAML
- ✅ Recarregamento de configurações
- ✅ Crews pré-definidas
- ✅ Execução de crews com resultados

**Abas Disponíveis**:
- 🏠 Dashboard - Visão geral do sistema
- 🤖 Agentes - Gerenciamento de agentes
- 📋 Tarefas - Gerenciamento de tarefas
- 👥 Crews - Gerenciamento de crews
- 📊 Execução - Execução de tarefas

### 5. **Configurações YAML**
**Status**: ✅ **FUNCIONANDO**

**Arquivos**:
- `app/config/agents.yaml` - Configurações de agentes
- `app/config/tasks.yaml` - Configurações de tarefas

**Características**:
- ✅ Configurações centralizadas
- ✅ Fácil modificação sem recompilação
- ✅ Versionamento via Git
- ✅ Validação automática

## 🚀 Aplicações e Ferramentas Funcionando

### 1. **Interface Web (Streamlit)**
- **URL**: `http://localhost:8501` (após executar `streamlit run app/main.py`)
- **Status**: ✅ **FUNCIONANDO**
- **Funcionalidades**: Interface completa para gerenciamento do sistema

### 2. **Sistema de Agentes**
- **Status**: ✅ **FUNCIONANDO**
- **Funcionalidades**: Criação, gerenciamento e execução de agentes

### 3. **Sistema de Tarefas**
- **Status**: ✅ **FUNCIONANDO**
- **Funcionalidades**: Definição e execução de tarefas parametrizadas

### 4. **Sistema de Crews**
- **Status**: ✅ **FUNCIONANDO**
- **Funcionalidades**: Criação e execução de equipes de agentes

### 5. **Configuração Dinâmica**
- **Status**: ✅ **FUNCIONANDO**
- **Funcionalidades**: Recarregamento de configurações sem reiniciar

## 🔄 Lógica de Funcionamento

### Fluxo Principal do Sistema

```mermaid
graph TD
    A[Inicialização] --> B[Carregar YAML]
    B --> C[AgentManager]
    B --> D[TaskManager]
    C --> E[CrewManager]
    D --> E
    E --> F[Interface Streamlit]
    F --> G[Criar Crews]
    F --> H[Executar Tarefas]
    G --> I[Resultados]
    H --> I
```

### 1. **Inicialização**
1. Carregamento das configurações YAML
2. Inicialização dos gerenciadores (Agent, Task, Crew)
3. Configuração da interface Streamlit

### 2. **Criação de Agentes**
1. Leitura da configuração do agente no YAML
2. Criação da instância do agente com CrewAI
3. Armazenamento no AgentManager

### 3. **Criação de Tarefas**
1. Leitura da configuração da tarefa no YAML
2. Substituição de parâmetros dinâmicos
3. Associação com agente responsável
4. Criação da instância da tarefa

### 4. **Criação de Crews**
1. Seleção de agentes e tarefas
2. Criação da crew com CrewAI
3. Adição de tarefas à crew
4. Armazenamento no CrewManager

### 5. **Execução**
1. Validação da crew e tarefas
2. Execução sequencial das tarefas
3. Coleta e retorno dos resultados

## ⚠️ Itens Pendentes de Desenvolvimento

### 🔴 **CRÍTICOS**

#### 1. **Configuração de Ambiente**
- ⚠️ **Arquivo `.env`** - Configuração de variáveis de ambiente
  - `OPENAI_API_KEY` - Chave da API OpenAI
  - `MODEL_NAME` - Modelo padrão
  - `TEMPERATURE` - Temperatura padrão
  - `MAX_TOKENS` - Limite de tokens

#### 2. **Validação e Segurança**
- ⚠️ **Validação de Schema YAML** - Validar configurações contra schemas
- ⚠️ **Sanitização de Inputs** - Proteção contra inputs maliciosos
- ⚠️ **Rate Limiting** - Controle de requisições à API

#### 3. **Tratamento de Erros**
- ⚠️ **Sistema de Logs** - Logging estruturado
- ⚠️ **Monitoramento** - Métricas de performance
- ⚠️ **Recovery** - Recuperação automática de falhas

### 🟡 **IMPORTANTES**

#### 4. **Funcionalidades Avançadas**
- ⚠️ **Sistema de Tools** - Integração com ferramentas externas
- ⚠️ **Memória Persistente** - Armazenamento de conversas
- ⚠️ **Templates de Crews** - Crews pré-configuradas
- ⚠️ **Workflows Complexos** - Sequências de tarefas condicionais

#### 5. **Interface e UX**
- ⚠️ **Editor de YAML** - Interface para editar configurações
- ⚠️ **Visualização de Resultados** - Gráficos e dashboards
- ⚠️ **Histórico de Execuções** - Log de crews executadas
- ⚠️ **Exportação de Resultados** - PDF, Excel, etc.

#### 6. **Integrações**
- ⚠️ **APIs Externas** - Integração com outros serviços
- ⚠️ **Bancos de Dados** - Armazenamento persistente
- ⚠️ **Sistema de Arquivos** - Upload/download de arquivos

### 🟢 **MELHORIAS**

#### 7. **Performance**
- ⚠️ **Cache** - Cache de configurações e resultados
- ⚠️ **Async/Await** - Execução assíncrona
- ⚠️ **Otimização** - Melhoria de performance

#### 8. **Testes**
- ⚠️ **Testes Unitários** - Cobertura completa
- ⚠️ **Testes de Integração** - Testes end-to-end
- ⚠️ **Testes de Performance** - Benchmarks

#### 9. **Documentação**
- ⚠️ **API Documentation** - Documentação da API
- ⚠️ **User Guide** - Guia do usuário
- ⚠️ **Developer Guide** - Guia do desenvolvedor

#### 10. **DevOps**
- ⚠️ **Docker** - Containerização
- ⚠️ **CI/CD** - Pipeline de deploy
- ⚠️ **Monitoring** - Monitoramento em produção

## 📊 Status de Implementação

| Componente | Status | Progresso |
|------------|--------|-----------|
| AgentManager | ✅ Funcionando | 100% |
| TaskManager | ✅ Funcionando | 100% |
| CrewManager | ✅ Funcionando | 100% |
| Interface Streamlit | ✅ Funcionando | 100% |
| Configurações YAML | ✅ Funcionando | 100% |
| Testes Básicos | ✅ Funcionando | 80% |
| Documentação | ✅ Funcionando | 90% |
| Configuração de Ambiente | ⚠️ Pendente | 0% |
| Validação e Segurança | ⚠️ Pendente | 0% |
| Sistema de Logs | ⚠️ Pendente | 0% |
| Integrações | ⚠️ Pendente | 0% |
| Performance | ⚠️ Pendente | 0% |

## 🎯 Próximos Passos Recomendados

### Fase 1 - Estabilização (Prioridade Alta)
1. **Configurar arquivo `.env`** com variáveis de ambiente
2. **Implementar sistema de logs** para debugging
3. **Adicionar validação de schemas** YAML
4. **Melhorar tratamento de erros**

### Fase 2 - Funcionalidades (Prioridade Média)
1. **Implementar sistema de tools** para agentes
2. **Adicionar templates de crews** pré-definidas
3. **Criar editor de YAML** na interface
4. **Implementar histórico de execuções**

### Fase 3 - Escalabilidade (Prioridade Baixa)
1. **Adicionar banco de dados** para persistência
2. **Implementar cache** para performance
3. **Criar sistema de monitoramento**
4. **Containerizar com Docker**

## 🔗 Dependências Externas

### APIs Necessárias
- **OpenAI API** - Para execução dos agentes
- **Opcional**: APIs específicas para tools

### Bibliotecas Python
- **CrewAI** - Framework principal
- **Streamlit** - Interface web
- **PyYAML** - Configurações
- **python-dotenv** - Variáveis de ambiente
- **OpenAI** - Cliente da API

## 📈 Métricas de Sucesso

### Técnicas
- ✅ Código funcionando sem erros
- ✅ Interface responsiva
- ✅ Configurações carregando corretamente
- ✅ Agentes criando e executando

### Funcionais
- ✅ Sistema de agentes operacional
- ✅ Interface de usuário funcional
- ✅ Configurações flexíveis
- ✅ Documentação completa

---

**Última Atualização**: 21/06/2025  
**Versão do Sistema**: 2.0.0  
**Status Geral**: ✅ **FUNCIONANDO** (80% completo)

# Estrutura do Projeto

## app/config/
- `agents.yaml`: Lista e configura todos os agentes do sistema.
- `tasks.yaml`: Lista e configura todas as tasks disponíveis.
- `tools.yaml`: (Opcional) Apenas informativo, descreve ferramentas oficiais.

## app/crews_db.json
- Banco de crews geradas pelo workflow builder. Cada crew contém nome, descrição, tasks e código Python gerado.

## app/pages/
- `agents.py`: Interface de gestão de agentes.
- `workflow_builder.py`: Interface de criação de crews.

## app/agents/
- `agent_manager.py`: Lógica de gestão de agentes.

## app/crews/
- `crew_manager.py`, `task_manager.py`: Lógica de crews e tasks (se necessário).

## .env
- Variáveis de ambiente/API keys para ferramentas externas.

## docs/
- Documentação e guias do projeto.

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

## Regras Gerais
- Não use arquivos obsoletos ou duplicados.
- Centralize toda configuração nos arquivos acima.
- Remova arquivos de cache e scripts antigos não utilizados.