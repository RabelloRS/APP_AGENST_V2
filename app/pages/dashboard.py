"""
Dashboard Principal da Aplicação - Versão Profissional
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


def show_dashboard():
    """Dashboard principal da aplicação com layout profissional e acesso rápido."""
    
    # Configuração da página
    st.set_page_config(page_title="Dashboard - Sistema de Agentes", page_icon="📊", layout="wide")
    
    # Header profissional
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            logo_path = "media/logo/LOGO_PROPOR_MEDIO.jpg"
            st.image(logo_path, width=80)
        except:
            st.markdown("🏗️")
    
    with col2:
        st.title("📊 Dashboard do Sistema")
        st.markdown("*Visão geral e controle central do ecossistema de agentes inteligentes*")
    
    st.markdown("---")
    
    # Gerentes de estado
    agent_manager = st.session_state.agent_manager
    task_manager = st.session_state.task_manager
    tools_manager = st.session_state.tools_manager
    crew_manager = st.session_state.crew_manager
    
    # ===== MÉTRICAS PRINCIPAIS =====
    st.subheader("📈 Métricas do Sistema")
    
    try:
        # Calcular métricas
        total_agents = len(agent_manager.list_available_agent_types())
        total_tasks = len(task_manager.list_available_task_types())
        total_tools = len(tools_manager.list_all_tools())
        total_crews = len(crew_manager.list_crew_names())
        
        # Layout em grid responsivo
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🤖 Agentes Ativos",
                value=total_agents,
                help="Total de agentes especializados configurados"
            )
        
        with col2:
            st.metric(
                label="📋 Tarefas Disponíveis",
                value=total_tasks,
                help="Tipos de tarefas que podem ser executadas"
            )
        
        with col3:
            st.metric(
                label="🔧 Ferramentas",
                value=total_tools,
                help="Ferramentas disponíveis para os agentes"
            )
        
        with col4:
            st.metric(
                label="👥 Crews Prontas",
                value=total_crews,
                help="Equipes configuradas para execução"
            )
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar métricas: {e}")
    
    st.markdown("---")
    
    # ===== CREWS EXECUTÁVEIS - ACESSO RÁPIDO =====
    st.subheader("🚀 Crews Disponíveis para Execução")
    
    try:
        crew_names = crew_manager.list_crew_names()
        
        if not crew_names:
            st.info("📝 **Nenhuma crew configurada ainda.**\n\nPara começar:\n1. Vá para **Gerenciamento → Crews**\n2. Crie uma nova crew\n3. Configure os agentes e tarefas")
        else:
            # Organizar crews em cards
            cols = st.columns(3)
            
            for idx, crew_name in enumerate(crew_names):
                with cols[idx % 3]:
                    crew_info = crew_manager.get_crew_info(crew_name)
                    
                    # Card da crew
                    with st.container():
                        st.markdown(f"""
                        <div style="
                            border: 1px solid #e0e0e0;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 10px 0;
                            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <h4 style="margin: 0 0 10px 0; color: #1f77b4;">👥 {crew_name}</h4>
                            <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">
                                {crew_info.get('description', 'Crew especializada') if crew_info else 'Crew especializada'}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botões de ação
                        col_btn1, col_btn2 = st.columns(2)
                        
                        with col_btn1:
                            if st.button("▶️ Executar", key=f"exec_{crew_name}", use_container_width=True):
                                st.session_state.selected_crew = crew_name
                                st.switch_page("pages/execution")
                        
                        with col_btn2:
                            if st.button("⚙️ Configurar", key=f"config_{crew_name}", use_container_width=True):
                                st.session_state.selected_crew = crew_name
                                st.switch_page("pages/crews")
    
    except Exception as e:
        st.error(f"❌ Erro ao carregar crews: {e}")
    
    st.markdown("---")
    
    # ===== ATALHOS RÁPIDOS =====
    st.subheader("⚡ Ações Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🤖 Gerenciar Agentes", use_container_width=True, help="Configurar agentes especializados"):
            st.switch_page("pages/agents")
    
    with col2:
        if st.button("📋 Gerenciar Tarefas", use_container_width=True, help="Definir e editar tarefas"):
            st.switch_page("pages/tasks")
    
    with col3:
        if st.button("🧩 Criar Workflow", use_container_width=True, help="Construtor visual de fluxos"):
            st.switch_page("pages/workflow_builder")
    
    with col4:
        if st.button("📱 WhatsApp", use_container_width=True, help="Integração com WhatsApp"):
            st.switch_page("pages/whatsapp")
    
    st.markdown("---")
    
    # ===== STATUS DO SISTEMA =====
    st.subheader("🔧 Status do Sistema")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status das configurações
        st.markdown("**📋 Configurações:**")
        
        config_status = []
        
        # Verificar arquivos de configuração
        config_files = ["agents.yaml", "tasks.yaml", "tools.yaml", "crews.yaml"]
        for file in config_files:
            file_path = Path(f"app/config/{file}")
            if file_path.exists():
                config_status.append(f"✅ {file}")
            else:
                config_status.append(f"❌ {file}")
        
        for status in config_status:
            st.markdown(f"- {status}")
    
    with col2:
        # Status da API
        st.markdown("**🔑 API Keys:**")
        
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        
        if api_key and api_key != "your_openai_api_key_here":
            st.markdown("✅ OpenAI API configurada")
        else:
            st.markdown("❌ OpenAI API não configurada")
        
        # Verificar outras APIs se necessário
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
            st.markdown("✅ Anthropic API configurada")
        else:
            st.markdown("⚠️ Anthropic API não configurada")
    
    st.markdown("---")
    
    # ===== ATIVIDADE RECENTE =====
    st.subheader("📜 Atividade Recente")
    
    try:
        # Buscar estatísticas do banco de dados
        stats = crew_manager.db_manager.get_statistics()
        
        if stats["total_executions"] > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Execuções", stats["total_executions"])
            
            with col2:
                st.metric("Taxa de Sucesso", f"{stats['success_rate']:.1f}%")
            
            with col3:
                if stats["most_executed_crew"]:
                    st.metric("Crew Mais Usada", stats["most_executed_crew"])
                else:
                    st.metric("Crew Mais Usada", "N/A")
            
            # Mostrar execuções recentes se disponível
            if "execution_history" in st.session_state and st.session_state.execution_history:
                st.markdown("**Últimas Execuções:**")
                history_df = pd.DataFrame(st.session_state.execution_history).tail(3)
                if not history_df.empty:
                    st.dataframe(
                        history_df[["Crew", "Tópico", "Início", "Duração"]],
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Crew": st.column_config.TextColumn("Equipe"),
                            "Tópico": st.column_config.TextColumn("Tópico"),
                            "Início": st.column_config.DatetimeColumn("Início", format="DD/MM HH:mm"),
                            "Duração": st.column_config.TextColumn("Duração"),
                        }
                    )
        else:
            st.info("📝 **Nenhuma execução registrada ainda.**\n\nExecute uma crew para ver a atividade aqui.")
    
    except Exception as e:
        st.warning(f"⚠️ Não foi possível carregar estatísticas: {e}")
    
    st.markdown("---")
    
    # ===== FOOTER PROFISSIONAL =====
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px; margin-top: 30px;">
        <p style="margin: 0; color: #666; font-size: 14px;">
            <strong>Sistema de Agentes de Engenharia</strong> | Desenvolvido pela Propor Engenharia<br>
            Eng. Civil Rodrigo Emanuel Rabello | CREA-RS 167.175-D
        </p>
    </div>
    """, unsafe_allow_html=True)


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
