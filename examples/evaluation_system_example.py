"""
Exemplo de uso do Sistema de Avaliação Automático de Crews
Este exemplo demonstra como o sistema avalia automaticamente as execuções das crews
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager


def main():
    """Demonstração do sistema de avaliação automático"""
    
    print("🚀 SISTEMA DE AVALIAÇÃO AUTOMÁTICO DE CREWS")
    print("=" * 60)
    
    # Inicializar managers
    print("📋 Inicializando sistema...")
    tools_manager = ToolsManager()
    agent_manager = AgentManager()
    agent_manager.set_tools_manager(tools_manager)
    task_manager = TaskManager()
    crew_manager = CrewManager(agent_manager, task_manager)
    
    # Criar uma crew de exemplo
    print("\n🔧 Criando crew de exemplo...")
    crew_name = "exemplo_avaliacao"
    agent_types = ["technical_researcher", "data_analyst", "technical_writer"]
    
    crew = crew_manager.create_crew(
        name=crew_name,
        agent_types=agent_types,
        description="Crew de exemplo para demonstrar o sistema de avaliação"
    )
    
    if not crew:
        print("❌ Erro ao criar crew")
        return
    
    print(f"✅ Crew '{crew_name}' criada com {len(crew.agents)} agentes")
    
    # Executar crew com avaliação automática
    print("\n🎯 Executando crew com avaliação automática...")
    print("ℹ️ O sistema irá automaticamente:")
    print("  • Executar a tarefa solicitada")
    print("  • Analisar a performance dos agentes")
    print("  • Avaliar qualidade dos outputs")
    print("  • Verificar adequação das ferramentas")
    print("  • Gerar relatório com recomendações")
    
    inputs = {
        'topic': 'Análise de viabilidade técnica para construção de ponte de concreto armado'
    }
    
    result = crew_manager.execute_crew(crew_name, inputs)
    
    if result:
        print("\n" + "=" * 80)
        print("📄 RESULTADO DA EXECUÇÃO COM AVALIAÇÃO:")
        print("=" * 80)
        
        # Mostrar apenas parte do resultado para não sobrecarregar
        result_preview = str(result)[:1000] + "..." if len(str(result)) > 1000 else str(result)
        print(result_preview)
        
        print("\n" + "=" * 80)
        print("📊 RESUMO DA AVALIAÇÃO:")
        print("=" * 80)
        
        # Extrair informações da avaliação (se presente no resultado)
        if "RELATÓRIO DE AVALIAÇÃO" in str(result):
            print("✅ Sistema de avaliação executado com sucesso!")
            print("📈 Relatório de avaliação incluído no resultado")
            print("🎯 Recomendações de melhoria geradas")
        else:
            print("⚠️ Avaliação não detectada no resultado")
    else:
        print("❌ Erro na execução da crew")
    
    # Mostrar histórico de execuções
    print("\n📚 HISTÓRICO DE EXECUÇÕES:")
    print("-" * 40)
    
    try:
        history = crew_manager.db_manager.get_execution_history()
        for i, execution in enumerate(history[:3], 1):  # Mostrar apenas as 3 mais recentes
            print(f"{i}. {execution['crew_name']} - {execution['topic'][:50]}...")
            print(f"   Status: {execution['status']} | Duração: {execution['duration']}")
            
            # Verificar se há relatório de avaliação
            eval_report = crew_manager.db_manager.get_evaluation_report(execution['id'])
            if eval_report:
                print(f"   📊 Relatório de avaliação: Disponível ({len(eval_report)} chars)")
            else:
                print(f"   📊 Relatório de avaliação: Não disponível")
            print()
    except Exception as e:
        print(f"❌ Erro ao carregar histórico: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\n💡 CARACTERÍSTICAS DO SISTEMA DE AVALIAÇÃO:")
    print("  ✅ Avaliação automática obrigatória em todas as execuções")
    print("  ✅ Análise detalhada de performance dos agentes")
    print("  ✅ Verificação de adequação das ferramentas")
    print("  ✅ Análise de fluxo de trabalho e eficiência")
    print("  ✅ Geração de recomendações específicas")
    print("  ✅ Relatórios salvos separadamente no banco de dados")
    print("  ✅ Sistema de fallback para garantir funcionamento")
    print("  ✅ Especialização para engenharia civil")
    
    print("\n🔍 PRÓXIMOS PASSOS:")
    print("  • Execute crews regularmente para coletar dados de avaliação")
    print("  • Revise os relatórios de avaliação para identificar padrões")
    print("  • Implemente as recomendações sugeridas pelos avaliadores")
    print("  • Monitore melhorias na qualidade ao longo do tempo")


if __name__ == "__main__":
    main() 