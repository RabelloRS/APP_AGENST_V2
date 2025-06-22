"""
Teste de criação de agentes com tools funcionais

Desenvolvido pela Propor Engenharia
Responsável Técnico: Eng. Civil Rodrigo Emanuel Rabello
CREA-RS: 167.175-D | CNPJ: 41.556.670/0001-76
"""

from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager


def test_agent_creation():
    """Testa a criação de agentes com tools"""

    print("🧪 Testando criação de agentes com tools...")
    print("=" * 60)

    # 1. Inicializar gerenciadores
    print("1. Inicializando gerenciadores...")
    tools_manager = ToolsManager()
    agent_manager = AgentManager()
    task_manager = TaskManager()

    # 2. Conectar ToolsManager ao AgentManager
    print("2. Conectando ToolsManager ao AgentManager...")
    agent_manager.set_tools_manager(tools_manager)

    # 3. Verificar tools disponíveis
    print("3. Tools disponíveis:")
    available_tools = tools_manager.list_available_tools()
    for tool in available_tools:
        tool_info = tools_manager.get_tool_info(tool)
        if tool_info:
            print(f"   - {tool}: {tool_info.get('description', 'Sem descrição')}")
        else:
            print(f"   - {tool}: Informações não encontradas")

    # 4. Testar criação de agentes
    print("\n4. Testando criação de agentes...")
    test_agents = ["researcher", "analyst", "writer", "excel_analyst"]

    created_agents = {}
    for agent_type in test_agents:
        print(f"   Criando agente: {agent_type}")
        agent = agent_manager.create_agent(agent_type)
        if agent:
            created_agents[agent_type] = agent
            tools_count = (
                len(agent.tools) if hasattr(agent, "tools") and agent.tools else 0
            )
            print(f"   ✅ {agent_type} criado com {tools_count} tools")
        else:
            print(f"   ❌ Erro ao criar {agent_type}")

    # 5. Verificar tools dos agentes criados
    print("\n5. Verificando tools dos agentes:")
    for agent_type, agent in created_agents.items():
        if hasattr(agent, "tools") and agent.tools:
            print(f"   {agent_type}: {len(agent.tools)} tools")
            for tool in agent.tools:
                print(f"     - {tool.name}: {tool.description}")
        else:
            print(f"   {agent_type}: Nenhuma tool")

    # 6. Testar criação de crew
    print("\n6. Testando criação de crew...")
    crew_manager = CrewManager(agent_manager, task_manager)

    crew = crew_manager.create_crew(
        "Test Crew", ["researcher", "analyst"], "Crew de teste"
    )

    if crew:
        print(f"   ✅ Crew criada com {len(crew.agents)} agentes")
        print(f"   ✅ Agentes na crew: {[agent.role for agent in crew.agents]}")
    else:
        print("   ❌ Erro ao criar crew")

    return len(created_agents) > 0


def test_excel_analysis_crew():
    """Testa a criação de uma crew específica para análise de Excel"""

    print("\n🧪 Testando crew de análise de Excel...")
    print("=" * 60)

    # Inicializar gerenciadores
    tools_manager = ToolsManager()
    agent_manager = AgentManager()
    task_manager = TaskManager()
    agent_manager.set_tools_manager(tools_manager)

    # Criar agente excel_analyst
    excel_agent = agent_manager.create_agent("excel_analyst")
    if excel_agent:
        tools_count = (
            len(excel_agent.tools)
            if hasattr(excel_agent, "tools") and excel_agent.tools
            else 0
        )
        print(f"✅ Agente excel_analyst criado com {tools_count} tools")

        # Verificar se tem as tools corretas
        expected_tools = [
            "read_excel_column",
            "read_excel_file",
            "analyze_excel_similarity",
        ]
        agent_tool_names = (
            [tool.name for tool in excel_agent.tools]
            if hasattr(excel_agent, "tools") and excel_agent.tools
            else []
        )

        for expected_tool in expected_tools:
            if expected_tool in agent_tool_names:
                print(f"   ✅ Tool {expected_tool} presente")
            else:
                print(f"   ❌ Tool {expected_tool} ausente")

        # Criar crew
        crew_manager = CrewManager(agent_manager, task_manager)
        crew = crew_manager.create_crew(
            "Excel Analysis Crew",
            ["excel_analyst"],
            "Crew especializada em análise de planilhas Excel",
        )

        if crew:
            print("✅ Crew de análise de Excel criada com sucesso!")
            return True
        else:
            print("❌ Erro ao criar crew de análise de Excel")
            return False
    else:
        print("❌ Erro ao criar agente excel_analyst")
        return False


if __name__ == "__main__":
    print("🏗️ Teste de Agentes de Engenharia da Propor")
    print("📞 Propor Engenharia - Eng. Civil Rodrigo Emanuel Rabello")
    print("=" * 60)

    # Executar testes
    success1 = test_agent_creation()
    success2 = test_excel_analysis_crew()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 Todos os testes passaram!")
        print("✅ Sistema de agentes funcionando corretamente")
    else:
        print("⚠️ Alguns testes falharam")
        print("❌ Verifique os logs acima para identificar problemas")

    print("\n💡 Para executar a aplicação completa:")
    print("   streamlit run app/main.py")
