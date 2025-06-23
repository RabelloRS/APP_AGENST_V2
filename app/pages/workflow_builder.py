import streamlit as st
import yaml
import uuid
from app.utils.database import DatabaseManager
import re
import os
import tempfile
import subprocess
import sys


def show_workflow_builder():
    # --- Page Configuration ---
    st.set_page_config(page_title="Construtor Visual de Fluxo de Trabalho CrewAI", page_icon="🧩", layout="wide")

    # --- App Title and Description ---
    st.title("🧩 Construtor Visual de Fluxo de Trabalho CrewAI")
    st.markdown(
        """
Esta aplicação permite que você construa visualmente um fluxo de trabalho (processo) para sua equipe de agentes CrewAI.
Os arquivos `agents.yaml` e `tasks.yaml` são carregados automaticamente. Selecione as tarefas, ordene-as e gere, salve ou execute o código Python.
"""
    )

    db = DatabaseManager()

    def export_crews_summary():
        """Exporta um resumo das crews do banco para JSON resumido."""
        import json
        crews = db.get_all_crew_configs()
        resumido = [
            {
                "name": c.get("crew_name"),
                "desc": c.get("description", ""),
                "tasks": c.get("task_types", []),
                "agents": c.get("agent_types", [])
            }
            for c in crews
        ]
        with open("app/crews_db_resumido.json", "w", encoding="utf-8") as f2:
            json.dump(resumido, f2, ensure_ascii=False, indent=2)

    # --- Carregar arquivos de configuração automaticamente ---
    try:
        agents_file_path = "app/config/agents.yaml"
        tasks_file_path = "app/config/tasks.yaml"
        with open(agents_file_path, "r", encoding="utf-8") as f:
            agents_data = yaml.safe_load(f) or {}
        with open(tasks_file_path, "r", encoding="utf-8") as f:
            tasks_data = yaml.safe_load(f) or {}
    except FileNotFoundError as e:
        st.error(f"❌ Arquivo de configuração não encontrado: {e.filename}.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivos de configuração: {e}")
        st.stop()

    # --- Helper Function for Code Generation ---
    def generate_python_code(ordered_tasks, agents_data, tasks_data):
        if not ordered_tasks: return "# Selecione e ordene as tarefas para gerar o código."
        native_tool_class_map = {'BraveSearchTool': 'BraveSearchTool', 'SerperDevTool': 'SerperDevTool', 'EXASearchTool': 'EXASearchTool','LinkupSearchTool': 'LinkupSearchTool', 'GithubSearchTool': 'GithubSearchTool','PDFSearchTool': 'PDFSearchTool', 'WebsiteSearchTool': 'WebsiteSearchTool', 'CodeDocsSearchTool': 'CodeDocsSearchTool','CSVSearchTool': 'CSVSearchTool', 'JSONSearchTool': 'JSONSearchTool', 'MDXSearchTool': 'MDXSearchTool','DOCXSearchTool': 'DOCXSearchTool', 'XMLSearchTool': 'XMLSearchTool', 'ScrapflyScrapeWebsiteTool': 'ScrapflyScrapeWebsiteTool','FirecrawlCrawlWebsiteTool': 'FirecrawlCrawlWebsiteTool', 'FirecrawlSearchTool': 'FirecrawlSearchTool', 'SeleniumScrapingTool': 'SeleniumScrapingTool','AIMindTool': 'AIMindTool', 'VisionTool': 'VisionTool', 'LlamaIndexTool': 'LlamaIndexTool', 'CodeInterpreterTool': 'CodeInterpreterTool','QdrantVectorSearchTool': 'QdrantVectorSearchTool', 'WeaviateVectorSearchTool': 'WeaviateVectorSearchTool','NL2SQLTool': 'NL2SQLTool', 'MySQLSearchTool': 'MySQLSearchTool', 'PGSearchTool': 'PGSearchTool','ApifyActorsTool': 'ApifyActorsTool', 'MultiOnTool': 'MultiOnTool', 'StagehandTool': 'StagehandTool','FileReadTool': 'FileReadTool', 'FileWriterTool': 'FileWriterTool', 'DirectoryReadTool': 'DirectoryReadTool',}
        tools_requiring_config = {'BraveSearchTool': 'BRAVE_API_KEY', 'SerperDevTool': 'SERPER_API_KEY', 'EXASearchTool': 'EXA_API_KEY','LinkupSearchTool': 'LINKUP_API_KEY', 'GithubSearchTool': ['GH_TOKEN'],'ScrapflyScrapeWebsiteTool': 'SCRAPFLY_API_KEY', 'FirecrawlCrawlWebsiteTool': 'FIRECRAWL_API_KEY','FirecrawlSearchTool': 'FIRECRAWL_API_KEY', 'AIMindTool': 'MINDS_API_KEY','QdrantVectorSearchTool': ['QDRANT_API_KEY', 'QDRANT_URL', 'OPENAI_API_KEY'],'WeaviateVectorSearchTool': ['WEAVIATE_API_KEY', 'WEAVIATE_CLUSTER_URL', 'OPENAI_API_KEY'],'ApifyActorsTool': 'APIFY_API_TOKEN', 'MultiOnTool': 'MULTION_API_KEY','StagehandTool': ['BROWSERBASE_API_KEY', 'BROWSERBASE_PROJECT_ID', 'OPENAI_API_KEY'],'PDFSearchTool': 'OPENAI_API_KEY', 'WebsiteSearchTool': 'OPENAI_API_KEY','CodeDocsSearchTool': 'OPENAI_API_KEY', 'CSVSearchTool': 'OPENAI_API_KEY','JSONSearchTool': 'OPENAI_API_KEY', 'MDXSearchTool': 'OPENAI_API_KEY','DOCXSearchTool': 'OPENAI_API_KEY', 'XMLSearchTool': 'OPENAI_API_KEY', 'VisionTool': 'OPENAI_API_KEY','NL2SQLTool': ['DB_URI'], 'MySQLSearchTool': ['DB_URI'], 'PGSearchTool': ['DB_URI'],}
        tool_imports, agent_instantiations, task_instantiations, tool_instantiations, api_keys_needed = set(), [], [], {}, set()
        required_agents = {tasks_data[tk].get("agent") for tk in ordered_tasks if tasks_data[tk].get("agent")}

        def get_tool_instantiation_code(tool_name, class_name):
            tool_var = f"{tool_name.lower()}_tool"
            if tool_name == 'GithubSearchTool': return f'{tool_var} = {class_name}(gh_token=os.getenv("GH_TOKEN"), content_types=["code", "issue"])'
            if 'DB_URI' in tools_requiring_config.get(tool_name, []): return f'{tool_var} = {class_name}(db_uri=os.getenv("DB_URI"))'
            api_key_env = tools_requiring_config.get(tool_name)
            if api_key_env and isinstance(api_key_env, str): return f'{tool_var} = {class_name}(api_key=os.getenv("{api_key_env}"))'
            return f'{tool_var} = {class_name}()'

        for agent_key in required_agents:
            if agent_key in agents_data:
                for tool_name in agents_data[agent_key].get("tools", []):
                    if tool_name in native_tool_class_map:
                        class_name = native_tool_class_map[tool_name]
                        tool_imports.add(f"from crewai_tools import {class_name}")
                        if tool_name not in tool_instantiations: tool_instantiations[tool_name] = get_tool_instantiation_code(tool_name, class_name)
                    else:
                        tool_imports.add(f"from app.utils.tools import {tool_name}")
                        if tool_name not in tool_instantiations: tool_instantiations[tool_name] = f"{tool_name.lower()}_tool = {tool_name}()"
                    if tool_name in tools_requiring_config:
                        keys = tools_requiring_config[tool_name]
                        api_keys_needed.update(keys if isinstance(keys, list) else [keys])

        for agent_key in required_agents:
            if agent_key in agents_data:
                agent_info = agents_data[agent_key]
                agent_tools_vars = [f"{t.lower()}_tool" for t in agent_info.get("tools", [])]
                tools_code = f"tools=[{', '.join(agent_tools_vars)}]" if agent_tools_vars else ""
                agent_instantiations.append(f"""\n{agent_key} = Agent(role="{agent_info.get("role", "")}", goal='''{agent_info.get("goal", "")}''', backstory='''{agent_info.get("backstory", "")}''', verbose=True, allow_delegation={agent_info.get('allow_delegation', False)}, {tools_code})""")

        placeholders = set()
        for task_key in ordered_tasks:
            if task_key in tasks_data:
                task_info = tasks_data[task_key]
                desc, exp_out = task_info.get("description", ""), task_info.get("expected_output", "")
                placeholders.update(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", desc + exp_out))
                task_instantiations.append(f"""\n{task_key} = Task(description='''{desc}''', expected_output='''{exp_out}''', agent={task_info.get("agent", "None")})""")
        
        if placeholders:
            inputs_example_str = "\n" + "".join([f"        '{ph}': 'Valor para {ph}',\n" for ph in sorted(list(placeholders))]) + "    "
            inputs_example = f"inputs = {{{inputs_example_str}}}"
        else:
            inputs_example = "inputs = {}"
        
        return f"""import os, sys\nfrom crewai import Agent, Task, Crew, Process\nfrom dotenv import load_dotenv\n\n# 1. Carregamento de Chaves de API\nload_dotenv()\n# ATENÇÃO: Verifique se as seguintes variáveis estão no seu .env: {', '.join(sorted(list(api_keys_needed)))}\n\n# 2. Importação das Ferramentas\n{"\n".join(sorted(list(tool_imports)))}\n\n# 3. Instanciação das Ferramentas\n{"\n".join(tool_instantiations.values())}\n\n# 4. Definição dos Agentes\n{''.join(agent_instantiations)}\n\n# 5. Definição das Tarefas\n{''.join(task_instantiations)}\n\n# 6. Montagem da Crew\ncrew = Crew(\n    agents=[{', '.join(sorted(list(required_agents)))}],\n    tasks=[{', '.join(ordered_tasks)}],\n    verbose=2,\n    process=Process.sequential\n)\n\n# 7. Execução\nif __name__ == "__main__":\n    print("🚀 Iniciando a execução da Crew...")\n    sys.stdout.flush()\n    {inputs_example}\n    result = crew.kickoff(inputs=inputs)\n    print("\\n########################")\n    print("## ✅ Resultado Final da Crew:")\n    print(result)\n    print("########################")\n    sys.stdout.flush()\n"""

    # --- Lógica da Interface Streamlit ---
    if "selected_tasks" not in st.session_state: st.session_state.selected_tasks = []
    if "workflow_tasks" not in st.session_state: st.session_state.workflow_tasks = []

    with st.sidebar:
        st.header("1. Ordenar Fluxo de Trabalho")
        current_selection = set(st.session_state.get("selected_tasks", []))
        st.session_state.workflow_tasks = [t for t in st.session_state.workflow_tasks if t in current_selection]
        for task in st.session_state.get("selected_tasks", []):
            if task not in st.session_state.workflow_tasks: st.session_state.workflow_tasks.append(task)
        ordered_tasks = st.data_editor(st.session_state.workflow_tasks, key="dnd_editor", use_container_width=True, num_rows="dynamic", hide_index=True, column_config={"value": "Tarefa"})
        st.session_state.workflow_tasks = ordered_tasks if isinstance(ordered_tasks, list) else ordered_tasks.values.flatten().tolist()
        st.markdown("---")
        st.info("A seleção e a ordem são salvas automaticamente.")

    tab1, tab2 = st.tabs(["📋 Seleção de Tarefas", "🐍 Código e Execução"])

    with tab1:
        st.header("Selecione as Tarefas para o Fluxo de Trabalho")
        agent_tasks = {}
        for task_key, task_details in tasks_data.items():
            agent_name = task_details.get("agent", "Sem Agente")
            if agent_name not in agent_tasks: agent_tasks[agent_name] = []
            agent_tasks[agent_name].append(task_key)
        agent_list, num_cols = sorted(agent_tasks.items()), min(4, len(agent_tasks))
        cols = st.columns(num_cols) if num_cols > 0 else [st]
        for i, (agent_name, task_list) in enumerate(agent_list):
            with cols[i % num_cols]:
                role = agents_data.get(agent_name, {}).get("role", agent_name)
                with st.expander(f"**Agente: {role}**"):
                    for task_key in task_list:
                        if st.checkbox(f"{task_key}", key=f"cb_{task_key}", value=task_key in st.session_state.selected_tasks, help=tasks_data[task_key].get("description"), on_change=lambda tk=task_key: (st.session_state.selected_tasks.append(tk) if tk not in st.session_state.selected_tasks else st.session_state.selected_tasks.remove(tk))): pass
                        st.caption(tasks_data[task_key].get("description"))

    with tab2:
        st.header("Código e Ações do Workflow")
        ordered_tasks_final = st.session_state.get("workflow_tasks", [])
        if not ordered_tasks_final:
            st.warning("Nenhuma tarefa selecionada. Volte para a aba 'Seleção de Tarefas'.")
        else:
            python_code = generate_python_code(ordered_tasks_final, agents_data, tasks_data)
            placeholders = extract_placeholders(python_code)

            action_cols = st.columns(2)
            with action_cols[0]:
                with st.form("save_crew_form"):
                    workflow_name = st.text_input("Nome para salvar o Workflow", "Minha Crew Personalizada")
                    if st.form_submit_button("💾 Salvar Workflow", use_container_width=True):
                        # Salvar workflow no banco de dados
                        db.save_crew_config(
                            workflow_name,
                            '',  # descrição pode ser expandida
                            [],  # lista de agentes pode ser expandida
                            ordered_tasks_final
                        )
                        export_crews_summary()
                        st.success(f"Workflow '{workflow_name}' salvo no banco de dados!")

            with action_cols[1]:
                with st.form("execute_crew_form"):
                    st.write("**Executar Workflow Diretamente**")
                    inputs = {ph: st.text_input(f"Valor para `{ph}`", key=f"exec_in_{ph}") for ph in placeholders}
                    submitted = st.form_submit_button("▶️ Executar Agora", use_container_width=True, type="primary")

            if submitted:
                # --- CORREÇÃO APLICADA AQUI: LÓGICA DE ESCAPE E EXECUÇÃO ---
                inputs_str_parts = []
                for k, v in inputs.items():
                    escaped_v = v.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
                    inputs_str_parts.append(f"        '{k}': '{escaped_v}'")
                
                if inputs_str_parts:
                    inputs_str = "{\n" + ",\n".join(inputs_str_parts) + "\n    }"
                else:
                    inputs_str = "{}"
                
                # Usamos um marcador único para substituição segura
                placeholder_marker = "#<--INPUTS_PLACEHOLDER-->"
                code_with_marker = re.sub(r"inputs = \{.*?\}", placeholder_marker, python_code, flags=re.DOTALL)
                code_to_run = code_with_marker.replace(placeholder_marker, f"inputs = {inputs_str}")

                log_container = st.empty()
                log_output = ""
                st.info("Executando a Crew... Acompanhe o progresso abaixo.")
                
                with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmpf:
                    tmpf.write(code_to_run)
                    tmp_path = tmpf.name
                
                proc = None
                try:
                    # Usamos Popen para ter controle sobre o processo
                    proc = subprocess.Popen(
                        [sys.executable, "-u", tmp_path],  # Usar sys.executable garante o mesmo ambiente python
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding='utf-8',
                        # Flag para não criar uma janela de console no Windows
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                    )

                    # Lendo a saída em tempo real
                    while True:
                        line = proc.stdout.readline()
                        if not line:
                            break
                        log_output += line
                        log_container.code(log_output, language="log")
                    
                    proc.wait()

                    if proc.returncode == 0:
                        st.success("Execução da Crew finalizada com sucesso!")
                    else:
                        st.error(f"O processo da Crew finalizou com um código de erro: {proc.returncode}")

                except Exception as e:
                     st.error(f"Ocorreu um erro ao tentar executar o processo: {e}")
                finally:
                    if proc and proc.poll() is None: proc.kill()
                    os.unlink(tmp_path)
            
            st.markdown("---")
            st.subheader("Código Python Gerado")
            st.code(python_code, language="python")
            st.download_button("⬇️ Baixar Código (main.py)", python_code, "main.py", "text/x-python")

def extract_placeholders(code):
        return sorted(list(set(re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", code))))

if __name__ == "__main__":
    show_workflow_builder()