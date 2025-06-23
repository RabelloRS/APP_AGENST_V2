"""
Gerenciamento de Agentes - Criação e Configuração de Agentes Inteligentes
"""

import streamlit as st
import os

# Ícones personalizados por função
ROLE_ICONS = {
    "Pesquisador Técnico": "🔍",
    "Analista de Dados": "📊",
    "Escritor Técnico": "📝",
    "Revisor Técnico": "✅",
    "Coordenador Técnico": "🧑‍💼",
    "Engenheiro Estrutural": "🏗️",
    "Engenheiro Geotécnico": "🌎",
    "Engenheiro Hidráulico": "💧",
    "Engenheiro de Custos": "💰",
    "Engenheiro de Qualidade": "🎯",
    "Engenheiro de Segurança": "🦺",
    "Engenheiro Ambiental": "🌱",
    "Planejador de Obras": "📆",
    "Especialista em Compras": "🛒",
    "Especialista em BIM": "🏢",
    "Especialista em Sustentabilidade": "♻️",
    "Especialista em Tecnologia": "💡",
    "Especialista Legal": "⚖️",
    "Especialista em Comunicação": "💬",
    "Especialista em Avaliação de Crews CrewAI": "🔎",
    "Avaliador Simples": "🕵️"
}

# Lista de ferramentas padrão do CrewAI detectadas na pasta crewai_tools/tools
CREWAI_DEFAULT_TOOLS = [
    "ai_mind_tool",
    "apify_actors_tool",
    "brave_search_tool",
    "browserbase_load_tool",
    "code_docs_search_tool",
    "code_interpreter_tool",
    "composio_tool",
    "crewai_enterprise_tools",
    "csv_search_tool",
    "dalle_tool",
    "databricks_query_tool",
    "directory_read_tool",
    "directory_search_tool",
    "docx_search_tool",
    "exa_tools",
    "files_compressor_tool",
    "file_read_tool",
    "file_writer_tool",
    "firecrawl_crawl_website_tool",
    "firecrawl_scrape_website_tool",
    "firecrawl_search_tool",
    "github_search_tool",
    "hyperbrowser_load_tool",
    "jina_scrape_website_tool",
    "json_search_tool",
    "linkup",
    "llamaindex_tool",
    "mdx_search_tool",
    "multion_tool",
    "mysql_search_tool",
    "nl2sql",
    "ocr_tool",
    "patronus_eval_tool",
    "pdf_search_tool",
    "pdf_text_writing_tool",
    "pg_search_tool",
    "qdrant_vector_search_tool",
    "rag",
    "scrapegraph_scrape_tool",
    "scrape_element_from_website",
    "scrape_website_tool",
    "scrapfly_scrape_website_tool",
    "selenium_scraping_tool",
    "serpapi_tool",
    "serper_dev_tool",
    "serply_api_tool",
    "snowflake_search_tool",
    "spider_tool",
    "stagehand_tool",
    "tavily_extractor_tool",
    "tavily_search_tool",
    "txt_search_tool",
    "vision_tool",
    "weaviate_tool",
    "website_search",
    "xml_search_tool",
    "youtube_channel_search_tool",
    "youtube_video_search_tool",
    "zapier_action_tool"
]

