"""
Gerenciamento de Tools - Configuração de Ferramentas para Agentes
"""

import streamlit as st
from pathlib import Path

def get_category_icon(category_name):
    """Retorna um ícone com base no nome da categoria."""
    icons = {
        "excel": "📈",
        "analise": "📊",
        "relatorios": "📄",
        "whatsapp": "📱",
        "gerenciamento_arquivos": "📂",
        "pesquisa": "🔍"
    }
    # Encontra o ícone correspondente (ignorando maiúsculas/minúsculas e espaços)
    key = category_name.lower().replace(" ", "_")
    return icons.get(key, "��")

def show_tools_category_selector(
    configuring_agent, tools_by_category, tools_manager, current_tools
):
    """Exibe os checkboxes de seleção de tools por categoria e retorna a lista de tools selecionadas"""
    selected_tools = []
    
    for category, tools in tools_by_category.items():
        with st.expander(f"📁 {category} ({len(tools)} tools)", expanded=False):
            for tool_name in tools:
                tool_info = tools_manager.get_tool_info(tool_name)
                if tool_info:
                    # Checkbox para cada tool
                    is_selected = st.checkbox(
                        f"✅ {tool_info['name']}",
                        value=tool_name in current_tools,
                        key=f"tool_{configuring_agent}_{tool_name}",
                        help=f"Atribuir {tool_info['name']} ao agente {configuring_agent}"
                    )

                    if is_selected:
                        selected_tools.append(tool_name)

                    # Mostrar detalhes da tool
                    st.write(f"**🔧 {tool_info['name']}**")
                    st.write(f"*{tool_info['description']}*")

                    # Mostrar detalhes da tool
                    st.write("**Detalhes:**")
                    st.write(f"**Descrição:** {tool_info['description']}")

                    if "parameters" in tool_info:
                        st.write("**Parâmetros:**")
                        for param, desc in tool_info["parameters"].items():
                            st.write(f"  - `{param}`: {desc}")

                    if "returns" in tool_info:
                        st.write(f"**Retorna:** {tool_info['returns']}")

                    if "example" in tool_info:
                        st.write("**Exemplo de Uso:**")
                        st.code(tool_info["example"], language="python")
                        
                    st.markdown("---")
    
    return selected_tools


def show_agent_tools_config(configuring_agent, agent_manager, tools_manager):
    """Exibe a interface de configuração de tools para um agente"""
    st.subheader(f"⚙️ Configurando Tools para: {configuring_agent}")
    
    # Ajuda para configuração
    with st.expander("ℹ️ Como configurar tools", expanded=False):
        st.info("""
        **O que são tools?**
        Tools são ferramentas que permitem aos agentes executar tarefas específicas.
        
        **Categorias disponíveis:**
        - **Excel**: Ferramentas para manipulação de planilhas
        - **Análise**: Ferramentas para análise de dados
        - **Relatórios**: Ferramentas para geração de relatórios
        - **WhatsApp**: Ferramentas para integração com WhatsApp
        
        **Como usar:**
        1. Selecione as tools que o agente deve ter acesso
        2. Clique em "Salvar Configuração"
        3. Use "Recriar Agente" para aplicar as mudanças
        """)

    # Obter tools atuais do agente
    current_tools = agent_manager.get_agent_tools(configuring_agent)

    # Listar todas as tools disponíveis
    tools_manager.list_available_tools()
    tools_by_category = tools_manager.get_tools_by_category()

    # Interface de seleção
    st.write("**Selecione as tools que este agente deve ter acesso:**")

    selected_tools = show_tools_category_selector(
        configuring_agent, tools_by_category, tools_manager, current_tools
    )

    # Botões de ação
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Salvar Configuração", type="primary"):
            if agent_manager.update_agent_tools(configuring_agent, selected_tools):
                st.success(f"Tools configuradas com sucesso para {configuring_agent}!")
                st.session_state.configuring_agent_tools = None
                st.rerun()
            else:
                st.error("Erro ao salvar configuração!")

    with col2:
        if st.button("❌ Cancelar"):
            st.session_state.configuring_agent_tools = None
            st.rerun()

    with col3:
        if st.button("🔄 Recarregar Original"):
            st.rerun()

    st.markdown("---")


