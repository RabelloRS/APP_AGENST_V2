"""
Gerenciador de agentes para o sistema
"""

import os
from typing import Dict, List, Optional, Type, Callable
from pydantic import BaseModel, Field

import yaml
from crewai import Agent
from crewai.tools import BaseTool  # Corrigido: importa BaseTool do CrewAI


class GenericArgsSchema(BaseModel):
    argumento: str = Field(..., description="Argumento genérico para a ferramenta.")


class AgentManager:
    """Classe para gerenciar agentes do sistema usando arquivos YAML"""

    def __init__(
        self,
        config_path: str = "app/config/agents.yaml",
        tools_config_path: str = "app/config/agent_tools.yaml",
    ):
        self.config_path = config_path
        self.tools_config_path = tools_config_path
        self.agents: Dict[str, Agent] = {}
        self.available_agents = self._load_agent_configs()
        self.agent_tools = self._load_agent_tools_configs()
        self.tools_manager = None  # Será configurado posteriormente

    def set_tools_manager(self, tools_manager):
        """Define o gerenciador de tools para este agent manager"""
        self.tools_manager = tools_manager

    def _load_agent_configs(self) -> Dict:
        """Carrega as configurações dos agentes do arquivo YAML"""
        try:
            if not os.path.exists(self.config_path):
                print(f"Arquivo de configuração não encontrado: {self.config_path}")
                return {}

            with open(self.config_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs or {}

        except Exception as e:
            print(f"Erro ao carregar configurações dos agentes: {e}")
            return {}

    def _load_agent_tools_configs(self) -> Dict:
        """Carrega as configurações de tools dos agentes"""
        try:
            if not os.path.exists(self.tools_config_path):
                # Criar arquivo padrão se não existir
                self._create_default_agent_tools_config()

            with open(self.tools_config_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs or {}

        except Exception as e:
            print(f"Erro ao carregar configurações de tools dos agentes: {e}")
            return {}

    def _create_default_agent_tools_config(self):
        """Cria configuração padrão de tools para agentes"""
        default_config = {
            "researcher": {
                "tools": [
                    "simple_research_tool",
                    "read_excel_file",
                    "compare_text_similarity",
                ],
                "description": "Tools para pesquisa e coleta de informações",
            },
            "analyst": {
                "tools": [
                    "analyze_excel_similarity",
                    "detect_data_patterns",
                    "generate_excel_report",
                ],
                "description": "Tools para análise avançada e geração de relatórios",
            },
            "writer": {
                "tools": ["generate_excel_report"],
                "description": "Tools para geração de conteúdo e relatórios",
            },
            "reviewer": {
                "tools": ["validate_excel_file", "detect_data_patterns"],
                "description": "Tools para validação e revisão de dados",
            },
            "coordinator": {
                "tools": ["read_excel_file", "validate_excel_file"],
                "description": "Tools básicas para coordenação",
            },
            "excel_analyst": {
                "tools": [
                    "read_excel_column",
                    "read_excel_file",
                    "analyze_excel_similarity",
                    "detect_data_patterns",
                    "generate_excel_report",
                    "validate_excel_file",
                ],
                "description": "Todas as tools relacionadas a análise de Excel",
            },
        }

        try:
            with open(self.tools_config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    default_config,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            print(
                f"Arquivo de configuração de tools dos agentes criado: {self.tools_config_path}"
            )
        except Exception as e:
            print(f"Erro ao criar arquivo de configuração de tools dos agentes: {e}")

    def _create_tool_objects(self, tool_names: List[str]) -> List[BaseTool]:
        """Cria objetos Tool compatíveis com CrewAI (prioriza nativas, fallback para customizadas)"""
        if not self.tools_manager:
            print("❌ ToolsManager não configurado")
            return []

        import re

        def camel_to_snake(name):
            s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        tools = []
        for tool_name in tool_names:
            tool_instance = None
            # 1. Tenta importar ferramenta nativa do crewai_tools pelo nome
            try:
                import importlib
                module_name = f"crewai_tools.tools.{camel_to_snake(tool_name)}"
                tool_module = importlib.import_module(module_name)
                tool_class = getattr(tool_module, tool_name)
                tool_instance = tool_class()
            except Exception:
                # 2. Fallback: ferramenta customizada - usar como função simples
                tool_function = self.tools_manager.get_tool_function(tool_name)
                if tool_function:
                    # Para ferramentas customizadas, vamos usar uma abordagem mais simples
                    # ou pular se não conseguirmos criar uma tool válida
                    print(f"⚠️ Tool customizada '{tool_name}' disponível como função, mas não como tool CrewAI")
                    continue
                else:
                    print(f"⚠️ Tool '{tool_name}' não encontrada")
                    continue
            tools.append(tool_instance)
        return tools

    def reload_configs(self) -> bool:
        """Recarrega as configurações dos agentes do arquivo YAML"""
        try:
            self.available_agents = self._load_agent_configs()
            self.agent_tools = self._load_agent_tools_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False

    def create_agent(
        self, agent_type: str, tools: Optional[list] = None, **kwargs
    ) -> Optional[Agent]:
        """Cria um agente do tipo especificado"""
        try:
            if agent_type not in self.available_agents:
                print(f"Tipo de agente '{agent_type}' não encontrado")
                return None

            agent_config = self.available_agents[agent_type]

            # Obter tools do agente se não especificadas
            if tools is None:
                agent_tools_config = self.agent_tools.get(agent_type, {})
                tool_names = agent_tools_config.get("tools", [])
                tools = self._create_tool_objects(tool_names)

            # Criar agente
            agent = Agent(
                role=agent_config.get("role", ""),
                goal=agent_config.get("goal", ""),
                backstory=agent_config.get("backstory", ""),
                tools=tools,
                verbose=agent_config.get("verbose", True),
                allow_delegation=agent_config.get("allow_delegation", False),
                **kwargs
            )

            self.agents[agent_type] = agent
            return agent

        except Exception as e:
            print(f"Erro ao criar agente {agent_type}: {e}")
            return None

    def get_agent(self, agent_type: str) -> Optional[Agent]:
        """Retorna um agente específico"""
        return self.agents.get(agent_type)

    def get_all_agents(self) -> Dict[str, Agent]:
        """Retorna todos os agentes criados"""
        return self.agents

    def list_available_agent_types(self) -> List[str]:
        """Lista todos os tipos de agentes disponíveis"""
        return list(self.available_agents.keys())

    def get_agent_info(self, agent_type: str) -> Optional[Dict]:
        """Retorna informações de um agente específico"""
        return self.available_agents.get(agent_type)

    def get_agent_configs(self) -> Dict:
        """Retorna todas as configurações de agentes"""
        return self.available_agents

    def get_agent_tools(self, agent_type: str) -> List[str]:
        """Retorna as tools de um agente específico (agora só do agents.yaml)"""
        agent_config = self.available_agents.get(agent_type, {})
        return agent_config.get("tools", [])

    def update_agent_tools(self, agent_type: str, tools: List[str]) -> bool:
        """Atualiza as tools de um agente específico"""
        try:
            if agent_type not in self.agent_tools:
                self.agent_tools[agent_type] = {"tools": [], "description": ""}

            self.agent_tools[agent_type]["tools"] = tools
            return self._save_agent_tools_to_file()

        except Exception as e:
            print(f"Erro ao atualizar tools do agente {agent_type}: {e}")
            return False

    def _save_agent_tools_to_file(self) -> bool:
        """Salva as configurações de tools dos agentes no arquivo YAML"""
        try:
            with open(self.tools_config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    self.agent_tools,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações de tools dos agentes: {e}")
            return False

    def update_agent_config(self, agent_type: str, new_config: Dict) -> bool:
        """Atualiza a configuração de um agente específico"""
        try:
            if agent_type not in self.available_agents:
                print(f"Tipo de agente '{agent_type}' não encontrado")
                return False

            self.available_agents[agent_type].update(new_config)
            return self._save_configs_to_file()

        except Exception as e:
            print(f"Erro ao atualizar configuração do agente {agent_type}: {e}")
            return False

    def _save_configs_to_file(self) -> bool:
        """Salva as configurações dos agentes no arquivo YAML"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    self.available_agents,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            return True
        except Exception as e:
            print(f"Erro ao salvar configurações dos agentes: {e}")
            return False

    def rename_agent(self, old_type: str, new_type: str) -> bool:
        """Renomeia um tipo de agente"""
        try:
            if old_type not in self.available_agents:
                print(f"Tipo de agente '{old_type}' não encontrado")
                return False

            if new_type in self.available_agents:
                print(f"Tipo de agente '{new_type}' já existe")
                return False

            # Mover configuração
            self.available_agents[new_type] = self.available_agents.pop(old_type)

            # Mover tools se existir
            if old_type in self.agent_tools:
                self.agent_tools[new_type] = self.agent_tools.pop(old_type)

            # Mover agente criado se existir
            if old_type in self.agents:
                self.agents[new_type] = self.agents.pop(old_type)

            # Salvar alterações
            self._save_configs_to_file()
            self._save_agent_tools_to_file()

            return True

        except Exception as e:
            print(f"Erro ao renomear agente {old_type} para {new_type}: {e}")
            return False
