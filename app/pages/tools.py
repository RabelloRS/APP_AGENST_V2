"""
🔧 Gerenciamento de Ferramentas (Tools)
Página padronizada conforme Agentes e Tasks
"""

import streamlit as st
from pathlib import Path
import math


def get_category_icon(category_name):
    icons = {
        "excel": "📈",
        "analise": "📊",
        "relatorios": "📄",
        "whatsapp": "📱",
        "gerenciamento_arquivos": "📂",
        "pesquisa": "🔍",
    }
    key = category_name.lower().replace(" ", "_")
    return icons.get(key, "🔧")


def show_tools_tab():
    st.header("🔧 Ferramentas Oficiais CrewAI")
    st.markdown("### Visualize e consulte as ferramentas disponíveis para os agentes")

    with st.expander("ℹ️ O que são ferramentas?", expanded=False):
        st.info(
            """
            **Ferramentas (Tools)** são habilidades específicas que os agentes podem usar para executar ações, como pesquisar na web, analisar arquivos ou interagir com APIs externas.\n\n
            - Cada ferramenta pertence a uma categoria (ex: Pesquisa, Excel, WhatsApp).
            - As ferramentas disponíveis são definidas em `app/config/tools.yaml`.
            - Atribuição de ferramentas aos agentes é feita em `agents.yaml`.
            """
        )

    st.markdown("---")

    tools_manager = st.session_state.tools_manager

    # Visão Geral
    st.subheader("📊 Visão Geral das Ferramentas")
    try:
        tools_by_category = tools_manager.get_tools_by_category()
        total_tools = sum(len(tools) for tools in tools_by_category.values())
        total_categories = len(tools_by_category)
        col1, col2 = st.columns(2)
        col1.metric("Total de Ferramentas", total_tools)
        col2.metric("Total de Categorias", total_categories)
    except Exception as e:
        st.error(f"Não foi possível carregar as estatísticas das ferramentas: {e}")

    st.markdown("---")

    # Lista de Categorias em 4 colunas, ferramentas em 1 coluna
    st.subheader("📋 Ferramentas Disponíveis por Categoria")
    try:
        if not tools_by_category:
            st.warning("Nenhuma ferramenta encontrada. Verifique o arquivo `app/config/tools.yaml`.")
        else:
            categories = list(tools_by_category.items())
            n_cols = 4
            n_rows = math.ceil(len(categories) / n_cols)
            cols = st.columns(n_cols)
            for idx, (category, tools) in enumerate(categories):
                col = cols[idx % n_cols]
                icon = get_category_icon(category)
                with col:
                    with st.expander(f"{icon} {category.replace('_', ' ').title()} ({len(tools)} ferramentas)", expanded=False):
                        for tool_name in tools:
                            tool_info = tools_manager.get_tool_info(tool_name)
                            if tool_info:
                                st.markdown(f"**🔧 {tool_info.get('name', tool_name)}** (`{tool_name}`)")
                                st.caption(f"_{tool_info.get('description', 'Sem descrição.')}_")
                                if "parameters" in tool_info and tool_info["parameters"]:
                                    st.markdown("**Parâmetros:**")
                                    for param, desc in tool_info["parameters"].items():
                                        st.markdown(f"- `{param}`: {desc}")
                                if "returns" in tool_info:
                                    st.markdown(f"**Retorna**: `{tool_info['returns']}`")
                                if "example" in tool_info:
                                    st.markdown("**Exemplo de Uso:**")
                                    st.code(tool_info["example"], language="python")
                                # Observação sobre API
                                api_env = tool_info.get('api_env')
                                if api_env:
                                    st.info(f"🔑 Necessita API: `{api_env}` no .env")
                                else:
                                    st.caption("Não requer API externa.")
                            else:
                                st.markdown(f"- ⚠️ `{tool_name}` (não encontrada)")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os detalhes das ferramentas: {e}")

    st.markdown("---")
    st.subheader("ℹ️ Visualizar Configuração YAML")
    col1 = st.columns(1)[0]
    with col1:
        with st.expander("📄 `tools.yaml` (informativo)", expanded=False):
            try:
                with open("app/config/tools.yaml", "r", encoding="utf-8") as f:
                    st.code(f.read(), language="yaml")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")


# Para integração com o sistema de navegação:
page = {
    "title": "Tools",
    "icon": "🔧",
    "function": show_tools_tab,
}

# Dica para navegação lateral retraída:
# No arquivo principal de navegação Streamlit, use:
# st.navigation(pages, position="sidebar", expanded=False)
# Isso garante que a barra lateral carregue retraída por padrão.
