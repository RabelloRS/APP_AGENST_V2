import streamlit as st

def show_about():
    """Página Sobre o Sistema"""
    st.set_page_config(page_title="Sobre o Sistema", page_icon="ℹ️", layout="centered")
    st.title("ℹ️ Sobre o Sistema de Agentes de Engenharia")
    st.markdown("""
Este sistema foi desenvolvido para orquestrar agentes inteligentes especializados em engenharia civil, utilizando CrewAI e Streamlit.

**Principais Funcionalidades:**
- Gerenciamento de agentes, tarefas, ferramentas e crews
- Construtor visual de workflows
- Execução e avaliação de crews
- Integração com WhatsApp
- Interface amigável e personalizável

**Documentação:**
- [README do Projeto](../../README.md)
- [Guia de Uso do WhatsApp](../../docs/WHATSAPP_GUIDE.md)
- [Resumo de Implementação](../../RESUMO_IMPLEMENTACAO.md)
- [Roadmap](../../docs/ROADMAP.md)

**Contato:**
- Propor Engenharia
- Eng. Civil Rodrigo Emanuel Rabello
- CREA-RS 167.175-D
- 📱 51 99164-6794
- 📍 Nova Petrópolis / RS
- 🏢 CNPJ: 41.556.670/0001-76

**Repositório:**
- [GitHub](https://github.com/rodrigorabello/APP_AGENST_V2)

---
*Desenvolvido com CrewAI, Streamlit e muito café ☕*
    """) 