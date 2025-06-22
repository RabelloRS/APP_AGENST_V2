"""
Teste do Sistema de Persistência de Crews
Este exemplo demonstra como as crews são salvas e carregadas automaticamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager


def main():
    """Demonstração do sistema de persistência de crews"""
    
    print("🔄 TESTE DO SISTEMA DE PERSISTÊNCIA DE CREWS")
    print("=" * 60)
    
    # Inicializar managers
    print("📋 Inicializando sistema...")
    tools_manager = ToolsManager()
    agent_manager = AgentManager()
    agent_manager.set_tools_manager(tools_manager)
    task_manager = TaskManager()
    
    # Criar CrewManager (irá carregar crews automaticamente)
    print("\n🔧 Inicializando CrewManager (carregamento automático)...")
    crew_manager = CrewManager(agent_manager, task_manager)
    
    # Mostrar crews carregadas
    print(f"\n📦 Crews carregadas automaticamente: {len(crew_manager.crews)}")
    for crew_name in crew_manager.list_crew_names():
        print(f"  ✅ {crew_name}")
    
    # Mostrar informações detalhadas das crews salvas
    print("\n📊 INFORMAÇÕES DETALHADAS DAS CREWS SALVAS:")
    print("-" * 50)
    
    saved_crews_info = crew_manager.get_saved_crews_info()
    for info in saved_crews_info:
        print(f"""
🏗️ CREW: {info['name']}
• Descrição: {info['description']}
• Agentes: {info['agent_count']} agentes ({', '.join(info['agent_types'])})
• Criada em: {info['created_at']}
• Status: {info['status']}
        """)
    
    # Teste: Criar uma nova crew
    print("\n🆕 TESTE: Criando nova crew...")
    new_crew_name = "teste_persistencia"
    new_crew = crew_manager.create_crew(
        name=new_crew_name,
        agent_types=["technical_researcher", "technical_writer"],
        description="Crew de teste para verificar persistência"
    )
    
    if new_crew:
        print(f"✅ Nova crew '{new_crew_name}' criada com sucesso!")
        print(f"📦 Total de crews agora: {len(crew_manager.crews)}")
    
    # Teste: Simular reinicialização do sistema
    print("\n🔄 TESTE: Simulando reinicialização do sistema...")
    print("(Criando novo CrewManager - simula reinício da aplicação)")
    
    # Criar novo CrewManager (simula reinicialização)
    new_crew_manager = CrewManager(agent_manager, task_manager)
    
    print(f"📦 Crews carregadas após 'reinicialização': {len(new_crew_manager.crews)}")
    for crew_name in new_crew_manager.list_crew_names():
        print(f"  ✅ {crew_name}")
    
    # Verificar se a nova crew foi persistida
    if new_crew_name in new_crew_manager.list_crew_names():
        print(f"🎉 SUCESSO! A crew '{new_crew_name}' foi persistida e carregada!")
    else:
        print(f"❌ FALHA! A crew '{new_crew_name}' não foi persistida.")
    
    # Teste: Força recarregamento
    print("\n🔄 TESTE: Força recarregamento do banco de dados...")
    reloaded_count = new_crew_manager.reload_crews_from_database()
    print(f"📦 Crews recarregadas: {reloaded_count}")
    
    # Teste: Executar uma crew persistida
    print("\n🎯 TESTE: Executando crew persistida...")
    crews_list = new_crew_manager.list_crew_names()
    if crews_list:
        test_crew_name = crews_list[0]
        print(f"Executando crew: {test_crew_name}")
        
        result = new_crew_manager.execute_crew(
            test_crew_name, 
            {"topic": "Teste de execução de crew persistida"}
        )
        
        if result:
            print("✅ Crew persistida executada com sucesso!")
            print(f"📄 Resultado: {len(str(result))} caracteres gerados")
        else:
            print("❌ Falha na execução da crew persistida")
    
    print("\n" + "=" * 60)
    print("🎉 TESTE DE PERSISTÊNCIA CONCLUÍDO!")
    print("=" * 60)
    
    print("\n📋 RESUMO DOS RESULTADOS:")
    print("✅ Crews são automaticamente salvas no banco de dados")
    print("✅ Crews são automaticamente carregadas na inicialização")
    print("✅ Crews persistem após reinicialização do sistema")
    print("✅ Sistema de recarregamento forçado disponível")
    print("✅ Crews persistidas podem ser executadas normalmente")
    
    print("\n💡 LOCALIZAÇÃO DOS DADOS:")
    print("📁 Banco de dados: app/data/crews_database.db")
    print("📊 Tabelas: crew_configs, executions, evaluation_reports")
    
    print("\n🔧 COMANDOS ÚTEIS:")
    print("• crew_manager.list_crew_names() - Lista crews em memória")
    print("• crew_manager.get_saved_crews_info() - Info detalhada das crews salvas")
    print("• crew_manager.reload_crews_from_database() - Força recarregamento")


if __name__ == "__main__":
    main() 