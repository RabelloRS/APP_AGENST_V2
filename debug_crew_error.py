#!/usr/bin/env python3
"""
Script de debug para reproduzir o erro '_type' ao criar crews
"""

import sys
import os

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def debug_crew_creation():
    """Debug da criação de crews para identificar o erro '_type'"""
    try:
        from agents.agent_manager import AgentManager
        from crews.crew_manager import CrewManager
        from crews.task_manager import TaskManager
        
        print("🔍 Debug: Iniciando teste de criação de crew...")
        
        # 1. Criar agent manager
        agent_manager = AgentManager()
        
        # 2. Criar task manager
        task_manager = TaskManager()
        
        # 3. Criar crew manager
        crew_manager = CrewManager(agent_manager, task_manager)
        
        print("✅ Managers criados com sucesso")
        
        # 4. Testar criação de crew simples (sem tarefas)
        print("\n🔍 Testando criação de crew simples...")
        crew = crew_manager.create_crew(
            name="debug_crew",
            agent_types=["technical_researcher", "data_analyst"],
            description="Crew de debug"
        )
        
        if crew:
            print("✅ Crew simples criada com sucesso!")
            print(f"   Agentes: {len(crew.agents)}")
            print(f"   Tarefas: {len(crew.tasks)}")
        else:
            print("❌ Falha ao criar crew simples")
            return False
        
        # 5. Testar criação de crew com tarefas (onde ocorre o erro '_type')
        print("\n🔍 Testando criação de crew com tarefas...")
        crew_with_tasks = crew_manager.create_crew_with_tasks(
            name="debug_crew_with_tasks",
            agent_types=["technical_researcher", "data_analyst"],
            task_types=["research_task", "analysis_task"],
            description="Crew de debug com tarefas"
        )
        
        if crew_with_tasks:
            print("✅ Crew com tarefas criada com sucesso!")
            print(f"   Agentes: {len(crew_with_tasks.agents)}")
            print(f"   Tarefas: {len(crew_with_tasks.tasks)}")
            return True
        else:
            print("❌ Falha ao criar crew com tarefas")
            return False
        
    except Exception as e:
        print(f"❌ Erro geral no debug: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_task_creation():
    """Debug específico da criação de tarefas"""
    try:
        from agents.agent_manager import AgentManager
        from crews.task_manager import TaskManager
        
        print("\n🔍 Debug: Testando criação de tarefas...")
        
        agent_manager = AgentManager()
        task_manager = TaskManager()
        
        # Criar um agente
        agent = agent_manager.create_agent('technical_researcher')
        if not agent:
            print("❌ Falha ao criar agente para teste")
            return False
        
        print("✅ Agente criado para teste")
        
        # Testar criação de tarefa
        task = task_manager.create_task_with_params(
            task_type="research_task",
            agent=agent,
            topic="teste"
        )
        
        if task:
            print("✅ Tarefa criada com sucesso!")
            return True
        else:
            print("❌ Falha ao criar tarefa")
            return False
        
    except Exception as e:
        print(f"❌ Erro na criação de tarefa: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal de debug"""
    print("🚀 Iniciando debug do erro '_type'...")
    print("=" * 60)
    
    # Teste 1: Criação de tarefas
    print("\n📋 TESTE 1: Criação de Tarefas")
    task_success = debug_task_creation()
    
    # Teste 2: Criação de crews
    print("\n📋 TESTE 2: Criação de Crews")
    crew_success = debug_crew_creation()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DO DEBUG:")
    print(f"   Criação de Tarefas: {'✅ PASSOU' if task_success else '❌ FALHOU'}")
    print(f"   Criação de Crews: {'✅ PASSOU' if crew_success else '❌ FALHOU'}")
    
    if task_success and crew_success:
        print("\n🎉 Todos os testes passaram! O erro '_type' não foi reproduzido.")
        print("   O problema pode estar na interface do Streamlit.")
    else:
        print("\n⚠️ Alguns testes falharam. O erro '_type' foi reproduzido.")
        print("   Verifique os logs acima para identificar o problema.")
    
    return task_success and crew_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 