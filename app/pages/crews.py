"""
Página de Gerenciamento de Crews - Crie e Configure Suas Equipes de Agentes
"""

import streamlit as st
import json
import os
from datetime import datetime

def save_selected_agents(agents):
    """Salva os agentes selecionados em um arquivo JSON temporário."""
    temp_file = "temp_selected_agents.json"
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)

def load_selected_agents():
    """Carrega os agentes selecionados do arquivo JSON temporário."""
    temp_file = "temp_selected_agents.json"
    if os.path.exists(temp_file):
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def show_crews_tab():
    """Exibe a aba de gerenciamento de crews com um layout de catálogo visual."""
    st.title("👥 Gerenciamento de Crews")

    st.markdown("""
    <style>
    .stButton>button { font-size: 1.1em; }
    .progress-bar {
        background: #e0e0e0;
        border-radius: 8px;
        height: 18px;
        margin-bottom: 16px;
        overflow: hidden;
    }
    .progress-bar-inner {
        background: #4CAF50;
        height: 100%;
        transition: width 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

    # === Barra de progresso do fluxo ===
    st.markdown("""
    <div class='progress-bar'>
      <div class='progress-bar-inner' style='width: 33%'></div>
    </div>
    <b>Fluxo:</b> 1. Montar Equipe &rarr; 2. Adicionar Tarefas &rarr; 3. Criar Crew
    """, unsafe_allow_html=True)

    st.header("1️⃣ Montar Equipe (Rascunho)")
    st.info("Monte sua equipe de agentes. Salve como rascunho para continuar depois.")

    # Mapeamento de nomes técnicos para nomes amigáveis
    agent_friendly_names = {
        "researcher": "🔍 Pesquisador",
        "analyst": "📊 Analista", 
        "writer": "✍️ Escritor",
        "reviewer": "🔍 Revisor",
        "coordinator": "🎯 Coordenador",
        "excel_analyst": "📈 Analista de Excel",
        "whatsapp_monitor": "📱 Monitor do WhatsApp",
        "file_downloader": "⬇️ Baixador de Arquivos",
        "file_organizer": "📁 Organizador de Arquivos"
    }
    
    task_friendly_names = {
        "research_task": "🔍 Pesquisa e Coleta de Dados",
        "analysis_task": "📊 Análise e Interpretação",
        "writing_task": "✍️ Redação de Conteúdo",
        "review_task": "🔍 Revisão e Validação",
        "coordination_task": "🎯 Coordenação de Equipe",
        "excel_analysis_task": "📈 Análise de Planilhas",
        "whatsapp_monitoring_task": "📱 Monitoramento do WhatsApp",
        "file_download_task": "⬇️ Download de Arquivos",
        "file_organization_task": "📁 Organização de Arquivos"
    }
    
    agent_descriptions = {
        "researcher": "Especialista em buscar e coletar informações técnicas na internet",
        "analyst": "Profissional que analisa dados e gera insights valiosos",
        "writer": "Especialista em criar conteúdo claro e bem estruturado",
        "reviewer": "Responsável por revisar e validar a qualidade do trabalho",
        "coordinator": "Gerencia o fluxo de trabalho e coordena a equipe",
        "excel_analyst": "Especialista em análise de planilhas e dados estruturados",
        "whatsapp_monitor": "Monitora grupos do WhatsApp e identifica arquivos importantes",
        "file_downloader": "Baixa e gerencia arquivos de diferentes fontes",
        "file_organizer": "Organiza e categoriza arquivos de forma eficiente"
    }
    
    task_descriptions = {
        "research_task": "Coleta informações relevantes sobre o tópico especificado",
        "analysis_task": "Analisa os dados coletados e extrai insights importantes",
        "writing_task": "Cria conteúdo baseado nas análises realizadas",
        "review_task": "Revisa e valida a qualidade do trabalho final",
        "coordination_task": "Coordena o fluxo de trabalho entre os agentes",
        "excel_analysis_task": "Analisa planilhas Excel e extrai informações relevantes",
        "whatsapp_monitoring_task": "Monitora grupos do WhatsApp em busca de arquivos",
        "file_download_task": "Baixa arquivos identificados pelos monitores",
        "file_organization_task": "Organiza os arquivos baixados por categoria"
    }

    # Mapeamento de agentes para ícones
    agent_icons = {
        "technical_researcher": "🔬",
        "data_analyst": "📊",
        "technical_writer": "✍️",
        "technical_reviewer": "✅",
        "technical_coordinator": "🤝",
        "structural_engineer": "🏗️",
        "geotechnical_engineer": "⛰️",
        "hydraulic_engineer": "💧",
        "cost_engineer": "💲",
        "quality_engineer": "⭐",
        "safety_engineer": "🛡️",
        "environmental_engineer": "🌿",
        "construction_planner": "📅",
        "procurement_specialist": "🛒",
        "bim_specialist": "🏢",
        "sustainability_expert": "♻️",
        "innovation_expert": "💡",
        "legal_expert": "⚖️",
        "communication_expert": "🗣️",
    }

    crew_manager = st.session_state.crew_manager
    agent_manager = st.session_state.agent_manager
    task_manager = st.session_state.task_manager

    # 🔄 SEÇÃO DE SINCRONIZAÇÃO (movida para depois da definição do crew_manager)
    with st.expander("🔄 Sistema de Sincronização Automática", expanded=False):
        st.markdown("""
        #### Sistema de Sincronização de Configurações
        
        Este sistema monitora automaticamente mudanças nos arquivos de configuração (agents.yaml, tasks.yaml, tools.yaml) 
        e atualiza as crews salvas no banco de dados quando necessário.
        """)
        
        # Status da sincronização
        try:
            sync_status = crew_manager.get_sync_status()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("📊 Status do Sistema", 
                         "✅ Ativo" if sync_status.get('sync_available') else "❌ Inativo")
                st.metric("🗃️ Crews no Banco", sync_status.get('crews_in_database', 0))
                
            with col2:
                st.metric("💾 Crews na Memória", sync_status.get('crews_in_memory', 0))
                st.metric("🔄 Sincronização Automática", 
                         "✅ Ativa" if sync_status.get('auto_sync_enabled') else "❌ Inativa")
            
            # Botão de sincronização manual
            if st.button("🔄 Executar Sincronização Manual", type="secondary"):
                with st.spinner("Executando sincronização..."):
                    sync_result = crew_manager.sync_with_config_changes()
                    
                    if sync_result.get('status') == 'completed':
                        st.success(f"✅ Sincronização concluída! {sync_result.get('crews_checked', 0)} crew(s) verificada(s)")
                    elif sync_result.get('status') == 'error':
                        st.error(f"❌ Erro na sincronização: {sync_result.get('message', 'Erro desconhecido')}")
                    else:
                        st.info("ℹ️ Sincronização executada com resultado indefinido")
                        
        except Exception as e:
            st.error(f"❌ Erro ao obter status de sincronização: {e}")
            
        st.markdown("""
        ##### 💡 Como Funciona:
        - **Detecção Automática:** O sistema detecta quando você altera nomes de agentes, tarefas ou ferramentas
        - **Sincronização Inteligente:** Atualiza automaticamente as crews salvas para usar os novos nomes
        - **Persistência:** Suas crews continuam funcionando mesmo após mudanças nas configurações
        - **Histórico:** Mantém um log de todas as sincronizações executadas
        """)

    # Carregar agentes selecionados do arquivo JSON
    if 'selected_crew_agents' not in st.session_state:
        st.session_state.selected_crew_agents = load_selected_agents()

    # Guia de criação de crews
    with st.expander("📖 Guia: Como Criar uma Crew Eficiente", expanded=False):
        st.markdown("""
        ### 🎯 **Como Funciona uma Crew**
        
        Uma **Crew** é uma equipe de agentes que trabalham em sequência para completar uma tarefa complexa.
        
        ### 📋 **Fluxo de Trabalho Típico:**
        
        1. **🔍 Pesquisador** → Coleta informações iniciais
        2. **📊 Analista** → Analisa e interpreta os dados
        3. **✍️ Escritor** → Cria o conteúdo final
        4. **🔍 Revisor** → Revisa e valida a qualidade
        
        ### 💡 **Dicas para Crews Eficientes:**
        
        - **Ordem Importante**: Os agentes trabalham na ordem que você selecionar
        - **Especialização**: Cada agente tem ferramentas específicas
        - **Comunicação**: Os agentes passam informações entre si automaticamente
        - **Resultado Final**: O último agente gera o resultado final
        
        ### 🛠️ **Ferramentas por Agente:**
        
        - **Pesquisador**: Busca na internet, lê arquivos Excel
        - **Analista**: Analisa dados, detecta padrões, compara informações
        - **Escritor**: Gera relatórios e conteúdo estruturado
        - **Revisor**: Valida arquivos e verifica qualidade
        """)

    st.markdown("---")

    # --- Layout principal com 2 colunas ---
    col1, col2 = st.columns([3, 1])  # Coluna da esquerda 3x maior

    # --- Coluna da Direita (Formulário e Equipe Montada) ---
    with col2:
        st.subheader("🚀 1. Detalhes da Crew")
        
        # Formulário para detalhes da crew
        with st.form(key="crew_form", border=True):
            crew_name = st.text_input("Nome da Crew", placeholder="Ex: Equipe de Pesquisa de Mercado")
            crew_description = st.text_area("Descrição da Crew", placeholder="Descreva o objetivo da equipe...")
            submit_button = st.form_submit_button("✅ Criar Crew", type="primary", use_container_width=True)

        # Seção de gerenciamento da equipe (fora do formulário)
        st.markdown("### 👥 2. Sua Equipe")
        
        if not st.session_state.selected_crew_agents:
            st.info("Adicione agentes do catálogo para montar sua equipe.")
        else:
            st.markdown("**Ordem de Trabalho:** (Os agentes trabalharão nesta sequência)")
            
            # Interface de manipulação da equipe
            for i, agent in enumerate(st.session_state.selected_crew_agents):
                icon = agent_icons.get(agent['type'], '🤖')
                
                # Container para cada agente com controles
                with st.container(border=True):
                    col_agent, col_controls = st.columns([3, 1])
                    
                    with col_agent:
                        st.markdown(f"**{i+1}. {icon} {agent['name']}**")
                    
                    with col_controls:
                        # Botões de controle para cada agente
                        col_up, col_down = st.columns(2)
                        
                        with col_up:
                            if st.button("⬆️", key=f"up_{i}", help="Mover para cima", disabled=i==0):
                                if i > 0:
                                    st.session_state.selected_crew_agents[i], st.session_state.selected_crew_agents[i-1] = \
                                        st.session_state.selected_crew_agents[i-1], st.session_state.selected_crew_agents[i]
                                    save_selected_agents(st.session_state.selected_crew_agents)
                                    st.rerun()
                        
                        with col_down:
                            if st.button("⬇️", key=f"down_{i}", help="Mover para baixo", disabled=i==len(st.session_state.selected_crew_agents)-1):
                                if i < len(st.session_state.selected_crew_agents) - 1:
                                    st.session_state.selected_crew_agents[i], st.session_state.selected_crew_agents[i+1] = \
                                        st.session_state.selected_crew_agents[i+1], st.session_state.selected_crew_agents[i]
                                    save_selected_agents(st.session_state.selected_crew_agents)
                                    st.rerun()
                    
                    # Botão de remoção individual
                    if st.button("❌ Remover", key=f"remove_{i}", use_container_width=True):
                        st.session_state.selected_crew_agents.pop(i)
                        save_selected_agents(st.session_state.selected_crew_agents)
                        st.rerun()
            
            # Botões de ação em massa
            col_clear, col_save = st.columns(2)
            
            with col_clear:
                if st.button("🗑️ Limpar Equipe", key="clear_team", use_container_width=True):
                    st.session_state.selected_crew_agents = []
                    save_selected_agents([])
                    st.rerun()
            
            with col_save:
                if st.button("💾 Salvar Equipe", key="save_team", use_container_width=True):
                    save_selected_agents(st.session_state.selected_crew_agents)
                    st.success("Equipe salva com sucesso!")

    # --- Coluna da Esquerda (Catálogo de Agentes) ---
    with col1:
        st.subheader("🤖 Catálogo de Agentes")
        st.info("Clique em 'Adicionar' para montar sua equipe na coluna à direita.")
        
        available_agents = agent_manager.list_available_agent_types()
        
        # Galeria de agentes em 4 colunas
        gallery_cols = st.columns(4)
        col_idx = 0

        for agent_type in available_agents:
            agent_info = agent_manager.get_agent_info(agent_type)
            if not agent_info:
                continue

            with gallery_cols[col_idx]:
                with st.container(border=True):
                    icon = agent_icons.get(agent_type, "🤖")
                    st.markdown(f"#### {icon} {agent_info.get('name', agent_type)}")
                    st.markdown(f"**Função:** *{agent_info.get('role', 'N/A')}*")
                    
                    # Verificar se o agente já está na equipe
                    is_selected = any(a['type'] == agent_type for a in st.session_state.selected_crew_agents)
                    
                    if not is_selected:
                        if st.button("➕ Adicionar", key=f"add_{agent_type}", use_container_width=True):
                            st.session_state.selected_crew_agents.append({
                                "type": agent_type, 
                                "name": agent_info.get('name', agent_type)
                            })
                            save_selected_agents(st.session_state.selected_crew_agents)
                            st.rerun()
                    else:
                        st.markdown("✅ **Já na equipe**")
                    
                    with st.expander("Ver detalhes"):
                        st.markdown(f"**Objetivo:** {agent_info.get('goal', 'N/A')}")
                        st.markdown(f"**Histórico:** {agent_info.get('backstory', 'N/A')}")
                        tools = agent_manager.get_agent_tools(agent_type)
                        if tools:
                            st.markdown("**Ferramentas:**")
                            for tool in tools:
                                st.code(tool, language='bash')
            
            col_idx = (col_idx + 1) % 4

    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.button("💾 Salvar Rascunho", key="save_draft", help="Guarda sua seleção para continuar depois", use_container_width=True)
    with col2:
        st.button("🗑️ Limpar Seleção", key="clear_selection", help="Remove todos os agentes selecionados", use_container_width=True)
    with col3:
        st.button("👀 Visualizar Rascunho", key="view_draft", help="Veja o rascunho salvo", use_container_width=True)

    st.markdown("---")
    st.header("2️⃣ Adicionar Tarefas à Equipe")
    st.info("Selecione as tarefas que cada agente irá executar. O número de tarefas deve ser igual ao de agentes.")

    # Processamento do formulário após o clique no botão
    if submit_button:
        selected_agents_types = [agent['type'] for agent in st.session_state.selected_crew_agents]
        
        # Mapeamento automático de agentes para tarefas (simplificado)
        agent_to_task_mapping = {
            "technical_researcher": "research_task",
            "data_analyst": "analysis_task", 
            "technical_writer": "writing_task",
            # Adicionar outros mapeamentos conforme necessário
        }
        selected_tasks = [agent_to_task_mapping.get(agent_type, "research_task") for agent_type in selected_agents_types]

        if not crew_name:
            st.error("Por favor, forneça um nome para a crew.")
        elif not selected_agents_types:
            st.error("Por favor, selecione pelo menos um agente.")
        else:
            try:
                st.info(f"🔄 Criando crew '{crew_name}' com {len(selected_agents_types)} agentes...")
                
                # Criar a crew com a ordem exata selecionada
                crew = crew_manager.create_crew_with_tasks(
                    crew_name, selected_agents_types, selected_tasks, crew_description
                )
                
                if crew:
                    st.success(f"✅ Crew '{crew_name}' criada com sucesso!")
                    
                    # Mostrar resumo da crew criada
                    with st.expander("📋 Resumo da Crew Criada", expanded=True):
                        st.markdown(f"**Nome:** {crew_name}")
                        st.markdown(f"**Descrição:** {crew_description}")
                        st.markdown("**🔄 Fluxo de Trabalho:**")
                        
                        for i, (agent_type, task_type) in enumerate(zip(selected_agents_types, selected_tasks), 1):
                            icon = agent_icons.get(agent_type, "🤖")
                            agent_name = agent_friendly_names.get(agent_type, agent_type)
                            task_name = task_friendly_names.get(task_type, task_type)
                            
                            if i < len(selected_agents_types):
                                st.markdown(f"{i}. {icon} **{agent_name}** → {task_name} ⬇️")
                            else:
                                st.markdown(f"{i}. {icon} **{agent_name}** → {task_type} ✅")
                        
                        st.markdown("---")
                        st.markdown("**💡 Como funciona:** Os agentes trabalham em sequência, passando informações entre si até completar a tarefa.")
                    
                    st.info("🎉 A crew está pronta para execução! Vá para a aba 'Execução' para testá-la.")
                    
                    # Limpar a equipe após criar a crew
                    st.session_state.selected_crew_agents = []
                    save_selected_agents([])
                    st.rerun()
                else:
                    st.error("❌ Falha ao criar a crew. Verifique os logs no terminal.")
                    
            except Exception as e:
                st.error(f"❌ Erro ao criar crew: {e}")

    # Lista de crews existentes
    st.markdown("---")
    st.subheader("📋 Crews Existentes")
    
    try:
        crews = crew_manager.get_all_crews()
        
        if not crews:
            st.info("Nenhuma crew foi criada ainda. Crie sua primeira crew acima!")
        else:
            for crew_name, crew in crews.items():
                crew_info = crew_manager.get_crew_info(crew_name)
                
                with st.expander(f"👥 {crew_name}", expanded=False):
                    if crew_info:
                        st.markdown(f"**Descrição:** {crew_info.get('description', 'Sem descrição')}")
                        st.markdown(f"**Agentes:** {len(crew.agents)}")
                        st.markdown(f"**Tarefas:** {len(crew.tasks)}")
                        
                        # Mostrar agentes da crew
                        st.markdown("**Agentes na Crew:**")
                        for i, agent in enumerate(crew.agents, 1):
                            agent_role = getattr(agent, 'role', 'Agente')
                            st.markdown(f"{i}. {agent_role}")
                        
                        # Mostrar tarefas da crew
                        if crew.tasks:
                            st.markdown("**Tarefas da Crew:**")
                            for i, task in enumerate(crew.tasks, 1):
                                task_desc = getattr(task, 'description', 'Tarefa')
                                st.markdown(f"{i}. {task_desc[:50]}...")
                    
                    # Botões de ação
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"🗑️ Deletar {crew_name}", key=f"delete_{crew_name}"):
                            if crew_manager.delete_crew(crew_name):
                                st.success(f"Crew '{crew_name}' deletada!")
                                st.rerun()
                    
                    with col2:
                        if st.button(f"▶️ Executar {crew_name}", key=f"execute_{crew_name}"):
                            st.info(f"Vá para a aba 'Execução' para executar a crew '{crew_name}'")
    
    except Exception as e:
        st.error(f"Erro ao carregar crews: {e}")