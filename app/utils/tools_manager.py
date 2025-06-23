"""
Gerenciador de Tools (Ferramentas) para o sistema
"""

import os
from typing import Any, Dict, List, Optional

import yaml

from app.utils.tools import (
    analyze_excel_similarity,
    compare_text_similarity,
    detect_common_prefixes,
    detect_common_suffixes,
    detect_data_patterns,
    detect_outliers,
    generate_excel_report,
    generate_similarity_recommendations,
    read_excel_column,
    read_excel_file,
    validate_excel_file,
    simple_research_tool,
    # Ferramentas de avaliação
    crew_performance_analyzer,
    agent_output_quality_checker,
    tool_usage_evaluator,
    workflow_efficiency_analyzer,
    recommendation_generator,
    execution_summary_builder,
)


class ToolsManager:
    """Classe para gerenciar tools (ferramentas) do sistema"""

    def __init__(self, config_path: str = "app/config/tools.yaml"):
        self.config_path = config_path
        self.tools_functions = self._register_tools_functions()
        self.available_tools = self._load_tools_configs()

        # Garantir que todas as ferramentas registradas estejam na configuração
        self._sync_tools_config()

    def _load_tools_configs(self) -> Dict:
        """Carrega as configurações das tools do arquivo YAML"""
        try:
            if not os.path.exists(self.config_path):
                # Criar arquivo padrão se não existir
                self._create_default_tools_config()

            with open(self.config_path, "r", encoding="utf-8") as file:
                configs = yaml.safe_load(file)
                return configs or {}

        except Exception as e:
            print(f"Erro ao carregar configurações das tools: {e}")
            return {}

    def _create_default_tools_config(self):
        """Cria configuração padrão das tools"""
        default_config = {
            "read_excel_column": {
                "name": "Ler Coluna Excel",
                "description": "Lê uma coluna específica de um arquivo Excel e retorna os dados como lista",
                "category": "Excel",
                "parameters": {
                    "file_path": "Caminho do arquivo Excel",
                    "column_name": "Nome da coluna a ser lida",
                },
                "returns": "Lista com os dados da coluna",
                "example": "read_excel_column('dados.xlsx', 'Material')",
            },
            "read_excel_file": {
                "name": "Ler Arquivo Excel",
                "description": "Lê um arquivo Excel completo e retorna informações estruturadas sobre sua estrutura",
                "category": "Excel",
                "parameters": {"file_path": "Caminho do arquivo Excel"},
                "returns": "Dicionário com informações do arquivo (colunas, linhas, tipos de dados, etc.)",
                "example": "read_excel_file('dados.xlsx')",
            },
            "compare_text_similarity": {
                "name": "Comparar Similaridade de Texto",
                "description": "Compara a similaridade entre duas listas de textos usando algoritmos fuzzy matching",
                "category": "Análise",
                "parameters": {
                    "list1": "Primeira lista de textos",
                    "list2": "Segunda lista de textos",
                },
                "returns": "Dicionário com correspondências e scores de similaridade",
                "example": "compare_text_similarity(['cimento', 'areia'], ['cimento portland', 'areia média'])",
            },
            "analyze_excel_similarity": {
                "name": "Análise de Similaridade Excel",
                "description": "Realiza análise completa de similaridade entre duas planilhas Excel",
                "category": "Excel",
                "parameters": {
                    "file1_path": "Caminho do primeiro arquivo Excel",
                    "file2_path": "Caminho do segundo arquivo Excel",
                    "column1": "Nome da coluna no primeiro arquivo",
                    "column2": "Nome da coluna no segundo arquivo",
                },
                "returns": "Análise completa com estatísticas e recomendações",
                "example": "analyze_excel_similarity('orcamento1.xlsx', 'orcamento2.xlsx', 'Material', 'Descrição')",
            },
            "detect_data_patterns": {
                "name": "Detectar Padrões nos Dados",
                "description": "Analisa uma coluna de dados e detecta padrões, tipos de dados e características",
                "category": "Análise",
                "parameters": {
                    "file_path": "Caminho do arquivo Excel",
                    "column_name": "Nome da coluna a ser analisada",
                },
                "returns": "Dicionário com padrões detectados nos dados",
                "example": "detect_data_patterns('dados.xlsx', 'Preço')",
            },
            "generate_excel_report": {
                "name": "Gerar Relatório Excel",
                "description": "Gera um relatório estruturado baseado nos resultados de análise",
                "category": "Relatórios",
                "parameters": {"analysis_results": "Resultados da análise (dicionário)"},
                "returns": "Relatório formatado em texto",
                "example": "generate_excel_report(resultados_analise)",
            },
            "validate_excel_file": {
                "name": "Validar Arquivo Excel",
                "description": "Valida um arquivo Excel e retorna informações sobre sua estrutura e qualidade",
                "category": "Excel",
                "parameters": {"file_path": "Caminho do arquivo Excel"},
                "returns": "Dicionário com informações de validação",
                "example": "validate_excel_file('dados.xlsx')",
            },
            "simple_research_tool": {
                "name": "Pesquisa Simples",
                "description": "Realiza pesquisa sobre um tópico específico e retorna informações estruturadas",
                "category": "Pesquisa",
                "parameters": {"topic": "Tópico a ser pesquisado"},
                "returns": "Informações estruturadas sobre o tópico",
                "example": "simple_research_tool('projetos de fundação de pontes')",
            },
        }

        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    default_config,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )
            print(f"Arquivo de configuração de tools criado: {self.config_path}")
        except Exception as e:
            print(f"Erro ao criar arquivo de configuração de tools: {e}")

    def _register_tools_functions(self) -> Dict[str, Any]:
        """Registra as funções das tools disponíveis"""
        return {
            # Ferramentas originais
            "read_excel_column": read_excel_column,
            "read_excel_file": read_excel_file,
            "compare_text_similarity": compare_text_similarity,
            "analyze_excel_similarity": analyze_excel_similarity,
            "generate_similarity_recommendations": generate_similarity_recommendations,
            "detect_data_patterns": detect_data_patterns,
            "detect_common_prefixes": detect_common_prefixes,
            "detect_common_suffixes": detect_common_suffixes,
            "detect_outliers": detect_outliers,
            "generate_excel_report": generate_excel_report,
            "validate_excel_file": validate_excel_file,
            "simple_research_tool": simple_research_tool,
            # Ferramentas de avaliação de crews
            "crew_performance_analyzer": crew_performance_analyzer,
            "agent_output_quality_checker": agent_output_quality_checker,
            "tool_usage_evaluator": tool_usage_evaluator,
            "workflow_efficiency_analyzer": workflow_efficiency_analyzer,
            "recommendation_generator": recommendation_generator,
            "execution_summary_builder": execution_summary_builder,
        }

    def _sync_tools_config(self):
        """Sincroniza as ferramentas do código com o arquivo de configuração."""
        config_changed = False
        for tool_name, tool_func in self.tools_functions.items():
            if tool_name not in self.available_tools:
                print(f"🔧 Adicionando nova ferramenta à configuração: {tool_name}")
                self.available_tools[tool_name] = {
                    "name": tool_name.replace("_", " ").title(),
                    "description": tool_func.__doc__ or f"Descrição da ferramenta {tool_name}",
                    "category": "Não categorizada",
                }
                config_changed = True

        if config_changed:
            print("💾 Salvando configuração de ferramentas atualizada...")
            self._save_configs_to_file()

    def reload_configs(self) -> bool:
        """Recarrega as configurações das tools do arquivo YAML"""
        try:
            self.available_tools = self._load_tools_configs()
            return True
        except Exception as e:
            print(f"Erro ao recarregar configurações: {e}")
            return False

    def list_available_tools(self) -> List[str]:
        """Lista todas as tools disponíveis"""
        return list(self.available_tools.keys())

    def get_tool_info(self, tool_name: str) -> Optional[Dict]:
        """Retorna informações sobre uma tool específica"""
        return self.available_tools.get(tool_name)

    def get_tools_by_category(self) -> Dict[str, List[str]]:
        """Agrupa tools por categoria"""
        categories = {}
        for tool_name, tool_info in self.available_tools.items():
            category = tool_info.get("category", "Outros")
            if category not in categories:
                categories[category] = []
            categories[category].append(tool_name)
        return categories

    def get_tool_function(self, tool_name: str):
        """Retorna a função de uma tool. Se não for customizada, retorna None (apenas para tools locais)."""
        # Primeiro tenta buscar entre as customizadas
        return self.tools_functions.get(tool_name)

    def get_tool_class(self, tool_name: str):
        """Tenta importar e retornar a classe de uma tool nativa do crewai_tools pelo nome exato."""
        try:
            import importlib

            module_name = f"crewai_tools.tools.{tool_name.lower()}"
            tool_module = importlib.import_module(module_name)
            tool_class = getattr(tool_module, tool_name)
            return tool_class
        except Exception:
            return None

    def get_tools_for_agent(self, agent_type: str) -> List[str]:
        """Retorna as tools atribuídas a um agente específico"""
        # Por enquanto, retorna todas as tools
        # Isso pode ser expandido para ter configuração específica por agente
        return self.list_available_tools()

    def update_tool_config(self, tool_name: str, new_config: Dict) -> bool:
        """Atualiza a configuração de uma tool"""
        try:
            if tool_name not in self.available_tools:
                print(f"Tool '{tool_name}' não encontrada")
                return False

            # Atualizar configuração na memória
            self.available_tools[tool_name].update(new_config)

            # Salvar no arquivo YAML
            return self._save_configs_to_file()

        except Exception as e:
            print(f"Erro ao atualizar configuração da tool {tool_name}: {e}")
            return False

    def _save_configs_to_file(self) -> bool:
        """Salva as configurações atuais no arquivo YAML"""
        try:
            # Criar backup do arquivo original
            backup_path = f"{self.config_path}.backup"
            if os.path.exists(self.config_path):
                import shutil

                shutil.copy2(self.config_path, backup_path)

            # Salvar nova configuração
            with open(self.config_path, "w", encoding="utf-8") as file:
                yaml.dump(
                    self.available_tools,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            print(f"Configurações de tools salvas com sucesso em {self.config_path}")
            return True

        except Exception as e:
            print(f"Erro ao salvar configurações de tools: {e}")
            return False