def show_agents_tab():
    st.set_page_config(page_title="Gerenciar Agentes", layout="wide")
    st.title("Gerenciamento de Agentes Especializados")
    st.info("Gerencie os seus agentes: edite, exclua ou crie novos agentes para sua equipe de engenharia civil.")

    agent_manager = st.session_state.agent_manager
    tools_manager = st.session_state.tools_manager

    # Estado de edição/criação/exclusão
    if "editing_agent" not in st.session_state:
        st.session_state.editing_agent = None
    if "creating_agent" not in st.session_state:
        st.session_state.creating_agent = False
    if "delete_agent" not in st.session_state:
        st.session_state.delete_agent = None

    # Listagem visual dos agentes em cards
    st.subheader("Agentes cadastrados")
    available_agents = agent_manager.list_available_agent_types()
    if not available_agents:
        st.warning("Nenhum agente cadastrado.")
    else:
        cols = st.columns(4)
        for idx, agent_type in enumerate(available_agents):
            info = agent_manager.get_agent_info(agent_type) or {}
            icon = ROLE_ICONS.get(info.get("role", ""), "🤖")
            with cols[idx % 4]:
                with st.expander(f"{icon} {info.get('name', agent_type)}", expanded=False):
                    st.markdown(f"**Função:** {info.get('role', '*Não definida*')}")
                    st.markdown(f"**Objetivo:** {info.get('goal', '*Não definido*')}")
                    st.markdown(f"**História:** {info.get('backstory', '*Não definida*')}")
                    agent_tools = agent_manager.get_agent_tools(agent_type)
                    if agent_tools:
                        st.markdown("**Ferramentas:** " + ', '.join(agent_tools))
                    else:
                        st.markdown("**Ferramentas:** _Nenhuma atribuída_")
                    colb1, colb2 = st.columns(2)
                    with colb1:
                        if st.button("✏️ Editar", key=f"edit_{agent_type}"):
                            st.session_state.editing_agent = agent_type
                            st.session_state.creating_agent = False
                    with colb2:
                        if st.button("🗑️ Excluir", key=f"delete_{agent_type}"):
                            st.session_state.delete_agent = agent_type

    # Confirmação de exclusão
    if st.session_state.delete_agent:
        agent_to_delete = st.session_state.delete_agent
        info = agent_manager.get_agent_info(agent_to_delete) or {}
        st.warning(f"Deseja realmente excluir o agente **{info.get('name', agent_to_delete)}**?", icon="⚠️")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmar Exclusão", key="confirm_delete"):
                try:
                    agent_manager.delete_agent(agent_to_delete)
                    st.success(f"Agente '{info.get('name', agent_to_delete)}' excluído com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao excluir agente: {e}")
                st.session_state.delete_agent = None
                st.experimental_rerun()
        with col2:
            if st.button("Cancelar", key="cancel_delete"):
                st.session_state.delete_agent = None

    # Formulário de criação/edição
    def show_agent_form(form_title, agent_data, edit_key=None):
        with st.form(key="form_create_edit"):
            st.markdown(f"#### {form_title}")
            name = st.text_input("Nome do agente", value=agent_data.get("name", ""))
            role = st.text_input("Função", value=agent_data.get("role", ""))
            goal = st.text_area("Objetivo principal", value=agent_data.get("goal", ""))
            backstory = st.text_area("Histórico/Especialização", value=agent_data.get("backstory", ""))
            # Ferramentas disponíveis
            all_tools = CREWAI_DEFAULT_TOOLS.copy()
            # Adicionar ferramentas customizadas do agente (não-oficiais)
            custom_tools = [t for t in agent_data.get("tools", []) if t not in all_tools]
            all_tools += custom_tools
            # Exibir nomes amigáveis para customizadas
            tool_labels = {t: t for t in CREWAI_DEFAULT_TOOLS}
            for t in custom_tools:
                tool_labels[t] = f"{t} (Customizada)"
            # Seleção: todas as ferramentas do agente
            current_tools = agent_data.get("tools", [])
            selected_tools = st.multiselect(
                "Ferramentas habilitadas",
                options=all_tools,
                default=current_tools,
                format_func=lambda t: tool_labels.get(t, t)
            )
            # Garantir que só ferramentas oficiais serão salvas
            selected_tools = [t for t in selected_tools if t in CREWAI_DEFAULT_TOOLS]
            verbose = st.checkbox("Verbose", value=agent_data.get("verbose", True), help="Habilitar logs detalhados para o agente")
            allow_delegation = st.checkbox("Permitir delegação", value=agent_data.get("allow_delegation", False))
            submitted = st.form_submit_button("Salvar")
            if submitted:
                try:
                    # Atualizar campos do agente
                    agent_type = edit_key or name.strip().lower().replace('ã','a').replace('ç','c').replace(' ', '_')
                    config_ok = agent_manager.update_agent_config(agent_type, {
                        "name": name,
                        "role": role,
                        "goal": goal,
                        "backstory": backstory,
                        "verbose": verbose,
                        "allow_delegation": allow_delegation
                    })
                    # Atualizar ferramentas
                    tools_ok = agent_manager.update_agent_tools(agent_type, list(selected_tools))
                    if config_ok and tools_ok:
                        st.success(f"Agente '{name}' salvo com sucesso!")
                        st.session_state.editing_agent = None
                        st.session_state.creating_agent = False
                        st.rerun()
                    else:
                        st.error("Erro ao salvar agente: verifique as permissões dos arquivos de configuração.")
                except Exception as e:
                    st.error(f"Erro ao salvar agente: {e}")
        if st.button("Cancelar", key="cancel_form"):
            st.session_state.editing_agent = None
            st.session_state.creating_agent = False

    # Botão para criar novo agente
    st.markdown("---")
    if st.button("➕ Adicionar novo agente"):
        st.session_state.creating_agent = True
        st.session_state.editing_agent = None

    if st.session_state.creating_agent:
        show_agent_form("Novo Agente", {
            "name": "",
            "role": "",
            "goal": "",
            "backstory": "",
            "tools": [],
            "verbose": True,
            "allow_delegation": False
        }, edit_key=None)

    if st.session_state.editing_agent:
        agent_key = st.session_state.editing_agent
        info = agent_manager.get_agent_info(agent_key) or {}
        col_form, col_tools = st.columns(2)
        with col_form:
            show_agent_form(f"Editar Agente: {info.get('name', agent_key)}", info, edit_key=agent_key)
        with col_tools:
            st.markdown("#### 🛠️ Tabela de Ferramentas Padrão CrewAI")
            # Dicionário de nomes amigáveis e descrições para algumas ferramentas principais
            TOOLS_PT = {
                "ai_mind_tool": ("Mente de IA (MindsDB)", "Consulta fontes de dados (bancos de dados, etc.) usando linguagem natural, integração com MindsDB."),
                "apify_actors_tool": ("Executor de Atores Apify", "Executa 'Atores' da plataforma Apify para automação web, scraping e extração de dados."),
                "brave_search_tool": ("Busca com Brave", "Realiza buscas na internet utilizando a API do buscador Brave, com foco em privacidade."),
                "browserbase_load_tool": ("Carregador Browserbase", "Automação de navegador em nuvem com recursos como modo stealth e resolução de captchas."),
                "code_docs_search_tool": ("Busca em Docs de Código", "Busca semântica (RAG) em documentações de código online a partir de uma URL."),
                "code_interpreter_tool": ("Intérprete de Código", "Executa código Python 3 de forma segura em ambiente isolado (Docker)."),
                "composio_tool": ("Conector Composio", "Integra e executa ações em centenas de aplicativos de terceiros usando a plataforma Composio."),
                "crewai_enterprise_tools": ("Ferramentas Empresariais", "Conjunto de ferramentas para casos de uso empresariais, integrações corporativas."),
                "csv_search_tool": ("Busca em CSV", "Busca semântica (RAG) em arquivos CSV para extrair informações tabulares."),
                "dalle_tool": ("Gerador de Imagens DALL-E", "Gera imagens a partir de descrições textuais usando a API DALL-E da OpenAI."),
                "databricks_query_tool": ("Consulta Databricks", "Executa consultas SQL em cluster ou warehouse do Databricks."),
                "directory_read_tool": ("Listar Diretório", "Lista recursivamente o conteúdo de um diretório específico."),
                "directory_search_tool": ("Busca em Diretório", "Busca semântica (RAG) em todos os arquivos de um diretório."),
                "docx_search_tool": ("Busca em DOCX", "Busca semântica (RAG) em documentos do Microsoft Word (.docx)."),
                "exa_tools": ("Busca Semântica Exa", "Busca na web com base em significado/contexto usando Exa.ai."),
                "files_compressor_tool": ("Compressor de Arquivos", "Comprime arquivos e diretórios para o formato .zip."),
                "file_read_tool": ("Leitor de Arquivos", "Lê o conteúdo de um arquivo de texto, dado o caminho."),
                "file_writer_tool": ("Escritor de Arquivos", "Escreve conteúdo em um arquivo, podendo criar diretórios."),
                "firecrawl_crawl_website_tool": ("Rastreamento Firecrawl", "Rastreia todas as páginas de um site e converte para markdown ou dados estruturados."),
                "firecrawl_scrape_website_tool": ("Extração Firecrawl", "Extrai o conteúdo de uma única URL e converte para markdown ou dados estruturados."),
                "firecrawl_search_tool": ("Busca com Firecrawl", "Busca e retorna conteúdo das páginas mais relevantes usando Firecrawl."),
                "github_search_tool": ("Busca no GitHub", "Busca semântica (RAG) em repositórios do GitHub."),
                "hyperbrowser_load_tool": ("Carregador Hyperbrowser", "Web scraping/crawling em larga escala usando navegadores headless na Hyperbrowser."),
                "jina_scrape_website_tool": ("Extração com Jina AI", "Extrai o conteúdo principal de uma página web usando a API da Jina AI."),
                "json_search_tool": ("Busca em JSON", "Busca semântica (RAG) em arquivos de formato JSON."),
                "linkup": ("Busca de Vagas LinkUp", "Consulta a API da LinkUp para obter informações sobre vagas de emprego."),
                "llamaindex_tool": ("Ferramenta LlamaIndex", "Permite usar qualquer ferramenta ou motor de consulta do LlamaIndex."),
                "mdx_search_tool": ("Busca em MDX", "Busca semântica (RAG) em arquivos de formato MDX."),
                "multion_tool": ("Navegador Inteligente MultiOn", "Controla um navegador web usando linguagem natural para realizar ações complexas."),
                "mysql_search_tool": ("Busca em MySQL", "Busca semântica (RAG) em tabelas de um banco de dados MySQL."),
                "nl2sql": ("Tradutor NL para SQL", "Converte perguntas em linguagem natural em consultas SQL executáveis."),
                "ocr_tool": ("Reconhecimento de Texto (OCR)", "Extrai texto de imagens usando tecnologia OCR."),
                "patronus_eval_tool": ("Avaliação com Patronus AI", "Executa avaliações de qualidade e segurança em LLMs usando Patronus AI."),
                "pdf_search_tool": ("Busca em PDF", "Busca semântica (RAG) em arquivos PDF."),
                "pdf_text_writing_tool": ("Escrita em PDF", "Adiciona texto em posição específica de um PDF."),
                "pg_search_tool": ("Busca em PostgreSQL", "Busca semântica (RAG) em tabelas de um banco de dados PostgreSQL."),
                "qdrant_vector_search_tool": ("Busca Vetorial Qdrant", "Busca por similaridade semântica em banco Qdrant."),
                "rag": ("Ferramenta RAG", "Consulta base de conhecimento dinâmica criada a partir de diversas fontes."),
                "scrapegraph_scrape_tool": ("Extração com ScrapeGraph", "Extrai conteúdo de sites com base em um prompt usando ScrapeGraph AI."),
                "scrape_element_from_website": ("Extrair Elemento de Site", "Extrai o conteúdo de um elemento HTML específico de uma página."),
                "scrape_website_tool": ("Extrair Conteúdo de Site", "Extrai o conteúdo textual completo de uma página web."),
                "scrapfly_scrape_website_tool": ("Extração com Scrapfly", "Extrai dados de sites usando a API da Scrapfly."),
                "selenium_scraping_tool": ("Extração com Selenium", "Controla um navegador real para extrair dados de sites dinâmicos."),
                "serpapi_tool": ("Busca com SerpApi", "Busca na web e obtém resultados estruturados via API do SerpApi."),
                "serper_dev_tool": ("Busca com Serper.dev", "Busca na internet usando a API do Serper.dev."),
                "serply_api_tool": ("Busca com Serply", "Busca em tempo real no Google usando a API do Serply."),
                "snowflake_search_tool": ("Busca em Snowflake", "Busca semântica e executa consultas SQL em data warehouse Snowflake."),
                "spider_tool": ("Rastreamento com Spider", "Rastreia sites de forma autônoma para coletar dados usando Spider."),
                "stagehand_tool": ("Controle com Stagehand", "Interage com sites e automatiza tarefas de navegador via Stagehand."),
                "tavily_extractor_tool": ("Extrator Tavily", "Extrai conteúdo de URLs usando a API de extração da Tavily."),
                "tavily_search_tool": ("Busca com Tavily", "Busca online otimizadas para LLMs usando a API da Tavily."),
                "txt_search_tool": ("Busca em TXT", "Busca semântica (RAG) em arquivos TXT."),
                "vision_tool": ("Ferramenta de Visão", "Analisa o conteúdo de uma imagem e descreve em texto."),
                "weaviate_tool": ("Busca Vetorial Weaviate", "Busca por similaridade semântica em banco Weaviate."),
                "website_search": ("Busca em Site Específico", "Busca semântica (RAG) dentro do conteúdo de um site ou URL específica."),
                "xml_search_tool": ("Busca em XML", "Busca semântica (RAG) em arquivos de formato XML."),
                "youtube_channel_search_tool": ("Busca em Canal do YouTube", "Busca semântica (RAG) nos vídeos de um canal do YouTube."),
                "youtube_video_search_tool": ("Busca em Vídeo do YouTube", "Busca semântica (RAG) na transcrição de um vídeo do YouTube."),
                "zapier_action_tool": ("Ação Zapier", "Executa ações disponíveis na plataforma Zapier para integração com outros aplicativos."),
            }
            st.markdown("""
            <style>
            .tool-table th, .tool-table td {padding: 6px 12px; border: 1px solid #ccc;}
            .tool-table {border-collapse: collapse; width: 100%; font-size: 0.95em;}
            </style>
            """, unsafe_allow_html=True)
            st.markdown("<table class='tool-table'><tr><th>Nome Amigável</th><th>Nome Técnico</th><th>Descrição</th></tr>" +
                "".join([
                    f"<tr><td>{TOOLS_PT.get(t, (t.replace('_tool','').replace('_',' ').title(), t))[0]}</td>"
                    f"<td><code>{t}</code></td>"
                    f"<td>{TOOLS_PT.get(t, (t, ''))[1] or '---'}</td></tr>"
                    for t in CREWAI_DEFAULT_TOOLS
                ]) + "</table>", unsafe_allow_html=True)

    # Visualização do YAML de configuração
    st.markdown("---")
    st.subheader("📄 Visualizar Configuração Atual (`agents.yaml`)")
    try:
        with open("app/config/agents.yaml", "r", encoding="utf-8") as f:
            st.code(f.read(), language="yaml")
    except Exception as e:
        st.error(f"Erro ao ler arquivo de configuração: {e}")

    st.markdown("---")
    st.caption("Desenvolvido com CrewAI e Streamlit • © 2024")