import streamlit as st
import os

HELP_DIR = os.path.join(os.path.dirname(__file__), "help")

# Nomes amigáveis para arquivos de ajuda
HELP_TITLES = {
    "crewai_tools_explorer.html": "Explorador de Ferramentas CrewAI",
    "crewai_agent_task.html": "CrewAI: Orquestração de Agentes de IA",
    "crewai_tools_v2.html": "CrewAI Tools v2 (Novidades)",
    "crewai_v3.html": "CrewAI v3 (Visão Geral)",
    "ferramentas_api_keys.html": "🔑 Ferramentas e Chaves de API - Guia Completo",
}


def list_html_files():
    return [f for f in os.listdir(HELP_DIR) if f.endswith(".html")]


def read_html_file(filename):
    with open(os.path.join(HELP_DIR, filename), "r", encoding="utf-8") as f:
        return f.read()


def main():
    st.title("Documentação de Ajuda")
    with st.container():
        html_files = list_html_files()
        if not html_files:
            st.info("Nenhum documento de ajuda encontrado.")
            return
        # Exibir nomes amigáveis se disponíveis
        options = [HELP_TITLES.get(f, f) for f in html_files]
        # Seleção no topo, como em Gerenciamento
        selected_label = st.selectbox("Selecione um documento de ajuda:", options, key="help_select_top")
        selected = html_files[options.index(selected_label)]
        html_content = read_html_file(selected)
        st.components.v1.html(html_content, height=900, scrolling=True)


if __name__ == "__main__":
    main()
