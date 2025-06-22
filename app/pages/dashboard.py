"""
Dashboard Principal da Aplicação
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path

def show_config_files():
    """Exibe o conteúdo dos arquivos de configuração em abas."""
    st.subheader("📄 Conteúdo dos Arquivos de Configuração")
    
    tabs = st.tabs(["🤖 Agentes", "📋 Tarefas", "🔧 Ferramentas", "👥 Crews"])
    config_files = ["agents.yaml", "tasks.yaml", "tools.yaml", "crews.yaml"]
    
    for tab, file in zip(tabs, config_files):
        with tab:
            try:
                with open(f"app/config/{file}", "r", encoding="utf-8") as f:
                    st.code(f.read(), language="yaml")
            except Exception as e:
                st.error(f"❌ Erro ao ler o arquivo {file}: {e}")

def show_dashboard():
    """Exibe o dashboard principal da aplicação."""
    st.header("📊 Dashboard Principal")
    st.markdown("### Visão geral do ecossistema de agentes inteligentes")

    st.markdown("---")
    
    # Gerentes de estado
    agent_manager = st.session_state.agent_manager
    task_manager = st.session_state.task_manager
    tools_manager = st.session_state.tools_manager
    crew_manager = st.session_state.crew_manager

    # Métricas principais
    st.subheader("📈 Métricas Chave")
    try:
        total_agents = len(agent_manager.list_available_agent_types())
        total_tasks = len(task_manager.list_available_task_types())
        total_tools = len(tools_manager.list_all_tools())
        total_crews = len(crew_manager.list_crew_names())

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🤖 Agentes", total_agents, help="Total de agentes configurados")
        col2.metric("📋 Tarefas", total_tasks, help="Total de tipos de tarefas definidos")
        col3.metric("🔧 Ferramentas", total_tools, help="Total de ferramentas disponíveis")
        col4.metric("👥 Crews", total_crews, help="Total de equipes (crews) prontas para execução")

    except Exception as e:
        st.error(f"Não foi possível carregar as métricas: {e}")

    st.markdown("---")

    # Estatísticas do Sistema
    st.subheader("📊 Estatísticas do Sistema")
    
    try:
        # Buscar estatísticas do banco de dados
        stats = st.session_state.crew_manager.db_manager.get_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total de Execuções",
                value=stats['total_executions'],
                help="Número total de execuções realizadas"
            )
        
        with col2:
            st.metric(
                label="Execuções Bem-sucedidas",
                value=stats['successful_executions'],
                help="Execuções que foram concluídas com sucesso"
            )
        
        with col3:
            st.metric(
                label="Taxa de Sucesso",
                value=f"{stats['success_rate']:.1f}%",
                help="Percentual de execuções bem-sucedidas"
            )
        
        with col4:
            st.metric(
                label="Crews Configuradas",
                value=stats['total_crews'],
                help="Número de crews configuradas no sistema"
            )
        
        # Crew mais executada
        if stats['most_executed_crew']:
            st.info(f"🏆 **Crew mais executada:** {stats['most_executed_crew']}")
        
    except Exception as e:
        st.warning(f"Não foi possível carregar as estatísticas: {e}")
    
    st.markdown("---")

    # Gráficos de distribuição
    st.subheader("📊 Distribuição de Recursos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Ferramentas por Categoria**")
        try:
            tools_by_category = tools_manager.get_tools_by_category()
            if tools_by_category:
                category_counts = {cat.replace('_', ' ').title(): len(tools) for cat, tools in tools_by_category.items()}
                chart_data = pd.DataFrame.from_dict(category_counts, orient='index', columns=['Quantidade'])
                st.bar_chart(chart_data)
            else:
                st.info("Nenhuma categoria de ferramenta encontrada.")
        except Exception as e:
            st.warning(f"Não foi possível gerar o gráfico de ferramentas: {e}")

    with col2:
        st.markdown("**Agentes por Atribuição de Ferramentas**")
        try:
            available_agents = agent_manager.list_available_agent_types()
            agents_with_tools = sum(1 for agent in available_agents if agent_manager.get_agent_tools(agent))
            agents_without_tools = len(available_agents) - agents_with_tools
            
            if available_agents:
                data = {
                    "Com Ferramentas": agents_with_tools,
                    "Sem Ferramentas": agents_without_tools
                }
                chart_data = pd.DataFrame(pd.Series(data), columns=['Quantidade'])
                st.bar_chart(chart_data)
            else:
                st.info("Nenhum agente encontrado.")
        except Exception as e:
            st.warning(f"Não foi possível gerar o gráfico de agentes: {e}")
            
    st.markdown("---")
    
    # Atividade Recente
    st.subheader("📜 Atividade Recente (Últimas 5 Execuções)")
    if "execution_history" not in st.session_state or not st.session_state.execution_history:
        st.info("Nenhuma execução foi registrada ainda.")
    else:
        history_df = pd.DataFrame(st.session_state.execution_history).tail(5).sort_index(ascending=False)
        st.dataframe(
            history_df[["Crew", "Tópico", "Início", "Duração"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Crew": st.column_config.TextColumn("Equipe"),
                "Tópico": st.column_config.TextColumn("Tópico/Instrução"),
                "Início": st.column_config.DatetimeColumn("Início", format="DD/MM/YYYY HH:mm"),
                "Duração": st.column_config.TextColumn("Duração")
            }
        )

    st.markdown("---")
    st.info("""
    **Próximos Passos:**
    - **🤖 Agentes**: Configure seus agentes.
    - **🔧 Ferramentas**: Verifique as ferramentas disponíveis.
    - **📋 Tarefas**: Defina as tarefas que os agentes executarão.
    - **👥 Crews**: Crie equipes para orquestrar o trabalho.
    - **🚀 Execução**: Inicie suas crews para resolver problemas.
    """)