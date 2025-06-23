# APP_AGENTES - Sistema de Agentes Inteligentes

Um sistema de agentes inteligentes construído com CrewAI e Streamlit para criar, gerenciar e executar tarefas complexas através de múltiplos agentes especializados.

## 🚀 Características

- **CrewAI Integration**: Sistema de agentes colaborativos
- **Streamlit Interface**: Interface web moderna e responsiva
- **Multi-Agent System**: Agentes especializados para diferentes tarefas
- **Environment Management**: Configuração segura de chaves de API
- **Best Practices**: Estrutura organizada seguindo padrões Python

## 📋 Pré-requisitos

- Python 3.12+
- Git
- Conta na OpenAI (para chaves de API)

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio-github>
cd APP_AGENTES
```

### 2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o template
copy env_template.txt .env

# Edite o arquivo .env com suas chaves de API
# OPENAI_API_KEY=sua_chave_aqui
```

## 🚀 Como usar

### Executar a aplicação Streamlit
```bash
streamlit run app/main.py
```

### Executar testes
```bash
pytest tests/
```

### Formatar código
```bash
black .
```

## 📁 Estrutura do Projeto

```
APP_AGENTES/
├── app/                    # Aplicação principal
│   ├── main.py            # Entry point do Streamlit
│   ├── agents/            # Definições dos agentes
│   ├── crews/             # Configurações das crews
│   └── utils/             # Utilitários
├── tests/                 # Testes unitários
├── docs/                  # Documentação
├── requirements.txt       # Dependências Python
├── .gitignore            # Arquivos ignorados pelo Git
├── env_template.txt      # Template de variáveis de ambiente
└── README.md             # Este arquivo
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `env_template.txt`:

- `OPENAI_API_KEY`: Sua chave da API OpenAI
- `ANTHROPIC_API_KEY`: Sua chave da API Anthropic (opcional)
- `DEFAULT_MODEL`: Modelo padrão (ex: gpt-4)
- `DEFAULT_TEMPERATURE`: Temperatura para geração de texto

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas, abra uma issue no GitHub.

## 🔄 Atualizações

Para atualizar o projeto:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

# Plataforma de Gestão de Agentes, Tasks e Crews para Engenharia

## Estrutura dos Arquivos

- `app/config/agents.yaml`: Definição dos agentes, categorias, papéis e ferramentas.
- `app/config/tasks.yaml`: Definição das tasks disponíveis.
- `app/data/crews_database.db`: Banco de dados principal das crews (persistência única).
- `app/config/tools.yaml`: (Opcional) Descrição informativa das ferramentas.
- `.env`: Variáveis de ambiente/API keys necessárias para ferramentas externas.

## Fluxo de Gestão

- **Agentes:** Gerenciados via `agents.yaml` e interface `agents.py`.
- **Tasks:** Gerenciadas via `tasks.yaml`.
- **Crews:** Criadas, salvas, editadas e listadas exclusivamente via banco de dados SQLite (`app/data/crews_database.db`).
- **Ferramentas:** Apenas as oficiais do CrewAI, configuradas via `.env`.

## Recomendações

- Sempre edite agentes, tasks e crews pelas interfaces ou diretamente nos arquivos de configuração YAML.
- Mantenha a documentação enxuta e centralizada.
- Remova arquivos obsoletos para evitar confusão.

## Ajuda

Consulte `docs/PROJECT_STRUCTURE.md` para detalhes sobre cada arquivo e boas práticas de manutenção.

## 🔄 Persistência de Crews

A partir da versão 2.0.0, **todas as informações de crews são armazenadas exclusivamente no banco de dados SQLite (`app/data/crews_database.db`)**. Não há mais leitura ou escrita de crews em arquivos JSON para persistência principal.

- Criação, edição, exclusão e listagem de crews são feitas via banco de dados.
- O arquivo `crews_db_resumido.json` pode ser gerado apenas para exportação/visualização, mas não é fonte de verdade.
- Para exportar um resumo das crews para JSON, utilize a função utilitária disponível no sistema.

## 🗂️ Estrutura Recomendada

```text
app/
├── data/
│   └── crews_database.db   # Banco de dados principal das crews
├── crews/
│   └── crew_manager.py     # Toda lógica de manipulação de crews
```

## 🛠️ Migração

Se você utilizava arquivos JSON para crews, basta rodar o sistema normalmente: crews existentes serão migradas para o banco na primeira execução. Após a migração, remova arquivos JSON antigos para evitar confusão.