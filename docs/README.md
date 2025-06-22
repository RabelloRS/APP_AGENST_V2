# Agentes de Engenharia da Propor - Sistema de Agentes Inteligentes

## 📞 Informações da Empresa

**Propor Engenharia**  
**Responsável Técnico:** Eng. Civil Rodrigo Emanuel Rabello  
**CREA-RS:** 167.175-D  
**Telefone:** 51 99164-6794  
**Localização:** Nova Petrópolis / RS  
**CNPJ:** 41.556.670/0001-76

## 🎯 MVP - Produto Mínimo Viável

O **Agentes de Engenharia da Propor** é um sistema de agentes inteligentes baseado em CrewAI, focado inicialmente na **análise e comparação de planilhas Excel** para aplicações em engenharia civil.

### 🚀 Funcionalidades do MVP

#### 📊 Análise de Planilhas Excel
- **Comparação de similaridade** entre colunas de diferentes planilhas
- **Detecção de padrões** nos dados (textuais e numéricos)
- **Validação automática** de arquivos Excel
- **Geração de relatórios** estruturados
- **Recomendações inteligentes** baseadas na análise

#### 🎯 Casos de Uso Principais
1. **Comparação de orçamentos** de diferentes fornecedores
2. **Análise de variações** em projetos de engenharia
3. **Controle de qualidade** de dados em planilhas
4. **Detecção de inconsistências** entre versões de documentos

### 🛠️ Tecnologias Utilizadas

| Componente | Tecnologia | Status |
|------------|------------|--------|
| **Framework de Agentes** | CrewAI | ✅ Implementado |
| **Interface Gráfica** | Streamlit | ✅ Implementado |
| **Processamento de Dados** | Pandas + NumPy | ✅ Implementado |
| **Análise de Similaridade** | TheFuzz + Scikit-learn | ✅ Implementado |
| **Modelo de Linguagem** | OpenAI GPT-4 | ✅ Configurado |
| **Manipulação de Excel** | OpenPyXL | ✅ Implementado |

### 📋 Pré-requisitos

- Python 3.8+
- Chave da API OpenAI configurada
- Dependências listadas em `requirements.txt`

### 🚀 Instalação e Configuração

1. **Clone o repositório:**
```bash
cd Agentes_de_Engenharia_da_Propor
```

2. **Configure o ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp env.example .env
# Edite o arquivo .env e adicione sua chave da API OpenAI
```

5. **Execute o sistema:**
```bash
streamlit run app/main.py
```

### 📖 Como Usar o MVP

#### 1. Acesse a Interface
- Abra o navegador em `http://localhost:8501`
- Verifique se a API está configurada na sidebar

#### 2. Execute uma Análise de Planilhas
1. Vá para a aba **"Execução"**
2. Selecione **"Crew de Análise de Planilhas"**
3. Faça upload de dois arquivos Excel
4. Selecione as colunas para comparação
5. Configure as opções de análise:
   - ✅ Detectar padrões nos dados
   - ✅ Gerar recomendações
   - ✅ Relatório detalhado
6. Clique em **"Executar Tarefa"**

#### 3. Analise os Resultados
- **Métricas principais**: Score médio, distribuição de similaridade
- **Recomendações**: Sugestões baseadas na análise
- **Padrões detectados**: Análise da estrutura dos dados
- **Relatório detalhado**: Download do relatório completo
- **Correspondências**: Tabela com scores de similaridade

### 🔧 Exemplo Prático

Execute o exemplo incluído para ver o sistema em ação:

```bash
python examples/excel_comparison_example.py
```

Este exemplo cria planilhas de materiais de construção e demonstra:
- Validação de arquivos
- Análise de similaridade
- Detecção de padrões
- Geração de relatórios

### 📊 Estrutura do Projeto

```
Agentes_de_Engenharia_da_Propor/
├── app/                    # Aplicação principal
│   ├── agents/          # Gerenciamento de agentes
│   ├── crews/           # Gerenciamento de equipes
│   ├── config/          # Configurações YAML
│   ├── utils/           # Ferramentas e utilitários
│   └── main.py          # Interface Streamlit
├── examples/            # Exemplos práticos
├── docs/               # Documentação
├── tests/              # Testes automatizados
└── requirements.txt    # Dependências
```

### 🎯 Roadmap - Próximas Fases

#### Fase 2: Expansão de Funcionalidades
- [ ] Integração com normas técnicas (RAG)
- [ ] Análise de imagens de patologias
- [ ] Agente especialista em normas
- [ ] Sistema de busca em documentos

#### Fase 3: Automação Avançada
- [ ] Criação dinâmica de agentes
- [ ] Integração com APIs externas
- [ ] Sistema de workflow personalizado
- [ ] Dashboard avançado

### 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 📞 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Consulte a documentação em `docs/`
- Execute os exemplos em `examples/`

---

**Desenvolvido com ❤️ para a comunidade de engenharia civil** 