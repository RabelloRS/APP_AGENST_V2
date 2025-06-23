"""
Gerenciamento de Tarefas - Configuração e Visualização de Tarefas
"""

import streamlit as st
import os
from datetime import date

# Ícones personalizados por tipo de tarefa
TASK_ICONS = {
    "initial_research_task": "🔍",
    "data_analysis_task": "📊",
    "technical_writing_task": "📝",
    "technical_review_task": "✅",
    "project_coordination_task": "🧑‍💼",
    "structural_design_task": "🏗️",
    "geotechnical_report_task": "🌍",
    "foundation_design_task": "🏢",
    "retaining_wall_design_task": "🧱",
    "bridge_design_task": "🌉",
    "fem_analysis_task": "⚙️",
    "hydrological_study_task": "🌊",
    "drainage_system_design_task": "💧",
    "sanitation_plan_task": "🚰",
    "waste_management_plan_task": "♻️",
    "environmental_licensing_task": "🌱",
    "environmental_damage_assessment_task": "⚠️",
    "highway_geometric_design_task": "🛣️",
    "pavement_design_task": "🛤️",
    "traffic_impact_study_task": "🚦",
    "cost_estimation_task": "💰",
    "bidding_analysis_task": "📋",
    "budget_audit_task": "🔍",
    "funding_opportunity_mapping_task": "🎯",
    "transferegov_proposal_submission_task": "📤",
    "bim_coordination_task": "🏗️",
    "electrical_design_task": "⚡",
    "spda_design_task": "⚡",
    "hvac_design_task": "❄️",
    "construction_tech_scouting_task": "🚀",
    "fire_safety_plan_task": "🔥",
    "solar_energy_project_task": "☀️",
    "tool_development_task": "🔧",
    "tool_testing_task": "🧪",
    "crew_evaluation_task": "📈",
}

NOMES_TAREFAS = {
    # Tarefas Genéricas de Projeto
    "initial_research_task": "Pesquisa Técnica Inicial",
    "data_analysis_task": "Análise de Dados",
    "technical_writing_task": "Redação Técnica",
    "technical_review_task": "Revisão Técnica",
    "project_coordination_task": "Coordenação de Projeto",
    
    # Tarefas de Engenharia Estrutural e Geotecnia
    "structural_design_task": "Projeto Estrutural",
    "geotechnical_report_task": "Relatório Geotécnico",
    "foundation_design_task": "Projeto de Fundações",
    "retaining_wall_design_task": "Projeto de Muro de Contenção",
    "bridge_design_task": "Projeto de Ponte",
    "fem_analysis_task": "Análise por Elementos Finitos",
    
    # Tarefas de Hidráulica, Saneamento e Meio Ambiente
    "hydrological_study_task": "Estudo Hidrológico",
    "drainage_system_design_task": "Projeto de Drenagem",
    "sanitation_plan_task": "Plano de Saneamento",
    "waste_management_plan_task": "Plano de Gestão de Resíduos",
    "environmental_licensing_task": "Licenciamento Ambiental",
    "environmental_damage_assessment_task": "Avaliação de Dano Ambiental",
    
    # Tarefas de Infraestrutura Viária
    "highway_geometric_design_task": "Projeto Geométrico Rodoviário",
    "pavement_design_task": "Projeto de Pavimentação",
    "traffic_impact_study_task": "Estudo de Impacto de Tráfego",
    
    # Tarefas de Orçamento, Licitação e Financiamento
    "cost_estimation_task": "Orçamento de Obra",
    "bidding_analysis_task": "Análise de Edital",
    "budget_audit_task": "Auditoria de Orçamento",
    "funding_opportunity_mapping_task": "Mapeamento de Oportunidades de Financiamento",
    "transferegov_proposal_submission_task": "Submissão de Proposta no Transferegov",
    
    # Tarefas de Projetos Prediais Complementares e Inovação
    "bim_coordination_task": "Coordenação BIM",
    "electrical_design_task": "Projeto Elétrico",
    "spda_design_task": "Projeto de SPDA (Para-raios)",
    "hvac_design_task": "Projeto de Climatização",
    "construction_tech_scouting_task": "Levantamento de Tecnologias Inovadoras",
    "fire_safety_plan_task": "Plano de Prevenção contra Incêndio",
    "solar_energy_project_task": "Projeto de Energia Solar",
    
    # Tarefas de Desenvolvimento de Ferramentas
    "tool_development_task": "Desenvolvimento de Ferramenta",
    "tool_testing_task": "Teste de Ferramenta",
    
    # Tarefa de Avaliação
    "crew_evaluation_task": "Avaliação de Performance da Equipe",
}