def show_agents_tools_list(agent_manager, tools_manager):
    """Exibe a lista de agentes e suas tools"""
    st.subheader("🤖 Agentes e suas Tools")

    for agent_type in agent_manager.list_available_agent_types():
        agent_info = agent_manager.get_agent_info(agent_type) or {}
        agent_name = agent_info.get("name", agent_type)
        agent_tools = agent_manager.get_agent_tools(agent_type)

        with st.expander(f"🤖 {agent_name} ({len(agent_tools)} tools)", expanded=False):
            st.write(f"**Tipo:** {agent_type}")
            st.write(f"**Função:** {agent_info.get('role', '-')}")

            if agent_tools:
                st.write("**Tools Atribuídas:**")
                for tool_name in agent_tools:
                    tool_info = tools_manager.get_tool_info(tool_name)
                    if tool_info:
                        st.write(f"  - 🔧 {tool_info['name']} ({tool_info['category']})")
                    else:
                        st.write(f"  - ⚠️ {tool_name} (não encontrada)")
            else:
                st.write("**Tools Atribuídas:** Nenhuma")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("⚙️ Configurar Tools", key=f"config_tools_{agent_type}"):
                    st.session_state.configuring_agent_tools = agent_type
                    st.rerun()

            with col2:
                if st.button(
                    "🔄 Recriar Agente", key=f"recreate_with_tools_{agent_type}"
                ):
                    # Remover agente existente se houver
                    if agent_type in agent_manager.agents:
                        del agent_manager.agents[agent_type]

                    # Criar novo agente com tools configuradas
                    agent = agent_manager.create_agent(agent_type)
                    if agent:
                        st.success(f"Agente {agent_name} recriado com tools!")
                    else:
                        st.error(f"Erro ao recriar agente {agent_name}")


def show_tools_tab():
    """Exibe a aba de gerenciamento de tools."""
    st.header("🔧 Gerenciamento de Ferramentas (Tools)")
    st.markdown("### Visualize as ferramentas disponíveis para os agentes")
    
    with st.expander("ℹ️ Sobre Ferramentas (Tools)", expanded=False):
        st.info("""
        **O que são ferramentas?**
        Ferramentas são habilidades específicas que os agentes podem usar para executar ações, como pesquisar na web, analisar arquivos ou interagir com outras APIs.
        
        **Como funcionam:**
        1. Cada ferramenta pertence a uma categoria.
        2. Elas são atribuídas a agentes específicos para expandir suas capacidades.
        3. A atribuição é feita no arquivo de configuração `app/config/agent_tools.yaml`.
        """)

    st.markdown("---")

    tools_manager = st.session_state.tools_manager
    
    # Visão Geral
    st.subheader("📊 Visão Geral das Ferramentas")
    try:
        tools_by_category = tools_manager.get_tools_by_category()
        total_tools = sum(len(tools) for tools in tools_by_category.values())
        total_categories = len(tools_by_category)
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Ferramentas", total_tools, "Número total de ferramentas disponíveis no sistema.")
        col2.metric("Total de Categorias", total_categories, "As ferramentas são agrupadas por categorias para melhor organização.")
    except Exception as e:
        st.error(f"Não foi possível carregar as estatísticas das ferramentas: {e}")
    
    st.markdown("---")
    
    # Lista de Ferramentas por Categoria
    st.subheader("📋 Ferramentas Disponíveis por Categoria")
    try:
        if not tools_by_category:
            st.warning("Nenhuma ferramenta encontrada. Verifique o arquivo `app/config/tools.yaml`.")
        else:
            for category, tools in tools_by_category.items():
                icon = get_category_icon(category)
                with st.expander(f"{icon} **{category.replace('_', ' ').title()}** ({len(tools)} ferramentas)", expanded=True):
                    for tool_name in tools:
                        tool_info = tools_manager.get_tool_info(tool_name)
                        if tool_info:
                            st.markdown(f"**🔧 {tool_info.get('name', tool_name)}** (`{tool_name}`)")
                            st.caption(f"_{tool_info.get('description', 'Sem descrição.')}_")
                            
                            # Parâmetros
                            if "parameters" in tool_info and tool_info["parameters"]:
                                with st.container(border=True):
                                    st.markdown("**Parâmetros:**")
                                    for param, desc in tool_info["parameters"].items():
                                        st.markdown(f"- `{param}`: {desc}")
                            # Retorno
                            if "returns" in tool_info:
                                st.markdown(f"**Retorna**: `{tool_info['returns']}`")
                        else:
                            st.markdown(f"- ⚠️ `{tool_name}` (não encontrada)")
                        st.markdown("---")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os detalhes das ferramentas: {e}")

    # Configuração
    st.markdown("---")
    st.subheader("ℹ️ Informações sobre Configuração")
    st.info("As ferramentas e suas atribuições são definidas nos arquivos `tools.yaml` e `agent_tools.yaml` dentro da pasta `app/config/`.")

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📄 `tools.yaml`"):
            try:
                with open("app/config/tools.yaml", "r", encoding="utf-8") as f:
                    st.code(f.read(), language="yaml")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")
    with col2:
        with st.expander("📄 `agent_tools.yaml`"):
            try:
                with open("app/config/agent_tools.yaml", "r", encoding="utf-8") as f:
                    st.code(f.read(), language="yaml")
            except Exception as e:
                st.error(f"Erro ao ler o arquivo: {e}")
 