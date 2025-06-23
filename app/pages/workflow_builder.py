import streamlit as st
import yaml
from collections import OrderedDict
import json
import uuid
from pathlib import Path
import tempfile
import subprocess
import re

# --- Page Configuration ---
st.set_page_config(
    page_title="Construtor Visual de Fluxo de Trabalho CrewAI",
    page_icon="🧩",
    layout="wide"
)

# --- App Title and Description ---
st.title("🧩 Construtor Visual de Fluxo de Trabalho CrewAI")
st.markdown("""
Esta aplicação permite que você construa visualmente um fluxo de trabalho (processo) para sua equipe de agentes CrewAI.\
Carregue seus arquivos `agents.yaml` e `tasks.yaml`, selecione as tarefas desejadas, ordene-as e gere o código Python\
para executar sua `Crew`.
""")

# --- Helper Functions ---
def load_yaml_file(uploaded_file):
    """Loads a YAML file and returns its content."""
    if uploaded_file is not None:
        try:
            data = yaml.safe_load(uploaded_file)
            if data is None:
                return {}
            if not isinstance(data, dict):
                st.error("O arquivo YAML deve conter um dicionário no topo (não lista).")
                return {}
            return data
        except yaml.YAMLError as e:
            st.error(f"Erro ao ler o arquivo YAML: {e}")
            return {}
    return {}

def generate_python_code(ordered_tasks, agents_data, tasks_data):
    """Generates the Python code for the CrewAI process."""
    if not ordered_tasks:
        return "# Selecione e ordene as tarefas para gerar o código."

    agent_imports = set()
    tool_imports = set()
    agent_instantiations = []
    task_instantiations = []
    required_agents = set()
    for task_key in ordered_tasks:
        agent_name = tasks_data[task_key].get('agent')
        if agent_name:
            required_agents.add(agent_name)
    all_tools = {}
    for agent_key in required_agents:
        if agent_key in agents_data:
            agent_tools = agents_data[agent_key].get('tools', [])
            for tool_name in agent_tools:
                if tool_name not in all_tools:
                    tool_imports.add(f"from crewai_tools import {tool_name}")
                    all_tools[tool_name] = f"{tool_name.lower().replace('tool', '_')} = {tool_name}()"
    for agent_key in required_agents:
        if agent_key in agents_data:
            agent_info = agents_data[agent_key]
            agent_role = agent_info.get('role', '')
            agent_goal = agent_info.get('goal', '')
            agent_backstory = agent_info.get('backstory', '')
            agent_tools_list = agent_info.get('tools', [])
            tool_instances = [all_tools[t].split(' = ')[0] for t in agent_tools_list if t in all_tools]
            tools_code = ', '.join(tool_instances) if tool_instances else ''
            agent_instantiations.append(f"""
{agent_key} = Agent(
    role=\"{agent_role.strip()}\",
    goal=\"{agent_goal.strip()}\",
    backstory=\"{agent_backstory.strip()}\",
    verbose=True,
    allow_delegation={agent_info.get('allow_delegation', False)},
    tools=[{tools_code}]
)
""")
    for task_key in ordered_tasks:
        if task_key in tasks_data:
            task_info = tasks_data[task_key]
            task_description = task_info.get('description', '').strip()
            task_expected_output = task_info.get('expected_output', '').strip()
            task_agent = task_info.get('agent', '')
            task_instantiations.append(f"""
{task_key} = Task(
    description=f\"\"\"{task_description}\"\"\",
    expected_output=f\"\"\"{task_expected_output}\"\"\",
    agent={task_agent}
)
""")
    code = f"""
# =================================================================
# Código da Crew Gerado pela Aplicação Visual de Fluxo de Trabalho
# =================================================================

import os
from crewai import Agent, Task, Crew, Process

# Defina suas chaves de API (ex: para Serper)
# os.environ[\"SERPER_API_KEY\"] = \"SUA_CHAVE_AQUI\"

# --- 1. Importação das Ferramentas ---
# Adicione aqui as importações de ferramentas necessárias
{'\n'.join(sorted(list(tool_imports)))}

# --- 2. Instanciação das Ferramentas ---
# Instancie as ferramentas que seus agentes irão usar
{chr(10).join(all_tools.values())}

# --- 3. Definição dos Agentes ---
# Defina cada um dos seus agentes com suas configurações
{''.join(agent_instantiations)}

# --- 4. Definição das Tarefas ---
# Crie as tarefas que sua crew irá executar
{''.join(task_instantiations)}

# --- 5. Montagem da Crew ---
# Instancie sua crew com um processo sequencial
# O processo é definido pela ordem das tarefas na lista
crew = Crew(
    agents=[{', '.join(sorted(list(required_agents)))}],
    tasks=[{', '.join(ordered_tasks)}],
    verbose=2,
    process=Process.sequential
)

# --- 6. Execução ---
# Inicie o trabalho da sua crew!
# Para tarefas com placeholders como {{topic}}, você precisará fornecer os inputs
# result = crew.kickoff(inputs={{'topic': 'IA na Engenharia Civil'}})
# print(result)

# Exemplo de como iniciar (descomente e ajuste os inputs):
# try:
#     # Defina os inputs necessários para suas tarefas aqui
#     inputs = {{
#         'topic': 'Impacto da Inteligência Artificial na Engenharia de Estruturas',
#         # Adicione outras variáveis necessárias para suas tarefas
#         # 'project_name': 'Edifício Orion',
#         # 'location': 'São Paulo, SP'
#     }}
#     result = crew.kickoff(inputs=inputs)
#     print("######################")
#     print("## Resultado Final da Crew:")
#     print(result)
# except Exception as e:
#     print(f\"Ocorreu um erro ao executar a crew: {{e}}\")

print("Código da Crew gerado. Descomente e ajuste a seção 'Execução' para iniciar.")

"""
    return code