def show_tasks_tab():
    st.set_page_config(page_title="Gerenciar Tarefas", layout="wide")
    st.title("Gerenciamento de Tarefas Especializadas")
    st.info("Gerencie as tarefas: edite, exclua ou crie novas tarefas para sua equipe.")

    task_manager = st.session_state.task_manager
    agent_manager = st.session_state.agent_manager
    tools_manager = st.session_state.tools_manager

    # Estado de edição/criação/exclusão
    if "editing_task" not in st.session_state:
        st.session_state.editing_task = None
    if "creating_task" not in st.session_state:
        st.session_state.creating_task = False
    if "delete_task" not in st.session_state:
        st.session_state.delete_task = None

    # Listagem visual das tarefas em cards
    st.subheader("Tarefas cadastradas")
    available_tasks = task_manager.list_available_task_types()
    if not available_tasks:
        st.warning("Nenhuma tarefa cadastrada.")
    else:
        cols = st.columns(4)
        for idx, task_type in enumerate(available_tasks):
            info = task_manager.get_task_info(task_type) or {}
            icon = TASK_ICONS.get(task_type, "📋")
            nome_amigavel = NOMES_TAREFAS.get(task_type, task_type.replace("_", " ").title())
            with cols[idx % 4]:
                with st.expander(f"{icon} {nome_amigavel}", expanded=False):
                    st.markdown(f"**Descrição:** {info.get('description', '*Sem descrição*')}")
                    st.markdown(f"**Agente:** {info.get('agent', '*Não definido*')}")
                    st.markdown(f"**Saída Esperada:** {info.get('expected_output', '*Não especificado*')}")
                    st.markdown(f"**Contexto:** {info.get('context', '-')}")
                    st.markdown(
                        f"**Ferramentas:** {', '.join(info.get('tools', [])) if info.get('tools') else '_Nenhuma_'}"
                    )
                    st.markdown(f"**Parâmetros:** {info.get('parameters', '-')}")
                    st.markdown(f"**Formato de Saída:** {info.get('output_format', '-')}")
                    st.markdown(
                        f"**Dependências:** {', '.join(info.get('dependencies', [])) if info.get('dependencies') else '-'}"
                    )
                    st.markdown(f"**Prazo:** {info.get('deadline', '-')}")
                    st.markdown(f"**Status:** {info.get('status', '-')}")
                    colb1, colb2 = st.columns(2)
                    with colb1:
                        if st.button("✏️ Editar", key=f"edit_{task_type}"):
                            st.session_state.editing_task = task_type
                            st.session_state.creating_task = False
                    with colb2:
                        if st.button("🗑️ Excluir", key=f"delete_{task_type}"):
                            st.session_state.delete_task = task_type

    # Confirmação de exclusão
    if st.session_state.delete_task:
        task_to_delete = st.session_state.delete_task
        info = task_manager.get_task_info(task_to_delete) or {}
        st.warning(
            f"Deseja realmente excluir a tarefa **{NOMES_TAREFAS.get(task_to_delete, task_to_delete)}**?", icon="⚠️"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmar Exclusão", key="confirm_delete_task"):
                try:
                    task_manager.delete_task(task_to_delete)
                    st.success(f"Tarefa '{NOMES_TAREFAS.get(task_to_delete, task_to_delete)}' excluída com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir tarefa: {e}")
                st.session_state.delete_task = None
                st.rerun()
        with col2:
            if st.button("Cancelar", key="cancel_delete_task"):
                st.session_state.delete_task = None

    # Formulário de criação/edição
    def show_task_form(form_title, task_data, edit_key=None):
        with st.form(key="form_create_edit_task"):
            st.markdown(f"#### {form_title}")
            description = st.text_area("Descrição da tarefa", value=task_data.get("description", ""))
            agent = st.selectbox(
                "Agente responsável",
                options=["-"] + agent_manager.list_available_agent_types(),
                index=(
                    0
                    if not task_data.get("agent")
                    else agent_manager.list_available_agent_types().index(task_data.get("agent")) + 1
                ),
            )
            expected_output = st.text_area("Saída esperada", value=task_data.get("expected_output", ""))
            context = st.text_area("Contexto (opcional)", value=task_data.get("context", ""))
            all_tools = (
                tools_manager.list_available_tool_types() if hasattr(tools_manager, "list_available_tool_types") else []
            )
            selected_tools = st.multiselect(
                "Ferramentas habilitadas", options=all_tools, default=task_data.get("tools", [])
            )
            parameters = st.text_area("Parâmetros (JSON opcional)", value=str(task_data.get("parameters", "")))
            output_format = st.text_input("Formato de saída (opcional)", value=task_data.get("output_format", ""))
            dependencies = st.text_area(
                "Dependências (lista de tarefas, opcional)", value=", ".join(task_data.get("dependencies", []))
            )
            deadline = st.date_input(
                "Prazo (opcional)",
                value=task_data.get("deadline", date.today()) if task_data.get("deadline") else date.today(),
            )
            status = st.text_input("Status (opcional)", value=task_data.get("status", ""))
            submitted = st.form_submit_button("Salvar")
            if submitted:
                try:
                    task_manager.save_task(
                        description=description,
                        agent=agent if agent != "-" else None,
                        expected_output=expected_output,
                        context=context,
                        tools=list(selected_tools),
                        parameters=parameters,
                        output_format=output_format,
                        dependencies=[d.strip() for d in dependencies.split(",") if d.strip()],
                        deadline=str(deadline),
                        status=status,
                        edit_key=edit_key,
                    )
                    st.success(f"Tarefa salva com sucesso!")
                    st.session_state.editing_task = None
                    st.session_state.creating_task = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar tarefa: {e}")
        if st.button("Cancelar", key="cancel_form_task"):
            st.session_state.editing_task = None
            st.session_state.creating_task = False

    # Botão para criar nova tarefa
    st.markdown("---")
    if st.button("➕ Adicionar nova tarefa"):
        st.session_state.creating_task = True
        st.session_state.editing_task = None

    if st.session_state.creating_task:
        show_task_form(
            "Nova Tarefa",
            {
                "description": "",
                "agent": "",
                "expected_output": "",
                "context": "",
                "tools": [],
                "parameters": "",
                "output_format": "",
                "dependencies": [],
                "deadline": str(date.today()),
                "status": "",
            },
            edit_key=None,
        )

    if st.session_state.editing_task:
        task_key = st.session_state.editing_task
        info = task_manager.get_task_info(task_key) or {}
        show_task_form(f"Editar Tarefa: {NOMES_TAREFAS.get(task_key, task_key)}", info, edit_key=task_key)

    # Visualização do YAML de configuração
    st.markdown("---")
    st.subheader("📄 Visualizar Configuração Atual (`tasks.yaml`)")
    try:
        with open("app/config/tasks.yaml", "r", encoding="utf-8") as f:
            st.code(f.read(), language="yaml")
    except Exception as e:
        st.error(f"Erro ao ler arquivo de configuração: {e}")

    st.markdown("---")
    st.caption("Desenvolvido com CrewAI e Streamlit • © 2024")
