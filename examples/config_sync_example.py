"""
Exemplo de Sistema de Sincronização Automática
Demonstra como o sistema detecta mudanças e atualiza crews automaticamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.config_sync_manager import ConfigSyncManager
from app.utils.database import DatabaseManager
from app.agents.agent_manager import AgentManager
from app.crews.crew_manager import CrewManager
from app.crews.task_manager import TaskManager
from app.utils.tools_manager import ToolsManager

def test_sync_system():
    """Testa o sistema de sincronização automática"""
    print("🚀 Testando Sistema de Sincronização Automática")
    print("=" * 60)
    
    # 1. Inicializar componentes
    print("\n1️⃣ Inicializando componentes...")
    tools_manager = ToolsManager()
    agent_manager = AgentManager()
    agent_manager.set_tools_manager(tools_manager)
    task_manager = TaskManager()
    crew_manager = CrewManager(agent_manager, task_manager)
    
    # 2. Verificar status da sincronização
    print("\n2️⃣ Verificando status da sincronização...")
    sync_status = crew_manager.get_sync_status()
    
    print(f"📊 Status do Sistema: {'✅ Ativo' if sync_status.get('sync_available') else '❌ Inativo'}")
    print(f"🗃️ Crews no Banco: {sync_status.get('crews_in_database', 0)}")
    print(f"💾 Crews na Memória: {sync_status.get('crews_in_memory', 0)}")
    print(f"🔄 Sincronização Automática: {'✅ Ativa' if sync_status.get('auto_sync_enabled') else '❌ Inativa'}")
    
    # 3. Listar crews existentes
    print("\n3️⃣ Crews atualmente carregadas:")
    crews_info = crew_manager.get_saved_crews_info()
    
    if not crews_info:
        print("ℹ️ Nenhuma crew salva encontrada")
    else:
        for crew_info in crews_info:
            print(f"   📦 {crew_info['name']}")
            print(f"      Agentes: {', '.join(crew_info['agent_types'])}")
            print(f"      Status: {crew_info['status']}")
            print()
    
    # 4. Demonstrar sincronização manual
    print("\n4️⃣ Executando sincronização manual...")
    sync_result = crew_manager.sync_with_config_changes()
    
    print(f"📈 Resultado da Sincronização:")
    print(f"   Status: {sync_result.get('status', 'Desconhecido')}")
    print(f"   Crews verificadas: {sync_result.get('crews_checked', 0)}")
    if sync_result.get('status') == 'error':
        print(f"   Erro: {sync_result.get('message', 'Erro desconhecido')}")
    
    # 5. Verificar funcionamento do ConfigSyncManager diretamente
    print("\n5️⃣ Testando ConfigSyncManager diretamente...")
    sync_manager = ConfigSyncManager()
    
    # Detectar mudanças
    changes = sync_manager.detect_config_changes()
    print(f"   Arquivos verificados: {len(changes)}")
    
    for config_type, change_info in changes.items():
        print(f"   📁 {config_type}: {len(change_info.get('current_config', {}))} itens")
    
    # 6. Executar sincronização completa
    print("\n6️⃣ Executando sincronização completa...")
    full_sync_result = sync_manager.perform_full_sync()
    
    print(f"📊 Resultado da Sincronização Completa:")
    print(f"   Status: {full_sync_result.get('status', 'Desconhecido')}")
    print(f"   Mudanças detectadas: {full_sync_result.get('changes_detected', 0)}")
    print(f"   Crews verificadas: {full_sync_result.get('crews_checked', 0)}")
    
    print("\n✅ Teste do sistema de sincronização concluído!")
    print("=" * 60)

def demonstrate_config_change_scenario():
    """Demonstra um cenário de mudança de configuração"""
    print("\n🔄 Demonstrando Cenário de Mudança de Configuração")
    print("=" * 60)
    
    print("""
📝 CENÁRIO SIMULADO:
1. Você tem uma crew salva que usa o agente 'researcher'
2. Você renomeia 'researcher' para 'pesquisador' no agents.yaml
3. O sistema de sincronização deve detectar essa mudança
4. A crew salva deve ser atualizada automaticamente

💡 BENEFÍCIOS:
✅ Crews não ficam quebradas após mudanças
✅ Sincronização automática na inicialização
✅ Sincronização manual disponível
✅ Histórico de mudanças mantido
✅ Interface visual no Streamlit
    """)

def main():
    """Função principal do exemplo"""
    print("🔄 Sistema de Sincronização Automática de Crews")
    print("Este exemplo demonstra como o sistema mantém crews atualizadas")
    print()
    
    try:
        # Executar teste completo
        test_sync_system()
        
        # Demonstrar cenário
        demonstrate_config_change_scenario()
        
        print("\n🎉 Exemplo executado com sucesso!")
        print("\nPara testar mudanças reais:")
        print("1. Execute o aplicativo Streamlit")
        print("2. Crie uma crew")
        print("3. Altere um nome no arquivo agents.yaml")
        print("4. Reinicie o aplicativo")
        print("5. Veja a crew sendo sincronizada automaticamente")
        
    except Exception as e:
        print(f"❌ Erro durante o exemplo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 