def extract_placeholders(code):
    """Extrai placeholders do tipo {variavel} ou {{variavel}} do código Python."""
    # Busca por {variavel} e {{variavel}} (não pega chaves duplas do f-string)
    pattern = r"(?<!f)\{\{?([a-zA-Z_][a-zA-Z0-9_]*)\}?\}"
    return sorted(set(re.findall(pattern, code)))

DB_PATH = Path(__file__).parent.parent / "crews_db.json"

def load_crews_db():
    if DB_PATH.exists():
        with open(DB_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_crews_db(crews):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(crews, f, ensure_ascii=False, indent=2)

# --- Sidebar for File Uploads and Workflow ---
with st.sidebar:
    st.header("1. Carregar Arquivos de Configuração")
    agents_file = st.file_uploader("Carregue seu `agents.yaml`", type="yaml")
    tasks_file = st.file_uploader("Carregue seu `tasks.yaml`", type="yaml")
    agents_data = load_yaml_file(agents_file)
    tasks_data = load_yaml_file(tasks_file)
    st.header("2. Ordenar Fluxo de Trabalho")
    if st.button("Limpar seleção de tarefas"):
        st.session_state.selected_tasks = []
        st.session_state.workflow_tasks = []
        st.experimental_rerun()
    if 'workflow_tasks' not in st.session_state:
        st.session_state.workflow_tasks = []
    if tasks_data:
        st.session_state.workflow_tasks = [t for t in st.session_state.workflow_tasks if t in st.session_state.get('selected_tasks', [])]
        for task in st.session_state.get('selected_tasks', []):
            if task not in st.session_state.workflow_tasks:
                st.session_state.workflow_tasks.append(task)
        st.info("Arraste e solte as tarefas para definir a ordem de execução do processo.")
        ordered_tasks = st.data_editor(
            st.session_state.workflow_tasks,
            key="dnd_editor",
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={"value": "Tarefa"},
        )
        st.session_state.workflow_tasks = ordered_tasks.values.flatten().tolist()
    else:
        st.warning("Carregue o arquivo `tasks.yaml` para começar a montar seu fluxo de trabalho.")

# --- Main Content Area ---
if not agents_data or not tasks_data:
    st.info("Aguardando o carregamento dos arquivos `agents.yaml` e `tasks.yaml` na barra lateral...")
else:
    tab1, tab2, tab3 = st.tabs(["📋 Seleção de Tarefas", "🐍 Código da Crew Gerado", "📚 Banco de Crews"])
    with tab1:
        st.header("Selecione as Tarefas para o seu Fluxo de Trabalho")
        if 'selected_tasks' not in st.session_state:
            st.session_state.selected_tasks = []
        agent_tasks = {}
        for task_key, task_details in tasks_data.items():
            agent_name = task_details.get('agent', 'Sem Agente Designado')
            if agent_name not in agent_tasks:
                agent_tasks[agent_name] = []
            agent_tasks[agent_name].append(task_key)
        for agent_name, task_list in sorted(agent_tasks.items()):
            agent_display_name = agents_data.get(agent_name, {}).get('name', agent_name.replace('_', ' ').title())
            with st.expander(f"**{agent_display_name}** (`{agent_name}`)"):
                for task_key in task_list:
                    task_info = tasks_data[task_key]
                    is_selected = st.checkbox(
                        f"**{task_key}**", 
                        key=f"cb_{task_key}",
                        value=task_key in st.session_state.selected_tasks,
                        help=task_info.get('description', 'Sem descrição.')
                    )
                    st.caption(task_info.get('description', 'Sem descrição.'))
                    st.markdown("---")
                    if is_selected and task_key not in st.session_state.selected_tasks:
                        st.session_state.selected_tasks.append(task_key)
                        st.experimental_rerun()
                    elif not is_selected and task_key in st.session_state.selected_tasks:
                        st.session_state.selected_tasks.remove(task_key)
                        st.experimental_rerun()
    with tab2:
        st.header("Código Python para Executar sua Crew")
        ordered_tasks_final = st.session_state.get('workflow_tasks', [])
        if not ordered_tasks_final:
            st.warning("Nenhuma tarefa foi selecionada ou ordenada no fluxo de trabalho. Selecione as tarefas na aba anterior e ordene-as na barra lateral.")
        else:
            st.info("Este código representa a estrutura da sua Crew. Você precisará preencher as variáveis (placeholders como {topic}) ao executá-lo.")
            python_code = generate_python_code(ordered_tasks_final, agents_data, tasks_data)
            st.code(python_code, language="python")
            st.download_button(
                label="Baixar Código Python",
                data=python_code,
                file_name="crewai_workflow.py",
                mime="text/x-python"
            )
            with st.form("save_crew_form"):
                crew_name = st.text_input("Nome para este workflow/crew", value="Crew personalizada")
                crew_desc = st.text_area("Descrição (opcional)", value="")
                if st.form_submit_button("Salvar no Banco de Crews"):
                    crews = load_crews_db()
                    crew_id = str(uuid.uuid4())
                    crews.append({
                        "id": crew_id,
                        "name": crew_name,
                        "desc": crew_desc,
                        "tasks": ordered_tasks_final,
                        "code": python_code
                    })
                    save_crews_db(crews)
                    st.success(f"Workflow salvo como '{crew_name}'!")
    with tab3:
        st.header("Banco de Crews Salvas")
        crews = load_crews_db()
        if not crews:
            st.info("Nenhuma crew/workflow salva ainda.")
        else:
            for crew in crews:
                with st.expander(f"{crew['name']} ({crew['id'][:8]})"):
                    st.markdown(f"**Descrição:** {crew.get('desc','-')}")
                    st.markdown(f"**Tarefas:** {', '.join(crew.get('tasks', []))}")
                    with st.expander("Ver código Python"):
                        st.code(crew['code'], language="python")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"Excluir", key=f"del_{crew['id']}"):
                            crews = [c for c in crews if c['id'] != crew['id']]
                            save_crews_db(crews)
                            st.success("Crew excluída!")
                            st.experimental_rerun()
                    with col2:
                        # --- Inputs dinâmicos para placeholders ---
                        placeholders = extract_placeholders(crew['code'])
                        if st.button(f"Executar (experimental)", key=f"run_{crew['id']}") or st.session_state.get(f'run_form_{crew['id']}', False):
                            if placeholders:
                                st.session_state[f'run_form_{crew['id']}'] = True
                                with st.form(f"form_inputs_{crew['id']}"):
                                    st.info("Preencha os valores para os inputs necessários:")
                                    input_values = {}
                                    for ph in placeholders:
                                        input_values[ph] = st.text_input(f"{ph}", key=f"input_{crew['id']}_{ph}")
                                    submitted = st.form_submit_button("Executar com estes inputs")
                                    if submitted:
                                        code_to_run = crew['code']
                                        for ph, val in input_values.items():
                                            code_to_run = re.sub(rf"\{{{{{ph}}}}}", val, code_to_run)
                                            code_to_run = re.sub(rf"\{{{ph}\}}", val, code_to_run)
                                        st.session_state[f'run_form_{crew['id']}'] = False
                                        st.info("Executando código Python da crew em subprocesso isolado...")
                                        with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmpf:
                                            tmpf.write(code_to_run)
                                            tmp_path = tmpf.name
                                        try:
                                            result = subprocess.run([
                                                "python", tmp_path
                                            ], capture_output=True, text=True, timeout=120)
                                            st.subheader("Saída (stdout):")
                                            st.code(result.stdout or "(sem saída)", language="text")
                                            st.subheader("Erros (stderr):")
                                            st.code(result.stderr or "(sem erros)", language="text")
                                        except subprocess.TimeoutExpired:
                                            st.error("Execução excedeu o tempo limite (120s).")
                                        except Exception as e:
                                            st.error(f"Erro ao executar o código: {e}")
                                        finally:
                                            try:
                                                Path(tmp_path).unlink(missing_ok=True)
                                            except Exception:
                                                pass
                            else:
                                st.info("Executando código Python da crew em subprocesso isolado...")
                                with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmpf:
                                    tmpf.write(crew['code'])
                                    tmp_path = tmpf.name
                                try:
                                    result = subprocess.run([
                                        "python", tmp_path
                                    ], capture_output=True, text=True, timeout=120)
                                    st.subheader("Saída (stdout):")
                                    st.code(result.stdout or "(sem saída)", language="text")
                                    st.subheader("Erros (stderr):")
                                    st.code(result.stderr or "(sem erros)", language="text")
                                except subprocess.TimeoutExpired:
                                    st.error("Execução excedeu o tempo limite (120s).")
                                except Exception as e:
                                    st.error(f"Erro ao executar o código: {e}")
                                finally:
                                    try:
                                        Path(tmp_path).unlink(missing_ok=True)
                                    except Exception:
                                        pass
                    with col3:
                        if st.button(f"Duplicar", key=f"dup_{crew['id']}"):
                            crews = load_crews_db()
                            new_crew = crew.copy()
                            new_crew['id'] = str(uuid.uuid4())
                            new_crew['name'] = f"{crew['name']} (Cópia)"
                            crews.append(new_crew)
                            save_crews_db(crews)
                            st.success("Workflow duplicado! Edite conforme necessário.")
                            st.experimental_rerun()
                        if st.button(f"Editar", key=f"edit_{crew['id']}") or st.session_state.get(f'edit_form_{crew['id']}', False):
                            st.session_state[f'edit_form_{crew['id']}'] = True
                            with st.form(f"form_edit_{crew['id']}"):
                                new_name = st.text_input("Nome do workflow", value=crew['name'], key=f"edit_name_{crew['id']}")
                                new_desc = st.text_area("Descrição", value=crew.get('desc',''), key=f"edit_desc_{crew['id']}")
                                new_tasks = st.text_area("Tarefas (separadas por vírgula)", value=", ".join(crew.get('tasks', [])), key=f"edit_tasks_{crew['id']}")
                                new_code = st.text_area("Código Python", value=crew['code'], height=300, key=f"edit_code_{crew['id']}")
                                submitted = st.form_submit_button("Salvar alterações")
                                if submitted:
                                    crews = load_crews_db()
                                    for c in crews:
                                        if c['id'] == crew['id']:
                                            c['name'] = new_name
                                            c['desc'] = new_desc
                                            c['tasks'] = [t.strip() for t in new_tasks.split(',') if t.strip()]
                                            c['code'] = new_code
                                            break
                                    save_crews_db(crews)
                                    st.session_state[f'edit_form_{crew['id']}'] = False
                                    st.success("Workflow editado com sucesso!")
                                    st.experimental_rerun()
