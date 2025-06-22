# 🚀 Instruções de Uso - APP_AGENTES

## ✅ Setup Concluído!

O projeto foi configurado com sucesso! Aqui está o que foi criado:

### 📁 Estrutura do Projeto
```
APP_AGENTES/
├── app/                    # Aplicação principal
│   ├── main.py            # Interface Streamlit
│   ├── agents/            # Gerenciador de agentes
│   ├── crews/             # Gerenciador de crews
│   └── utils/             # Utilitários
├── tests/                 # Testes unitários
├── docs/                  # Documentação
├── venv/                  # Ambiente virtual Python
├── requirements.txt       # Dependências
├── .env                   # Configurações (você precisa editar)
├── run.bat               # Script para executar (Windows)
└── README.md             # Documentação principal
```

### 🔧 Próximos Passos

#### 1. Configurar Chaves de API
Edite o arquivo `.env` e adicione suas chaves de API:

```env
OPENAI_API_KEY=sua_chave_openai_aqui
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
```

**Como obter as chaves:**
- **OpenAI**: Acesse https://platform.openai.com/api-keys
- **Anthropic**: Acesse https://console.anthropic.com/

#### 2. Executar a Aplicação

**Opção 1 - Script Automático (Recomendado):**
```bash
# Windows
run.bat
```

**Opção 2 - Manual:**
```bash
# Ativar ambiente virtual
venv\Scripts\activate

# Executar aplicação
streamlit run app/main.py
```

#### 3. Acessar a Interface
A aplicação será aberta automaticamente em: **http://localhost:8501**

### 🎯 Funcionalidades Disponíveis

1. **Dashboard**: Visão geral do sistema
2. **Agentes**: Gerenciar agentes especializados
3. **Crews**: Criar e gerenciar equipes de agentes
4. **Execução**: Executar tarefas com as crews

### 🔍 Testando o Sistema

1. Abra a aplicação no navegador
2. Verifique se a API está configurada (sidebar)
3. Teste a criação de agentes
4. Crie uma crew com múltiplos agentes
5. Execute uma tarefa de exemplo

### 🛠️ Desenvolvimento

**Executar testes:**
```bash
venv\Scripts\activate
pytest tests/
```

**Formatar código:**
```bash
venv\Scripts\activate
black .
```

**Verificar qualidade:**
```bash
venv\Scripts\activate
flake8 .
```

### 📚 Recursos Adicionais

- **Documentação**: Veja `docs/README.md`
- **Exemplos**: Consulte o código em `app/`
- **Configurações**: Edite `app/utils/config.py`

### 🆘 Suporte

Se encontrar problemas:

1. Verifique se o Python 3.12+ está instalado
2. Confirme se as chaves de API estão corretas
3. Verifique se o ambiente virtual está ativo
4. Consulte os logs de erro no terminal

### 🎉 Pronto para Usar!

O sistema está configurado e pronto para criar agentes inteligentes com CrewAI e Streamlit!

---

**Dica**: Mantenha o arquivo `.env` seguro e nunca o compartilhe no GitHub. 