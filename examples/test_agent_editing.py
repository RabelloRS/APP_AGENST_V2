"""
Exemplo de teste para a funcionalidade de edição de agentes
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para importar o módulo app
sys.path.append(str(Path(__file__).parent.parent))

from app.agents.agent_manager import AgentManager


def test_agent_editing():
    """Testa a funcionalidade de edição de agentes"""

    print("🧪 Testando Funcionalidade de Edição de Agentes")
    print("=" * 60)

    # Criar instância do AgentManager
    manager = AgentManager()

    # Listar agentes disponíveis
    print("\n📋 Agentes disponíveis:")
    for agent_type in manager.list_available_agent_types():
        info = manager.get_agent_info(agent_type)
        if info:
            print("  - " + info["name"] + " (" + agent_type + ")")

    # Testar edição de um agente
    test_agent = "researcher"
    print("\n✏️ Testando edição do agente: " + test_agent)

    # Obter configuração atual
    current_config = manager.get_agent_info(test_agent)
    if current_config:
        print("  Nome atual: " + current_config["name"])
        print("  Função atual: " + current_config["role"])

        # Simular alterações
        new_config = {
            "name": "Pesquisador Avançado",
            "role": "Pesquisador especializado em IA",
            "goal": "Realizar pesquisas detalhadas sobre inteligência artificial",
            "backstory": "Especialista em pesquisa com vasta experiência em IA e machine learning",
            "verbose": True,
            "allow_delegation": True,
            "tools": [],
        }

        print("\n📝 Aplicando alterações...")
        print("  Novo nome: " + new_config["name"])
        print("  Nova função: " + new_config["role"])

        # Aplicar alterações
        success = manager.update_agent_config(test_agent, new_config)

        if success:
            print("✅ Alterações aplicadas com sucesso!")

            # Verificar se as alterações foram salvas
            updated_config = manager.get_agent_info(test_agent)
            if updated_config:
                print("  Nome atualizado: " + updated_config["name"])
                print("  Função atualizada: " + updated_config["role"])

            # Recarregar configurações
            print("\n🔄 Recarregando configurações...")
            if manager.reload_configs():
                print("✅ Configurações recarregadas!")

                # Verificar se as alterações persistiram
                reloaded_config = manager.get_agent_info(test_agent)
                if reloaded_config:
                    print("  Nome após reload: " + reloaded_config["name"])
                    print("  Função após reload: " + reloaded_config["role"])
        else:
            print("❌ Erro ao aplicar alterações!")

    print("\n" + "=" * 60)
    print("✅ Teste concluído!")


if __name__ == "__main__":
    test_agent_editing()
