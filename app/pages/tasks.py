"""
Gerenciamento de Tarefas - Configuração e Visualização de Tarefas
"""

import streamlit as st
from pathlib import Path

# Dicionário de nomes amigáveis para tarefas
NOMES_TAREFAS = {
    "research_task": "Pesquisa",
    "analysis_task": "Análise de Dados",
    "writing_task": "Redação de Relatório",
    "review_task": "Revisão",
    "coordination_task": "Coordenação",
    "excel_analysis_task": "Análise de Excel",
    "whatsapp_monitoring_task": "Monitoramento WhatsApp",
    "file_download_task": "Download de Arquivos",
    "file_organization_task": "Organização de Arquivos"
}

def get_task_category_icon(task_type):
    """Retorna um ícone com base no tipo da tarefa."""
    if "research" in task_type:
        return "🔍"
    elif "writing" in task_type:
        return "✍️"
    elif "review" in task_type:
        return "✅"
    elif "excel" in task_type:
        return "📈"
    elif "whatsapp" in task_type or "file" in task_type:
        return "📂"
    return "📊"

def show_tasks_tab():
    """Exibe a aba de gerenciamento de tarefas."""
    st.header("📋 Gerenciamento de Tarefas")
    st.markdown("### Visualize e configure as tarefas disponíveis no sistema")
    
    # Ajuda geral
    with st.expander("ℹ️ Sobre Tarefas", expanded=False):
        st.info("""
        **O que são tarefas?**
        Tarefas são ações específicas que os agentes podem executar para alcançar objetivos.

        **Como funcionam:**
        1. Cada tarefa tem um agente responsável.
        2. Tarefas podem ser combinadas em crews (equipes).
        3. As tarefas são executadas sequencialmente.
        4. O resultado de uma tarefa pode alimentar a próxima.
        """)

    st.markdown("---")

    task_manager = st.session_state.task_manager
    agent_manager = st.session_state.agent_manager
    
    # Estatísticas
    st.subheader("📊 Visão Geral")
    try:
        available_tasks = task_manager.list_available_task_types()
        tasks_with_agents = sum(1 for task_type in available_tasks 
                               if (task_manager.get_task_info(task_type) or {}).get("agent"))
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Tipos de Tarefas", len(available_tasks), help="Número total de tarefas pré-configuradas no sistema.")
        col2.metric("Tarefas com Agente Atribuído", tasks_with_agents, help="Tarefas que já possuem um agente padrão definido.")
    except Exception as e:
        st.error(f"Não foi possível carregar as estatísticas das tarefas: {e}")

    st.markdown("---")
    
    # Lista detalhada de tarefas
    st.subheader("📋 Detalhes das Tarefas Disponíveis")
    
    try:
        if not available_tasks:
            st.warning("Nenhuma tarefa encontrada. Verifique o arquivo `app/config/tasks.yaml`.")
        else:
            for task_type in available_tasks:
                info = task_manager.get_task_info(task_type) or {}
                
                nome_amigavel = NOMES_TAREFAS.get(task_type, task_type.replace("_", " ").title())
                icon = get_task_category_icon(task_type)
                
                with st.expander(f"{icon} **{nome_amigavel}** (`{task_type}`)", expanded=False):
                    description = info.get("description", "*Sem descrição*")
                    expected_output = info.get("expected_output", "*Não especificado*")
                    agent_name = info.get("agent", "Nenhum")

                    st.markdown(f"**Descrição**: {description}")
                    st.markdown(f"**Saída Esperada**: {expected_output}")

                    st.markdown(f"**Agente Responsável Padrão**: `{agent_name}`")
                    
                    if agent_name != "Nenhum":
                        agent_info = agent_manager.get_agent_info(agent_name)
                        if agent_info:
                            st.success(f"✅ Agente **{agent_info.get('name', agent_name)}** encontrado e pronto para uso.")
                        else:
                            st.error(f"❌ O agente **{agent_name}** não foi encontrado. Verifique a configuração.")

                    if "parameters" in info:
                        st.markdown("**Parâmetros da Tarefa:**")
                        st.json(info["parameters"])
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar os detalhes das tarefas: {e}")

    # Informações sobre configuração
    st.markdown("---")
    st.subheader("ℹ️ Informações sobre Configuração")
    
    st.info("""
    As tarefas são configuradas no arquivo `app/config/tasks.yaml`. 
    Para adicionar ou modificar uma tarefa, edite este arquivo e recarregue a aplicação.
    """)
    
    # Visualizar configuração atual
    with st.expander("📄 Visualizar Configuração Atual (`tasks.yaml`)"):
        try:
            with open("app/config/tasks.yaml", "r", encoding="utf-8") as f:
                current_config = f.read()
            st.code(current_config, language="yaml")
        except Exception as e:
            st.error(f"Erro ao ler arquivo de configuração: {e}")

    # Exemplos de uso
    st.markdown("---")
    st.subheader("💡 Exemplos de Uso")
    
    examples = [
        {
            "title": "Pesquisa Completa",
            "description": "Pesquisar sobre um tópico e gerar relatório",
            "tasks": ["research_task", "analysis_task", "writing_task"],
            "agents": ["researcher", "analyst", "writer"]
        },
        {
            "title": "Análise de Dados",
            "description": "Analisar dados e gerar insights",
            "tasks": ["analysis_task", "writing_task"],
            "agents": ["analyst", "writer"]
        },
        {
            "title": "Análise de Planilhas",
            "description": "Comparar e analisar planilhas Excel",
            "tasks": ["excel_analysis_task"],
            "agents": ["excel_analyst"]
        }
    ]
    
    for example in examples:
        with st.expander(f"📋 {example['title']}", expanded=False):
            st.write(f"**Descrição:** {example['description']}")
            st.write("**Tarefas:** " + ", ".join([str(NOMES_TAREFAS.get(t, t)) for t in example['tasks']]))
            st.write(f"**Agentes:** {', '.join(example['agents'])}") 