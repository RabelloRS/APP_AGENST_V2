"""
Gerenciador de crews para o sistema
"""

from typing import Dict, List, Optional
from datetime import datetime

from crewai import Crew, Task

from app.agents.agent_manager import AgentManager
from app.crews.task_manager import TaskManager
from app.utils.database import DatabaseManager
from app.utils.config_sync_manager import ConfigSyncManager
from app.utils.log_manager import log_manager


class CrewManager:
    """Classe para gerenciar crews do sistema"""

    def __init__(
        self, agent_manager: AgentManager, task_manager: Optional[TaskManager] = None
    ):
        self.agent_manager = agent_manager
        self.task_manager = task_manager or TaskManager()
        self.crews: Dict[str, Crew] = {}
        self.crew_configs: Dict[str, Dict] = {}
        self.db_manager = DatabaseManager()
        self.sync_manager = ConfigSyncManager(self.db_manager)
        
        # 🔄 SINCRONIZAÇÃO AUTOMÁTICA ANTES DE CARREGAR CREWS
        self._perform_auto_sync()
        
        # 🔄 CARREGAR CREWS SALVAS AUTOMATICAMENTE
        self._load_saved_crews()

    def _perform_auto_sync(self):
        """Executa sincronização automática na inicialização se necessário"""
        try:
            print("🔄 Verificando necessidade de sincronização...")
            
            # Executar sincronização automática silenciosa
            sync_result = self.sync_manager.perform_full_sync()
            
            if sync_result['status'] == 'completed':
                print(f"✅ Sincronização concluída - {sync_result['crews_checked']} crew(s) verificada(s)")
            
        except Exception as e:
            print(f"⚠️ Erro na sincronização automática (continuando sem sincronização): {e}")

    def _load_saved_crews(self):
        """Carrega crews salvas do banco de dados na inicialização"""
        try:
            print("🔄 Carregando crews salvas do banco de dados...")
            saved_configs = self.db_manager.get_all_crew_configs()
            
            loaded_count = 0
            for config in saved_configs:
                crew_name = config['crew_name']
                agent_types = config['agent_types']
                description = config['description']
                
                # Recriar a crew na memória
                success = self._recreate_crew_from_config(crew_name, agent_types, description)
                if success:
                    loaded_count += 1
                    print(f"✅ Crew '{crew_name}' carregada com sucesso")
                else:
                    print(f"⚠️ Falha ao carregar crew '{crew_name}'")
            
            print(f"📦 Total de crews carregadas: {loaded_count}/{len(saved_configs)}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar crews salvas: {e}")

    def _recreate_crew_from_config(self, name: str, agent_types: List[str], description: str) -> bool:
        """Recria uma crew a partir da configuração salva no banco"""
        try:
            # Verificar se a crew já existe na memória
            if name in self.crews:
                print(f"⚠️ Crew '{name}' já existe na memória, pulando...")
                return True
            
            # Criar agentes se não existirem
            agents = []
            for agent_type in agent_types:
                agent = self.agent_manager.get_agent(agent_type)
                if not agent:
                    agent = self.agent_manager.create_agent(agent_type)
                if agent:
                    agents.append(agent)
            
            if not agents:
                print(f"❌ Nenhum agente válido criado para crew '{name}'")
                return False
            
            # Debug: Verificar tipos dos agentes antes de criar a crew
            for idx, agent in enumerate(agents):
                print(f"[DEBUG] Tipo do agente {idx}: {type(agent)} - {getattr(agent, 'role', agent)}")

            # Criar crew
            crew = Crew(
                agents=agents,
                tasks=[],  # Tarefas serão adicionadas posteriormente se necessário
                verbose=True,
                memory=True,
            )
            
            # Adicionar à memória
            self.crews[name] = crew
            self.crew_configs[name] = {
                "description": description,
                "agent_types": agent_types,
                "created_at": "Carregado do banco de dados",
                "loaded_from_db": True
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao recriar crew '{name}': {e}")
            return False

    def create_crew(
        self, name: str, agent_types: List[str], description: str = ""
    ) -> Optional[Crew]:
        """Cria uma nova crew com os agentes especificados"""
        try:
            # Criar agentes se não existirem
            agents = []
            for agent_type in agent_types:
                agent = self.agent_manager.get_agent(agent_type)
                if not agent:
                    agent = self.agent_manager.create_agent(agent_type)
                if agent:
                    agents.append(agent)

            if not agents:
                print("Nenhum agente válido foi criado")
                return None

            # Debug: Verificar tipos e conteúdos dos agentes antes de criar a crew
            print(f"[DEBUG] Tipos e conteúdos dos agentes antes de criar Crew '{name}':")
            for idx, agent in enumerate(agents):
                print(f"  - Agente {idx}: type={type(agent)} | repr={repr(agent)} | dict={agent if isinstance(agent, dict) else 'N/A'} | role={getattr(agent, 'role', None)}")
                if hasattr(agent, 'tools'):
                    tools = getattr(agent, 'tools', [])
                    print(f"    [DEBUG] Agent {idx} tools:")
                    for t_idx, tool in enumerate(tools):
                        print(f"      - Tool {t_idx}: type={type(tool)} | repr={repr(tool)} | dict={tool if isinstance(tool, dict) else 'N/A'} | name={getattr(tool, 'name', None)}")
                        if isinstance(tool, dict):
                            print(f"        [ERRO] Tool {t_idx} do agente {idx} é um dicionário! Chave '_type': {tool.get('_type', 'N/A')}")
                else:
                    print(f"    [ERRO] Agente {idx} não possui atributo 'tools'!")

            # Criar crew
            crew = Crew(
                agents=agents,
                tasks=[],  # Tarefas serão adicionadas posteriormente
                verbose=True,
                memory=True,
            )

            # Validação de ferramentas dos agentes ao criar crew
            if not self._validate_agents_tools(crew):
                print(f"❌ Criação de crew abortada: Um ou mais agentes estão sem ferramentas configuradas.")
                return None

            self.crews[name] = crew
            self.crew_configs[name] = {
                "description": description,
                "agent_types": agent_types,
                "created_at": datetime.now().isoformat(),
            }
            
            # Salvar configuração no banco de dados
            self.db_manager.save_crew_config(name, description, agent_types, [])

            return crew

        except Exception as e:
            print(f"Erro ao criar crew {name}: {e}")
            return None

    def add_task_to_crew(self, crew_name: str, task_type: str, **params) -> bool:
        """Adiciona uma tarefa a uma crew específica"""
        try:
            print(f"🔧 Debug: Adicionando tarefa '{task_type}' à crew '{crew_name}'")
            
            crew = self.get_crew(crew_name)
            if not crew:
                print(f"❌ Crew {crew_name} não encontrada")
                return False

            # Obter o agente responsável pela tarefa
            task_info = self.task_manager.get_task_info(task_type)
            if not task_info:
                print(f"❌ Tipo de tarefa {task_type} não encontrado")
                return False

            agent_type = task_info.get("agent")
            if not agent_type:
                print(f"❌ Agente não especificado para tarefa {task_type}")
                return False

            print(f"🔧 Debug: Agente responsável pela tarefa: {agent_type}")

            agent = self.agent_manager.get_agent(agent_type)
            if not agent:
                print(f"❌ Agente {agent_type} não encontrado")
                return False

            print(f"🔧 Debug: Agente encontrado: {getattr(agent, 'role', 'Unknown')}")

            # Criar tarefa
            task = self.task_manager.create_task_with_params(task_type, agent, **params)
            if not task:
                print(f"❌ Falha ao criar tarefa {task_type}")
                return False

            # Adicionar tarefa à crew
            crew.tasks.append(task)
            print(f"✅ Tarefa '{task_type}' adicionada à crew '{crew_name}' com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar tarefa à crew: {e}")
            print(f"   Tipo de erro: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False

    def create_crew_with_tasks(
        self,
        name: str,
        agent_types: List[str],
        task_types: List[str],
        description: str = "",
        **task_params,
    ) -> Optional[Crew]:
        """Cria uma crew com agentes e tarefas pré-definidas"""
        crew = self.create_crew(name, agent_types, description)
        if not crew:
            return None

        # Adicionar tarefas
        for task_type in task_types:
            self.add_task_to_crew(name, task_type, **task_params)

        return crew

    def _select_best_agent_for_task(self, crew, task_description: str) -> Optional[object]:
        """Seleciona o agente mais adequado da crew para a tarefa dinâmica"""
        # Busca por correspondência no role ou ferramentas
        task_desc_lower = task_description.lower()
        best_agent = None
        max_score = 0
        for agent in crew.agents:
            score = 0
            # Pontua se o role do agente aparece na descrição
            if hasattr(agent, 'role') and agent.role and agent.role.lower() in task_desc_lower:
                score += 2
            # Pontua se alguma ferramenta do agente aparece na descrição
            if hasattr(agent, 'tools'):
                for tool in agent.tools:
                    tool_name = getattr(tool, 'name', str(tool)).lower()
                    if tool_name in task_desc_lower:
                        score += 1
            if score > max_score:
                max_score = score
                best_agent = agent
        # Se ninguém pontuou, retorna o primeiro agente (fallback)
        return best_agent or (crew.agents[0] if crew.agents else None)

    def execute_crew_task(self, crew_name: str, task_description: str) -> Optional[str]:
        """Executa uma tarefa usando uma crew específica"""
        crew = self.get_crew(crew_name)
        if not crew:
            print(f"Crew {crew_name} não encontrada")
            return None
        # Validação de ferramentas dos agentes
        if not self._validate_agents_tools(crew):
            print(f"❌ Execução abortada: Um ou mais agentes da crew '{crew_name}' estão sem ferramentas configuradas.")
            return None
        try:
            # Seleciona o agente mais adequado
            agent = self._select_best_agent_for_task(crew, task_description)
            # Criar tarefa dinâmica
            task = Task(
                description=task_description,
                expected_output="Resultado da execução da tarefa",
                agent=agent,
            )

            # Executar crew
            result = crew.kickoff()
            return str(result)

        except Exception as e:
            print(f"Erro ao executar tarefa na crew {crew_name}: {e}")
            return None

    def execute_crew(self, crew_name: str, inputs: Optional[Dict] = None) -> Optional[str]:
        """Executa uma crew com suas tarefas pré-definidas ou cria tarefas dinâmicas"""
        crew = self.get_crew(crew_name)
        if not crew:
            print(f"Crew {crew_name} não encontrada")
            return None

        # Salvar execução no banco de dados
        topic = inputs.get('topic', 'Execução sem tópico') if inputs else 'Execução sem tópico'
        start_time = datetime.now()
        execution_id = self.db_manager.save_execution(crew_name, topic, start_time)

        try:
            # Se não há tarefas pré-definidas, criar uma tarefa dinâmica
            if not crew.tasks:
                print(f"Crew {crew_name} não possui tarefas definidas, criando tarefa dinâmica...")
                if not inputs or 'topic' not in inputs:
                    print("Parâmetro 'topic' não fornecido para tarefa dinâmica")
                    self.db_manager.update_execution_result(
                        execution_id, "Erro: Tópico não fornecido", 
                        datetime.now(), "0:00:00", "error", "Parâmetro 'topic' não fornecido"
                    )
                    return None
                # Seleciona o agente mais adequado
                agent = self._select_best_agent_for_task(crew, inputs['topic'])
                # Criar tarefa dinâmica baseada no tópico
                topic = inputs['topic']
                task = Task(
                    description=f"Execute a seguinte tarefa: {topic}",
                    expected_output="Resultado detalhado da execução da tarefa",
                    agent=agent,
                )
                crew.tasks = [task]
            # Executar crew normalmente
            result = crew.kickoff()
            end_time = datetime.now()
            duration = str(end_time - start_time).split('.')[0]
            
            # SISTEMA AVANÇADO DE AVALIAÇÃO AUTOMÁTICA
            try:
                evaluation_report = self._execute_comprehensive_evaluation(
                    crew, result, {
                        'crew_name': crew_name,
                        'topic': topic,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': duration,
                        'status': 'completed'
                    }
                )
                
                # Anexar relatório de avaliação ao resultado
                result = f"{str(result)}\n\n{self._format_evaluation_separator()}\n{evaluation_report}"
                
                # Salvar relatório de avaliação separadamente no banco
                self.db_manager.save_evaluation_report(execution_id, evaluation_report)
                
            except Exception as e:
                print(f"⚠️ Erro na avaliação automática: {e}")
                # Fallback para avaliação básica
                try:
                    basic_evaluation = self._execute_basic_evaluation(crew, result)
                    result = f"{str(result)}\n\n{self._format_evaluation_separator()}\n{basic_evaluation}"
                except Exception as fallback_error:
                    print(f"❌ Erro também na avaliação básica: {fallback_error}")
                    result = f"{str(result)}\n\n{self._format_evaluation_separator()}\n⚠️ Avaliação automática não disponível nesta execução."

            # Salvar resultado no banco de dados
            self.db_manager.update_execution_result(
                execution_id, str(result), end_time, duration, "completed"
            )
            return str(result)
            
        except Exception as e:
            end_time = datetime.now()
            duration = str(end_time - start_time).split('.')[0]
            error_msg = str(e)
            
            # Salvar erro no banco de dados
            self.db_manager.update_execution_result(
                execution_id, "", end_time, duration, "error", error_msg
            )
            
            print(f"Erro ao executar crew {crew_name}: {e}")
            return None

    def execute_crew_with_logs(self, crew_name: str, inputs: Optional[Dict] = None):
        """Executa uma crew capturando todos os logs em tempo real (versão segura)"""
        logs = []
        
        try:
            # Iniciar captura de logs de forma segura
            log_manager.start_capture()
            log_manager.log_info(f"🚀 Iniciando execução da crew '{crew_name}'")
            
            # Executar crew normalmente
            result = self.execute_crew(crew_name, inputs)
            
            # Obter logs capturados
            logs = log_manager.get_recent_logs(100)  # Limitar a 100 logs
            
            log_manager.log_info(f"✅ Execução da crew '{crew_name}' concluída")
            
            return result, logs
            
        except Exception as e:
            log_manager.log_error(f"❌ Erro na execução da crew '{crew_name}': {e}")
            logs = log_manager.get_recent_logs(50)  # Menos logs em caso de erro
            return None, logs
            
        finally:
            # Sempre parar captura de logs
            try:
                log_manager.stop_capture()
            except:
                pass  # Ignorar erros ao parar captura
    
    def execute_crew_safe(self, crew_name: str, inputs: Optional[Dict] = None) -> Optional[str]:
        """Versão segura de execução sem captura de logs (fallback)"""
        try:
            print(f"🚀 Executando crew '{crew_name}' (modo seguro)")
            
            crew = self.get_crew(crew_name)
            if not crew:
                print(f"❌ Crew '{crew_name}' não encontrada")
                return None

            # Verificar se crew tem agentes
            if not crew.agents:
                print(f"❌ Crew '{crew_name}' não possui agentes")
                return None

            # Salvar execução no banco de dados
            topic = inputs.get('topic', 'Execução segura') if inputs else 'Execução segura'
            start_time = datetime.now()
            execution_id = self.db_manager.save_execution(crew_name, topic, start_time)

            # Se não há tarefas pré-definidas, criar uma tarefa dinâmica
            if not crew.tasks:
                print(f"Criando tarefa dinâmica para '{crew_name}'...")
                
                if not inputs or 'topic' not in inputs:
                    error_msg = "Parâmetro 'topic' não fornecido"
                    print(f"❌ {error_msg}")
                    self.db_manager.update_execution_result(
                        execution_id, "", datetime.now(), "0:00:00", "error", error_msg
                    )
                    return None
                
                # Criar tarefa dinâmica
                task = Task(
                    description=f"Execute a seguinte tarefa: {topic}",
                    expected_output="Resultado detalhado da execução da tarefa",
                    agent=crew.agents[0],
                )
                crew.tasks = [task]
            
            print(f"🔄 Executando crew com {len(crew.agents)} agentes e {len(crew.tasks)} tarefas")
            
            # Executar crew
            result = crew.kickoff()
            end_time = datetime.now()
            duration = str(end_time - start_time).split('.')[0]
            
            print(f"✅ Execução concluída em {duration}")
            
            # Salvar resultado
            self.db_manager.update_execution_result(
                execution_id, str(result), end_time, duration, "completed"
            )
            
            return str(result)
            
        except Exception as e:
            end_time = datetime.now()
            duration = str(end_time - start_time).split('.')[0] if 'start_time' in locals() else "0:00:00"
            error_msg = str(e)
            
            print(f"❌ Erro na execução: {error_msg}")
            
            if 'execution_id' in locals():
                self.db_manager.update_execution_result(
                    execution_id, "", end_time, duration, "error", error_msg
                )
            
            return None

    def get_crew(self, name: str) -> Optional[Crew]:
        """Retorna uma crew existente"""
        return self.crews.get(name)

    def get_all_crews(self) -> Dict[str, Crew]:
        """Retorna todas as crews criadas"""
        return self.crews

    def get_crew_info(self, name: str) -> Optional[Dict]:
        """Retorna informações sobre uma crew"""
        return self.crew_configs.get(name)

    def delete_crew(self, name: str) -> bool:
        """Remove uma crew (mantém o histórico no banco de dados)"""
        if name in self.crews:
            del self.crews[name]
            del self.crew_configs[name]
            # Não deletar do banco de dados para manter histórico
            # self.db_manager.delete_crew_config(name)
            return True
        return False

    def list_crew_names(self) -> List[str]:
        """Lista todos os nomes de crews"""
        return list(self.crews.keys())

    def reload_configs(self) -> bool:
        """Recarrega as configurações de agentes e tarefas"""
        try:
            self.agent_manager.reload_configs()
            self.task_manager.reload_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False

    def reload_crews_from_database(self) -> int:
        """Recarrega crews do banco de dados (força recarregamento)"""
        try:
            print("🔄 Recarregando crews do banco de dados...")
            
            # Limpar crews atuais em memória
            crews_before = len(self.crews)
            self.crews.clear()
            self.crew_configs.clear()
            
            # Carregar crews do banco
            self._load_saved_crews()
            
            crews_after = len(self.crews)
            print(f"🔄 Recarregamento concluído: {crews_before} → {crews_after} crews")
            
            return crews_after
            
        except Exception as e:
            print(f"❌ Erro ao recarregar crews do banco: {e}")
            return 0

    def get_saved_crews_info(self) -> List[Dict]:
        """Retorna informações das crews salvas no banco de dados"""
        try:
            saved_configs = self.db_manager.get_all_crew_configs()
            
            crew_info = []
            for config in saved_configs:
                crew_name = config['crew_name']
                is_loaded = crew_name in self.crews
                
                crew_info.append({
                    'name': crew_name,
                    'description': config['description'],
                    'agent_types': config['agent_types'],
                    'agent_count': len(config['agent_types']),
                    'created_at': config['created_at'],
                    'is_loaded_in_memory': is_loaded,
                    'status': '✅ Carregada' if is_loaded else '⚠️ Não carregada'
                })
            
            return crew_info
            
        except Exception as e:
            print(f"❌ Erro ao obter informações das crews salvas: {e}")
            return []

    def _execute_comprehensive_evaluation(self, crew, result, execution_data):
        """Executa avaliação abrangente usando o agente especialista"""
        print("🔍 Iniciando avaliação abrangente da crew...")
        
        # Coletar dados detalhados para avaliação
        evaluation_data = self._collect_evaluation_data(crew, result, execution_data)
        
        # Obter ou criar agente avaliador
        evaluator_agent = self._get_or_create_evaluator_agent()
        if not evaluator_agent:
            raise Exception("Não foi possível criar o agente avaliador")
        
        # Criar tarefa de avaliação específica, passando os parâmetros como um dicionário
        evaluation_task = self.task_manager.create_task_with_params(
            'crew_evaluation_task',
            evaluator_agent,
            params={
                'topic': execution_data.get('topic', 'Execução da crew'),
                'context': self._build_comprehensive_evaluation_context(evaluation_data)
            }
        )
        
        if not evaluation_task:
            raise Exception("Não foi possível criar a tarefa de avaliação")
        
        # Criar uma crew temporária para a avaliação
        evaluation_crew = Crew(
            agents=[evaluator_agent],
            tasks=[evaluation_task],
            verbose=True
        )
        
        # Executar a crew de avaliação
        print("📊 Executando análise detalhada...")
        evaluation_report_result = evaluation_crew.kickoff()
        
        # Garantir que o resultado seja uma string
        evaluation_report = str(evaluation_report_result) if evaluation_report_result else "Relatório de avaliação não gerado."
        
        print("✅ Avaliação abrangente concluída")
        return evaluation_report
    
    def _execute_basic_evaluation(self, crew, result):
        """Executa avaliação básica em caso de falha na avaliação principal"""
        print("🔄 Executando avaliação básica de fallback...")
        
        try:
            # Usar agente de fallback
            evaluator_agent = self._get_or_create_simple_evaluator()
            if not evaluator_agent:
                raise Exception("Agente de fallback não disponível")
            
            # Gerar resumo básico
            basic_summary = self._build_basic_execution_summary(crew, result)
            
            # Executar avaliação básica usando a ferramenta basic_evaluation_tool
            from app.utils.tools import basic_evaluation_tool
            basic_report = basic_evaluation_tool(basic_summary)
            
            return basic_report
            
        except Exception as e:
            print(f"❌ Erro na avaliação básica: {e}")
            return self._generate_minimal_evaluation_report(crew, result)
    
    def _collect_evaluation_data(self, crew, result, execution_data):
        """Coleta dados detalhados para avaliação"""
        agents_data = {}
        tools_data = {}
        tasks_data = []
        
        # Coletar dados dos agentes
        for agent in crew.agents:
            agent_role = getattr(agent, 'role', 'Unknown')
            agent_tools = [getattr(tool, 'name', str(tool)) for tool in getattr(agent, 'tools', [])]
            agents_data[agent_role] = {
                'tools': agent_tools,
                'backstory': getattr(agent, 'backstory', ''),
                'goal': getattr(agent, 'goal', '')
            }
            tools_data[agent_role] = agent_tools
        
        # Coletar dados das tarefas
        for task in crew.tasks:
            task_data = {
                'description': getattr(task, 'description', ''),
                'agent': getattr(getattr(task, 'agent', None), 'role', 'Unknown'),
                'expected_output': getattr(task, 'expected_output', '')
            }
            tasks_data.append(task_data)
        
        return {
            'agents': agents_data,
            'tools_usage': tools_data,
            'tasks': tasks_data,
            'execution_info': execution_data,
            'final_result': result,
            'crew_metrics': {
                'agents_count': len(crew.agents),
                'tasks_count': len(crew.tasks),
                'status': execution_data.get('status', 'unknown'),
                'duration': execution_data.get('duration', 'N/A')
            }
        }
    
    def _get_or_create_evaluator_agent(self):
        """Obtém ou cria o agente avaliador especializado"""
        evaluator_type = "crewai_evaluator"
        
        # Tentar obter agente existente
        evaluator_agent = self.agent_manager.get_agent(evaluator_type)
        if evaluator_agent:
            return evaluator_agent
        
        # Criar novo agente avaliador
        return self.agent_manager.create_agent(evaluator_type)
    
    def _get_or_create_simple_evaluator(self):
        """Obtém ou cria o agente avaliador simples para fallback"""
        evaluator_type = "simple_evaluator"
        
        # Tentar obter agente existente
        evaluator_agent = self.agent_manager.get_agent(evaluator_type)
        if evaluator_agent:
            return evaluator_agent
        
        # Criar novo agente avaliador simples
        return self.agent_manager.create_agent(evaluator_type)
    
    def _build_comprehensive_evaluation_context(self, evaluation_data):
        """Constrói contexto abrangente para avaliação"""
        context = f"""
DADOS PARA AVALIAÇÃO ABRANGENTE:

1. INFORMAÇÕES DA EXECUÇÃO:
   • Crew: {evaluation_data['execution_info'].get('crew_name', 'N/A')}
   • Tópico: {evaluation_data['execution_info'].get('topic', 'N/A')}
   • Duração: {evaluation_data['execution_info'].get('duration', 'N/A')}
   • Status: {evaluation_data['execution_info'].get('status', 'N/A')}

2. AGENTES E FERRAMENTAS:
"""
        
        for agent_name, agent_info in evaluation_data['agents'].items():
            context += f"   • {agent_name}: {len(agent_info['tools'])} ferramentas\n"
            context += f"     Ferramentas: {', '.join(agent_info['tools'])}\n"
        
        context += f"\n3. TAREFAS EXECUTADAS: {len(evaluation_data['tasks'])}\n"
        for i, task in enumerate(evaluation_data['tasks'], 1):
            context += f"   {i}. Agente: {task['agent']}\n"
            context += f"      Descrição: {task['description'][:100]}...\n"
        
        context += f"\n4. RESULTADO FINAL:\n"
        context += f"   Tamanho: {len(str(evaluation_data['final_result']))} caracteres\n"
        
        return context
    
    def _generate_evaluation_report(self, evaluation_data, context):
        """Gera relatório de avaliação usando as ferramentas implementadas"""
        try:
            from app.utils.tools import (
                crew_performance_analyzer, agent_output_quality_checker,
                tool_usage_evaluator, workflow_efficiency_analyzer,
                recommendation_generator, execution_summary_builder
            )
            
            # Usar as ferramentas para gerar análises
            performance_analysis = crew_performance_analyzer(evaluation_data['crew_metrics'])
            
            # Simular outputs dos agentes para análise de qualidade
            agent_outputs = {agent: f"Output do agente {agent}" for agent in evaluation_data['agents'].keys()}
            quality_analysis = agent_output_quality_checker(agent_outputs)
            
            tool_analysis = tool_usage_evaluator(evaluation_data['tools_usage'])
            workflow_analysis = workflow_efficiency_analyzer(evaluation_data['crew_metrics'])
            
            # Gerar recomendações
            recommendations = recommendation_generator({'analysis': 'completed'})
            
            # Construir resumo
            summary = execution_summary_builder(
                {'name': evaluation_data['execution_info'].get('crew_name', 'N/A'),
                 'agents': list(evaluation_data['agents'].keys()),
                 'tasks': evaluation_data['tasks']},
                evaluation_data['execution_info']
            )
            
            # Consolidar tudo em um relatório abrangente
            comprehensive_report = f"""
{summary}

{performance_analysis}

{quality_analysis}

{tool_analysis}

{workflow_analysis}

{recommendations}
            """
            
            return comprehensive_report.strip()
            
        except Exception as e:
            print(f"Erro na geração do relatório de avaliação: {e}")
            return self._generate_fallback_evaluation_report(evaluation_data)
    
    def _generate_fallback_evaluation_report(self, evaluation_data):
        """Gera relatório de fallback em caso de erro"""
        return f"""
=== RELATÓRIO DE AVALIAÇÃO (MODO FALLBACK) ===

📊 RESUMO DA EXECUÇÃO:
• Crew: {evaluation_data['execution_info'].get('crew_name', 'N/A')}
• Tópico: {evaluation_data['execution_info'].get('topic', 'N/A')}
• Duração: {evaluation_data['execution_info'].get('duration', 'N/A')}
• Agentes: {len(evaluation_data['agents'])}
• Tarefas: {len(evaluation_data['tasks'])}

⚠️ AVALIAÇÃO LIMITADA:
Esta avaliação foi gerada em modo de fallback devido a limitações técnicas.
Para uma análise completa, verifique as configurações do sistema de avaliação.

🎯 RECOMENDAÇÕES BÁSICAS:
• Verificar se o agente avaliador está configurado corretamente
• Revisar as ferramentas de avaliação disponíveis
• Considerar executar avaliação manual se necessário
        """
    
    def _generate_minimal_evaluation_report(self, crew, result):
        """Gera relatório mínimo quando tudo mais falha"""
        return f"""
=== AVALIAÇÃO MÍNIMA ===

📊 INFORMAÇÕES BÁSICAS:
• Agentes na crew: {len(crew.agents)}
• Tarefas executadas: {len(crew.tasks)}
• Resultado obtido: {'Sim' if result else 'Não'}
• Tamanho do resultado: {len(str(result))} caracteres

✅ STATUS: Execução concluída
⚠️ AVALIAÇÃO: Sistema de avaliação indisponível

💡 RECOMENDAÇÃO: 
Verificar logs do sistema e configurações dos agentes avaliadores.
        """
    
    def _build_basic_execution_summary(self, crew, result):
        """Gera resumo básico da execução para avaliação de fallback"""
        summary = f"RESUMO DA EXECUÇÃO:\n"
        summary += f"Agentes: {len(crew.agents)}\n"
        summary += f"Tarefas: {len(crew.tasks)}\n"
        summary += f"Resultado: {len(str(result))} caracteres\n"
        
        for i, agent in enumerate(crew.agents, 1):
            agent_role = getattr(agent, 'role', f'Agente {i}')
            agent_tools = getattr(agent, 'tools', [])
            summary += f"Agente {i}: {agent_role} - {len(agent_tools)} ferramentas\n"
        
        return summary
    
    def _format_evaluation_separator(self):
        """Formata separador visual para o relatório de avaliação"""
        return """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          RELATÓRIO DE AVALIAÇÃO                             ║
║                    Sistema Automático de Qualidade                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """

    # 🔄 MÉTODOS DE SINCRONIZAÇÃO PÚBLICA
    
    def sync_with_config_changes(self) -> Dict:
        """Executa sincronização manual das crews com mudanças de configuração"""
        try:
            print("🔄 Executando sincronização manual...")
            result = self.sync_manager.perform_full_sync()
            
            # Recarregar crews após sincronização
            self.reload_crews_from_database()
            
            return result
        except Exception as e:
            print(f"❌ Erro na sincronização manual: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_sync_status(self) -> Dict:
        """Retorna status atual da sincronização"""
        try:
            return {
                'sync_available': True,
                'last_sync': 'Sistema ativo',
                'crews_in_database': len(self.db_manager.get_all_crew_configs()),
                'crews_in_memory': len(self.crews),
                'sync_manager_status': 'Ativo',
                'auto_sync_enabled': True
            }
        except Exception as e:
            return {
                'sync_available': False,
                'error': str(e),
                'sync_manager_status': 'Erro',
                'auto_sync_enabled': False
            }
    
    def _validate_agents_tools(self, crew) -> bool:
        """Valida se todos os agentes da crew possuem pelo menos uma ferramenta configurada. Exibe todos os agentes inválidos."""
        invalid_agents = []
        for agent in crew.agents:
            tools = getattr(agent, 'tools', [])
            if not tools or len(tools) == 0:
                invalid_agents.append(getattr(agent, 'role', 'Desconhecido'))
        if invalid_agents:
            print(f"⚠️ Os seguintes agentes estão sem ferramentas configuradas: {', '.join(invalid_agents)}")
            return False
        return True
