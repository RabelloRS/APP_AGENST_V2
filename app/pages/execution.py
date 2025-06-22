"""
Página de Execução de Crews - Inicie e Acompanhe Suas Equipes em Ação
"""

import streamlit as st
from datetime import datetime
import pandas as pd

def show_execution_tab():
    """Exibe a aba de execução de crews."""
    st.header("🚀 Execução de Crews")
    st.markdown("### Inicie e acompanhe o trabalho das suas equipes de agentes")

    with st.expander("ℹ️ Como Executar uma Crew", expanded=False):
        st.info("""
        1. **Selecione a Crew**: Escolha uma das equipes configuradas.
        2. **Informe os Parâmetros**: Preencha as informações necessárias para as tarefas (ex: tópico de pesquisa).
        3. **Inicie a Execução**: Clique no botão para colocar a equipe para trabalhar.
        4. **Acompanhe o Resultado**: O progresso e o resultado final serão exibidos abaixo.
        """)

    st.markdown("---")

    crew_manager = st.session_state.crew_manager

    # Seção de Execução
    st.subheader("⚙️ Configurar e Iniciar Execução")
    
    try:
        crew_options = crew_manager.list_crew_names()
        if not crew_options:
            st.warning("Nenhuma crew encontrada. Crie uma na aba 'Crews' para começar.")
            return

        selected_crew = st.selectbox(
            "Selecione a Crew para Executar",
            options=crew_options,
            index=0,
            help="Escolha qual equipe de agentes você deseja acionar."
        )

        st.markdown("**Parâmetros de Entrada:**")
        # Parâmetros dinâmicos baseados nas tarefas da crew
        task_inputs = {}
        # Por enquanto, usamos um campo genérico "topic", mas isso pode ser expandido
        topic = st.text_input(
            "Tópico ou Instrução Principal",
            placeholder="Ex: Análise de mercado sobre IA no Brasil",
            help="Forneça o contexto principal para a execução das tarefas."
        )
        task_inputs['topic'] = topic

        if st.button("🚀 Iniciar Execução da Crew", type="primary", use_container_width=True):
            if not selected_crew:
                st.error("Por favor, selecione uma crew.")
            elif not topic:
                st.error("Por favor, forneça um tópico ou instrução.")
            else:
                # Criar containers para resultado e logs
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader("📄 Resultado da Execução")
                    result_container = st.empty()
                
                with col2:
                    st.subheader("📊 Logs de Execução em Tempo Real")
                    logs_container = st.empty()
                
                # Botão para escolher modo de execução
                execution_mode = st.radio(
                    "Modo de Execução:",
                    ["🔍 Com Logs (Recomendado)", "⚡ Modo Rápido (Sem Logs)"],
                    horizontal=True,
                    help="Logs mostram o progresso em tempo real, mas podem ser mais lentos"
                )
                
                # Iniciar execução
                with st.spinner(f"Executando a crew '{selected_crew}'... Acompanhe o progresso {'nos logs ao lado' if 'Com Logs' in execution_mode else 'abaixo'}."):
                    try:
                        if "Com Logs" in execution_mode:
                            # Execução com status visual
                            with logs_container.container():
                                st.markdown("### 📊 Status da Execução")
                                status_messages = st.empty()
                                
                                # Mostrar status inicial
                                status_messages.markdown("""
                                🔵 **Iniciando execução da crew...**
                                
                                📋 Preparando agentes e tarefas...
                                """)
                            
                            # Executar crew
                            result = crew_manager.execute_crew_safe(selected_crew, inputs=task_inputs)
                            
                            # Atualizar status final
                            with logs_container.container():
                                if result:
                                    status_messages.markdown("""
                                    ✅ **Execução concluída!**
                                    
                                    🔍 Crew executada com sucesso
                                    📄 Resultado gerado
                                    ✅ Avaliação automática aplicada
                                    """)
                                else:
                                    status_messages.markdown("""
                                    ❌ **Execução falhou**
                                    
                                    ⚠️ Houve um problema durante a execução
                                    """)
                            
                            # Exibir resultado
                            with result_container.container():
                                if result:
                                    st.success("✅ Execução concluída com sucesso!")
                                    st.markdown(result)
                                else:
                                    st.error("❌ A execução falhou. Verifique os logs no terminal para mais detalhes.")
                        
                        else:
                            # Modo rápido sem logs
                            with logs_container.container():
                                st.info("💡 **Modo Rápido Ativo**\n\nExecução direta sem logs detalhados.")
                                
                            result = crew_manager.execute_crew_safe(selected_crew, inputs=task_inputs)
                            
                            with result_container.container():
                                if result:
                                    st.success("✅ Execução concluída com sucesso!")
                                    st.markdown(result)
                                else:
                                    st.error("❌ A execução falhou. Tente o modo com logs para mais detalhes.")
                        
                    except Exception as e:
                        with result_container.container():
                            st.error(f"❌ Erro crítico durante a execução: {e}")
                        
                        with logs_container.container():
                            st.error("❌ Não foi possível capturar logs devido ao erro crítico.")

    except Exception as e:
        st.error(f"Erro ao carregar as opções de crew: {e}")

    # Histórico de Execuções
    st.markdown("---")
    st.subheader("📜 Histórico de Execuções")

    try:
        # Buscar histórico do banco de dados
        history = crew_manager.db_manager.get_execution_history()
        
        if not history:
            st.info("Nenhuma execução foi realizada ainda.")
        else:
            # Converter para DataFrame
            history_data = []
            for exec_data in history:
                history_data.append({
                    "ID": exec_data['id'],
                    "Crew": exec_data['crew_name'],
                    "Tópico": exec_data['topic'],
                    "Início": exec_data['start_time'][:19] if exec_data['start_time'] else "N/A",
                    "Duração": exec_data['duration'] or "N/A",
                    "Status": exec_data['status'],
                    "Resultado": exec_data['result'][:100] + "..." if exec_data['result'] and len(exec_data['result']) > 100 else exec_data['result'] or "N/A"
                })
            
            history_df = pd.DataFrame(history_data)
            
            st.dataframe(
                history_df[["Crew", "Tópico", "Início", "Duração", "Status"]],
                use_container_width=True,
                hide_index=True
            )

            # Seleção de execução para detalhes
            if len(history) > 0:
                selected_execution_id = st.selectbox(
                    "Ver detalhes de uma execução anterior",
                    options=[exec_data['id'] for exec_data in history],
                    format_func=lambda id: f"Execução #{id} - {next(exec['crew_name'] for exec in history if exec['id'] == id)} ({next(exec['start_time'][:19] for exec in history if exec['start_time'] and exec['id'] == id)})",
                    index=None,
                    placeholder="Selecione uma execução para ver o resultado"
                )

                if selected_execution_id is not None:
                    # Buscar detalhes da execução
                    execution_details = crew_manager.db_manager.get_execution_details(selected_execution_id)
                    
                    if execution_details:
                        with st.expander(f"Resultado da Execução #{selected_execution_id}", expanded=True):
                            st.markdown(f"**Crew:** {execution_details['crew_name']}")
                            st.markdown(f"**Tópico:** {execution_details['topic']}")
                            st.markdown(f"**Status:** {execution_details['status']}")
                            st.markdown(f"**Duração:** {execution_details['duration']}")
                            
                            # RESUMO DA ATUAÇÃO DOS AGENTES (campo retraído)
                            with st.expander("🔎 Resumo do Fluxo dos Agentes", expanded=False):
                                if execution_details.get('task_results'):
                                    for idx, task_result in enumerate(execution_details['task_results']):
                                        st.markdown(f"**Agente:** {task_result.get('agent_name', 'N/A')}")
                                        st.write(f"- Tarefa: {task_result.get('task_description', 'N/A')}")
                                        st.write(f"- Ferramentas usadas: {task_result.get('tools_used', 'N/A')}")
                                        st.write(f"- Recebeu: {task_result.get('input_info', 'N/A')}")
                                        st.write(f"- Passou para o próximo: {task_result.get('output_info', 'N/A')}")
                                        st.write("---")
                                else:
                                    st.info("Nenhuma informação detalhada dos agentes disponível.")
                                # Agente Avaliador fixo
                                st.markdown("**Agente Avaliador (Qualidade do Processo)**")
                                st.write("- Avaliação do tempo de trabalho de cada agente")
                                st.write("- Importância da atuação de cada agente na tarefa")
                                st.write("- Observações sobre a qualidade do processo")
                            # ...existing code...
                            if execution_details['result']:
                                st.markdown("**Resultado:**")
                                st.markdown(execution_details['result'])
                            
                            if execution_details['error_message']:
                                st.error(f"**Erro:** {execution_details['error_message']}")
                            
                            # Mostrar resultados das tarefas se houver
                            if execution_details.get('task_results'):
                                st.markdown("**Resultados das Tarefas:**")
                                for task_result in execution_details['task_results']:
                                    with st.expander(f"Tarefa: {task_result['task_description'][:50]}...", expanded=False):
                                        st.markdown(f"**Agente:** {task_result['agent_name']}")
                                        st.markdown(f"**Status:** {task_result['task_status']}")
                                        st.markdown(f"**Resultado:** {task_result['task_result']}")
                    else:
                        st.error("Detalhes da execução não encontrados.")
    
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
        st.info("Nenhuma execução foi realizada ainda.")