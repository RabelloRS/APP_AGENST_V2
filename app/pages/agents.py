"""
Gerenciamento de Agentes - Criação e Configuração de Agentes Inteligentes
"""

import streamlit as st

def show_agents_tab():
    """Exibe a aba de gerenciamento de agentes."""
    st.header("🤖 Gerenciamento de Agentes")
    st.markdown("### Crie, configure e gerencie seus agentes inteligentes")
    
    with st.expander("ℹ️ Sobre Agentes Inteligentes", expanded=False):
        st.info("""
        **O que são agentes?**
        Agentes são entidades inteligentes que executam tarefas específicas usando IA, equipados com ferramentas e um contexto (história) para orientar suas ações.

        **Como funcionam:**
        1. **Função (Role)**: Define a especialidade do agente (ex: "Analista de Dados").
        2. **Objetivo (Goal)**: Descreve a meta principal que o agente deve alcançar.
        3. **História (Backstory)**: Fornece o contexto e a personalidade do agente.
        4. **Ferramentas (Tools)**: Habilidades específicas que o agente pode usar.
        """)

    st.markdown("---")

    agent_manager = st.session_state.agent_manager
    tools_manager = st.session_state.tools_manager

    # Seção de Visão Geral
    st.subheader("📊 Visão Geral")
    try:
        available_agents = agent_manager.list_available_agent_types()
        agents_with_tools = sum(1 for agent_type in available_agents if agent_manager.get_agent_tools(agent_type))
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Agentes", len(available_agents), "Número total de agentes configurados.")
        col2.metric("Agentes com Ferramentas", agents_with_tools, "Agentes que possuem uma ou mais ferramentas atribuídas.")
    except Exception as e:
        st.error(f"Não foi possível carregar as estatísticas dos agentes: {e}")

    st.markdown("---")

    # Lista de Agentes Disponíveis
    st.subheader("📋 Agentes Disponíveis")
    try:
        if not available_agents:
            st.warning("Nenhum agente encontrado. Verifique o arquivo `app/config/agents.yaml`.")
        else:
            for agent_type in available_agents:
                info = agent_manager.get_agent_info(agent_type) or {}
                
                with st.expander(f"🤖 **{info.get('name', agent_type)}** (`{agent_type}`)", expanded=False):
                    st.markdown(f"**Função**: {info.get('role', '*Não definida*')}")
                    st.markdown(f"**Objetivo**: {info.get('goal', '*Não definido*')}")
                    st.markdown(f"**História**: {info.get('backstory', '*Não definida*')}")
                    
                    st.markdown("---")
                    
                    # Opções e Ferramentas
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Opções:**")
                        st.checkbox("Modo Verbose", value=info.get('verbose', False), key=f"verbose_{agent_type}", disabled=True)
                        st.checkbox("Permitir Delegação", value=info.get('allow_delegation', False), key=f"delegation_{agent_type}", disabled=True)

                    with col2:
                        st.markdown("**Ferramentas Atribuídas:**")
                        agent_tools = agent_manager.get_agent_tools(agent_type)
                        if not agent_tools:
                            st.info("Nenhuma ferramenta atribuída.")
                        else:
                            for tool_name in agent_tools:
                                tool_info = tools_manager.get_tool_info(tool_name)
                                if tool_info:
                                    st.success(f"✅ {tool_info.get('name', tool_name)}")
                                else:
                                    st.error(f"❌ {tool_name} (não encontrada)")
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os detalhes dos agentes: {e}")

    # Informações sobre configuração
    st.markdown("---")
    st.subheader("ℹ️ Informações sobre Configuração")
    
    st.info("Os agentes são configurados no arquivo `app/config/agents.yaml`. Para editar, adicione as alterações no arquivo e recarregue a aplicação.")
    
    with st.expander("📄 Visualizar Configuração Atual (`agents.yaml`)"):
        try:
            with open("app/config/agents.yaml", "r", encoding="utf-8") as f:
                st.code(f.read(), language="yaml")
        except Exception as e:
            st.error(f"Erro ao ler arquivo de configuração: {e}")

    # Exemplos de agentes
    st.markdown("---")
    st.subheader("💡 Exemplos de Agentes")
    
    examples = [
        {
            "name": "Researcher",
            "role": "Pesquisador",
            "goal": "Encontrar informações precisas e relevantes",
            "backstory": "Especialista em pesquisa com vasta experiência em análise de dados"
        },
        {
            "name": "Analyst",
            "role": "Analista de Dados",
            "goal": "Analisar dados e gerar insights valiosos",
            "backstory": "Analista experiente com conhecimento em estatística e visualização"
        },
        {
            "name": "Writer",
            "role": "Escritor",
            "goal": "Criar conteúdo claro e bem estruturado",
            "backstory": "Escritor técnico especializado em relatórios e documentação"
        }
    ]
    
    for example in examples:
        with st.expander(f"🤖 {example['name']}", expanded=False):
            st.write(f"**Função:** {example['role']}")
            st.write(f"**Objetivo:** {example['goal']}")
            st.write(f"**História:** {example['backstory']}") 