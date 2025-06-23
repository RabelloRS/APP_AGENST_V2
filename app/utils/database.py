"""
Sistema de banco de dados para armazenar resultados e histórico de crews
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path


class DatabaseManager:
    """Gerenciador de banco de dados SQLite para o sistema"""

    def __init__(self, db_path: str = "app/data/crews_database.db"):
        self.db_path = db_path
        self._ensure_data_directory()
        self._create_tables()

    def _ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _create_tables(self):
        """Cria as tabelas necessárias se não existirem"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabela de execuções
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crew_name TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration TEXT,
                    status TEXT DEFAULT 'running',
                    result TEXT,
                    error_message TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Tabela de resultados detalhados
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS execution_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER,
                    agent_name TEXT,
                    task_description TEXT,
                    task_result TEXT,
                    task_status TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES executions (id)
                )
            """
            )

            # Tabela de configurações de crews (backup)
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS crew_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crew_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    agent_types TEXT,  -- JSON array
                    task_types TEXT,   -- JSON array
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    def save_execution(self, crew_name: str, topic: str, start_time: datetime) -> int:
        """Salva uma nova execução e retorna o ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO executions (crew_name, topic, start_time)
                VALUES (?, ?, ?)
            """,
                (crew_name, topic, start_time.isoformat()),
            )
            conn.commit()
            result = cursor.lastrowid
            if result is None:
                raise Exception("Falha ao inserir execução no banco de dados")
            return result

    def update_execution_result(
        self,
        execution_id: int,
        result: str,
        end_time: datetime,
        duration: str,
        status: str = "completed",
        error_message: Optional[str] = None,
    ):
        """Atualiza o resultado de uma execução"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE executions 
                SET result = ?, end_time = ?, duration = ?, status = ?, error_message = ?
                WHERE id = ?
            """,
                (result, end_time.isoformat(), duration, status, error_message, execution_id),
            )
            conn.commit()

    def save_task_result(
        self,
        execution_id: int,
        agent_name: str,
        task_description: str,
        task_result: str,
        task_status: str = "completed",
    ):
        """Salva o resultado de uma tarefa específica"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO execution_results 
                (execution_id, agent_name, task_description, task_result, task_status)
                VALUES (?, ?, ?, ?, ?)
            """,
                (execution_id, agent_name, task_description, task_result, task_status),
            )
            conn.commit()

    def get_execution_history(self) -> List[Dict]:
        """Retorna o histórico completo de execuções"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, crew_name, topic, start_time, end_time, duration, 
                       status, result, error_message, created_at
                FROM executions 
                ORDER BY created_at DESC
            """
            )

            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_execution_details(self, execution_id: int) -> Optional[Dict]:
        """Retorna detalhes de uma execução específica"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Buscar execução principal
            cursor.execute(
                """
                SELECT id, crew_name, topic, start_time, end_time, duration, 
                       status, result, error_message, created_at
                FROM executions 
                WHERE id = ?
            """,
                (execution_id,),
            )

            execution = cursor.fetchone()
            if not execution:
                return None

            columns = [description[0] for description in cursor.description]
            execution_dict = dict(zip(columns, execution))

            # Buscar resultados das tarefas
            cursor.execute(
                """
                SELECT agent_name, task_description, task_result, task_status, created_at
                FROM execution_results 
                WHERE execution_id = ?
                ORDER BY created_at
            """,
                (execution_id,),
            )

            task_columns = [description[0] for description in cursor.description]
            execution_dict["task_results"] = [dict(zip(task_columns, row)) for row in cursor.fetchall()]

            return execution_dict

    def save_crew_config(self, crew_name: str, description: str, agent_types: List[str], task_types: List[str]):
        """Salva configuração de uma crew"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO crew_configs 
                (crew_name, description, agent_types, task_types, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (crew_name, description, json.dumps(agent_types), json.dumps(task_types), datetime.now().isoformat()),
            )
            conn.commit()

    def get_crew_config(self, crew_name: str) -> Optional[Dict]:
        """Retorna configuração de uma crew"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT crew_name, description, agent_types, task_types, created_at, updated_at
                FROM crew_configs 
                WHERE crew_name = ?
            """,
                (crew_name,),
            )

            row = cursor.fetchone()
            if not row:
                return None

            return {
                "crew_name": row[0],
                "description": row[1],
                "agent_types": json.loads(row[2]),
                "task_types": json.loads(row[3]),
                "created_at": row[4],
                "updated_at": row[5],
            }

    def delete_crew_config(self, crew_name: str) -> bool:
        """Remove configuração de uma crew"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM crew_configs WHERE crew_name = ?", (crew_name,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_crew_configs(self) -> List[Dict]:
        """Retorna todas as configurações de crews"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT crew_name, description, agent_types, task_types, created_at, updated_at
                FROM crew_configs 
                ORDER BY updated_at DESC
            """
            )

            results = []
            for row in cursor.fetchall():
                results.append(
                    {
                        "crew_name": row[0],
                        "description": row[1],
                        "agent_types": json.loads(row[2]) if row[2] else [],
                        "task_types": json.loads(row[3]) if row[3] else [],
                        "created_at": row[4],
                        "updated_at": row[5],
                    }
                )

            return results

    def search_executions(self, query: str) -> List[Dict]:
        """Busca execuções por texto"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, crew_name, topic, start_time, end_time, duration, 
                       status, result, error_message, created_at
                FROM executions 
                WHERE crew_name LIKE ? OR topic LIKE ? OR result LIKE ?
                ORDER BY created_at DESC
            """,
                (f"%{query}%", f"%{query}%", f"%{query}%"),
            )

            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_statistics(self) -> Dict:
        """Retorna estatísticas do banco de dados"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total de execuções
            cursor.execute("SELECT COUNT(*) FROM executions")
            total_executions = cursor.fetchone()[0]

            # Execuções bem-sucedidas
            cursor.execute("SELECT COUNT(*) FROM executions WHERE status = 'completed'")
            successful_executions = cursor.fetchone()[0]

            # Total de crews configuradas
            cursor.execute("SELECT COUNT(*) FROM crew_configs")
            total_crews = cursor.fetchone()[0]

            # Crew mais executada
            cursor.execute(
                """
                SELECT crew_name, COUNT(*) as count 
                FROM executions 
                GROUP BY crew_name 
                ORDER BY count DESC 
                LIMIT 1
            """
            )
            most_executed = cursor.fetchone()

            return {
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "total_crews": total_crews,
                "most_executed_crew": most_executed[0] if most_executed else None,
                "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0,
            }

    def save_evaluation_report(self, execution_id: int, evaluation_report: str):
        """Salva relatório de avaliação para uma execução específica"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Verificar se a tabela de relatórios de avaliação existe
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS evaluation_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id INTEGER,
                    evaluation_report TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (execution_id) REFERENCES executions (id)
                )
            """
            )

            # Inserir relatório de avaliação
            cursor.execute(
                """
                INSERT INTO evaluation_reports (execution_id, evaluation_report)
                VALUES (?, ?)
            """,
                (execution_id, evaluation_report),
            )

            conn.commit()

    def get_evaluation_report(self, execution_id: int) -> Optional[str]:
        """Recupera relatório de avaliação para uma execução específica"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT evaluation_report FROM evaluation_reports 
                WHERE execution_id = ? 
                ORDER BY created_at DESC 
                LIMIT 1
            """,
                (execution_id,),
            )

            result = cursor.fetchone()
            return result[0] if result else None
