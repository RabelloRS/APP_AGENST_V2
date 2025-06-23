"""
Gerenciador de tarefas para o sistema
"""

import os
from typing import Dict, List, Optional

import yaml
from crewai import Task


class TaskManager:
    """Classe para gerenciar tarefas do sistema usando arquivos YAML"""

    def __init__(self, config_path: str = "app/config/tasks.yaml"):
        self.config_path = config_path
        self.tasks: Dict[str, Task] = {}
        self.available_tasks = self._load_task_configs()

    def _load_task_configs(self) -> Dict:
        """Carrega as configurações das tarefas do arquivo YAML"""
        try:
            if not os.path.exists(self.config_path):
                print(f"Arquivo de configuração não encontrado: {self.config_path}")
                return {}

            with open(self.config_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs or {}

        except Exception as e:
            print(f"Erro ao carregar configurações das tarefas: {e}")
            return {}

    def reload_configs(self) -> bool:
        """Recarrega as configurações das tarefas do arquivo YAML"""
        try:
            self.available_tasks = self._load_task_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False

    def create_task(self, task_type: str, agent, **kwargs) -> Optional[Task]:
        """Cria uma nova tarefa do tipo especificado"""
        if task_type not in self.available_tasks:
            print(f"Tipo de tarefa '{task_type}' não encontrado nas configurações")
            return None

        task_config = self.available_tasks[task_type].copy()

        # Sobrescrever configurações padrão com kwargs
        task_config.update(kwargs)

        try:
            task = Task(
                description=task_config["description"], expected_output=task_config["expected_output"], agent=agent
            )

            self.tasks[task_type] = task
            return task

        except Exception as e:
            print(f"Erro ao criar tarefa {task_type}: {e}")
            return None

    def create_task_with_params(self, task_type: str, agent, **params) -> Optional[Task]:
        """Cria uma tarefa substituindo parâmetros na descrição"""
        try:
            print(f"🔧 Debug: Criando tarefa '{task_type}' para agente '{getattr(agent, 'role', 'Unknown')}'")

            if task_type not in self.available_tasks:
                print(f"❌ Tipo de tarefa '{task_type}' não encontrado nas configurações")
                print(f"   Tarefas disponíveis: {list(self.available_tasks.keys())}")
                return None

            task_config = self.available_tasks[task_type].copy()
            print(f"✅ Configuração da tarefa carregada: {task_config.get('description', 'Sem descrição')[:50]}...")

            # Substituir parâmetros na descrição
            description = task_config["description"]
            for key, value in params.items():
                description = description.replace(f"{{{key}}}", str(value))

            task_config["description"] = description

            print(f"🔧 Debug: Criando objeto Task com descrição: {description[:50]}...")

            # Criar tarefa usando a sintaxe correta do CrewAI
            task = Task(
                description=task_config["description"], expected_output=task_config["expected_output"], agent=agent
            )

            print(f"✅ Tarefa '{task_type}' criada com sucesso!")
            return task

        except Exception as e:
            print(f"❌ Erro ao criar tarefa {task_type}: {e}")
            print(f"   Tipo de erro: {type(e).__name__}")
            import traceback

            traceback.print_exc()
            return None

    def get_task(self, task_type: str) -> Optional[Task]:
        """Retorna uma tarefa existente"""
        return self.tasks.get(task_type)

    def get_all_tasks(self) -> Dict[str, Task]:
        """Retorna todas as tarefas criadas"""
        return self.tasks

    def list_available_task_types(self) -> List[str]:
        """Lista todos os tipos de tarefas disponíveis"""
        return list(self.available_tasks.keys())

    def get_task_info(self, task_type: str) -> Optional[Dict]:
        """Retorna informações sobre um tipo de tarefa"""
        return self.available_tasks.get(task_type)

    def get_task_configs(self) -> Dict:
        """Retorna todas as configurações de tarefas"""
        return self.available_tasks.copy()
