"""
Exemplo de teste para a funcionalidade de gerenciamento de tools
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar o módulo app
sys.path.append(str(Path(__file__).parent.parent))

from app.agents.agent_manager import AgentManager
from app.utils.tools_manager import ToolsManager


def list_available_tools(tools_manager):
    """Lista todas as tools disponíveis por categoria"""
    print("\n📋 Tools disponíveis:")
    tools_by_category = tools_manager.get_tools_by_category()
    for category, tools in tools_by_category.items():
        print("  📁 " + category + ":")
        for tool_name in tools:
            tool_info = tools_manager.get_tool_info(tool_name)
            if tool_info:
                print("    - " + tool_info["name"] + " (" + tool_name + ")")


def list_agents_and_tools(agent_manager, tools_manager):
    """Lista todos os agentes e suas tools atribuídas"""
    print("\n🤖 Agentes e suas tools:")
    for agent_type in agent_manager.list_available_agent_types():
        agent_info = agent_manager.get_agent_info(agent_type)
        agent_name = agent_info.get("name", agent_type) if agent_info else agent_type
        agent_tools = agent_manager.get_agent_tools(agent_type)

        print("  🤖 " + agent_name + " (" + agent_type + "):")
        if agent_tools:
            for tool_name in agent_tools:
                tool_info = tools_manager.get_tool_info(tool_name)
                if tool_info:
                    print(
                        "    - 🔧 "
                        + tool_info["name"]
                        + " ("
                        + tool_info["category"]
                        + ")"
                    )
                else:
                    print("    - ⚠️ " + tool_name + " (não encontrada)")
        else:
            print("    - Nenhuma tool atribuída")


def test_tool_assignment(agent_manager, test_agent):
    """Testa a atribuição de tools a um agente"""
    print("\n⚙️ Testando atribuição de tools...")

    # Obter tools atuais
    current_tools = agent_manager.get_agent_tools(test_agent)
    print("  Tools atuais do " + test_agent + ": " + str(current_tools))

    # Atribuir novas tools
    new_tools = ["read_excel_file", "analyze_excel_similarity", "generate_excel_report"]
    print("  Atribuindo tools: " + str(new_tools))

    success = agent_manager.update_agent_tools(test_agent, new_tools)
    if success:
        print("✅ Tools atribuídas com sucesso!")

        # Verificar se as tools foram salvas
        updated_tools = agent_manager.get_agent_tools(test_agent)
        print("  Tools atualizadas: " + str(updated_tools))

        # Recarregar configurações
        print("\n🔄 Recarregando configurações...")
        if agent_manager.reload_configs():
            print("✅ Configurações recarregadas!")

            # Verificar se as tools persistiram
            reloaded_tools = agent_manager.get_agent_tools(test_agent)
            print("  Tools após reload: " + str(reloaded_tools))
        else:
            print("❌ Erro ao recarregar configurações!")
    else:
        print("❌ Erro ao atribuir tools!")


def test_agent_creation(agent_manager, test_agent):
    """Testa a criação de um agente com tools"""
    print("\n🤖 Testando criação de agente com tools...")

    # Remover agente existente se houver
    if test_agent in agent_manager.agents:
        del agent_manager.agents[test_agent]

    # Criar novo agente
    agent = agent_manager.create_agent(test_agent)
    if agent:
        print("✅ Agente " + test_agent + " criado com sucesso!")
        print("  Tools do agente: " + str(agent.tools))
    else:
        print("❌ Erro ao criar agente " + test_agent)


def test_tools_management():
    """Testa a funcionalidade de gerenciamento de tools"""

    print("🔧 Testando Gerenciamento de Tools")
    print("=" * 60)

    # Criar instâncias dos gerenciadores
    tools_manager = ToolsManager()
    agent_manager = AgentManager()

    # Listar tools disponíveis
    list_available_tools(tools_manager)

    # Listar agentes e suas tools
    list_agents_and_tools(agent_manager, tools_manager)

    # Testar atribuição de tools
    test_agent = "excel_analyst"
    test_tool_assignment(agent_manager, test_agent)

    # Testar criação de agente com tools
    test_agent_creation(agent_manager, test_agent)

    print("\n" + "=" * 60)
    print("✅ Teste concluído!")


if __name__ == "__main__":
    test_tools_management()
