"""
Exemplo de uso da Crew do WhatsApp para download de arquivos
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager


def main():
    """Exemplo de uso da crew do WhatsApp"""
    
    print("🚀 Iniciando Crew do WhatsApp...")
    
    # Inicializar gerenciadores
    agent_manager = AgentManager()
    task_manager = TaskManager()
    tools_manager = ToolsManager()
    crew_manager = CrewManager(agent_manager, task_manager)
    
    # Configurar tools manager no agent manager
    agent_manager.set_tools_manager(tools_manager)
    
    # Criar crew do WhatsApp
    crew_name = "Crew do WhatsApp"
    agent_types = ["whatsapp_monitor", "file_downloader", "file_organizer"]
    description = "Crew especializada em monitorar grupos do WhatsApp e baixar arquivos"
    
    # Criar a crew
    crew = crew_manager.create_crew(crew_name, agent_types, description)
    
    if crew:
        print("✅ Crew do WhatsApp criada com sucesso!")
        print(f"📋 Nome: {crew_name}")
        print(f"📝 Descrição: {description}")
        print(f"🤖 Agentes: {len(crew.agents)}")
        
        # Adicionar tarefas à crew
        print("\n📋 Adicionando tarefas...")
        
        # Tarefa 1: Monitorar WhatsApp
        success1 = crew_manager.add_task_to_crew(
            crew_name, 
            "whatsapp_monitoring_task", 
            group_name="Grupo de Trabalho"
        )
        
        # Tarefa 2: Baixar arquivos
        success2 = crew_manager.add_task_to_crew(
            crew_name, 
            "file_download_task"
        )
        
        # Tarefa 3: Organizar arquivos
        success3 = crew_manager.add_task_to_crew(
            crew_name, 
            "file_organization_task"
        )
        
        if success1 and success2 and success3:
            print("✅ Todas as tarefas adicionadas com sucesso!")
            print(f"📋 Total de tarefas: {len(crew.tasks)}")
            
            # Executar a crew
            print("\n🔄 Executando crew...")
            
            try:
                result = crew_manager.execute_crew(crew_name)
                if result:
                    print("✅ Crew executada com sucesso!")
                    print(f"📄 Resultado: {result}")
                else:
                    print("❌ Erro na execução da crew")
                    
            except Exception as e:
                print(f"❌ Erro na execução da crew: {str(e)}")
        else:
            print("❌ Erro ao adicionar tarefas à crew")
    
    else:
        print("❌ Erro ao criar crew do WhatsApp")


if __name__ == "__main__":
    main() 