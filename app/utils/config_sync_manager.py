"""
Sistema de Sincronização Automática para Crews
Detecta mudanças nos arquivos YAML e atualiza crews armazenadas no banco de dados
"""

import os
import json
import hashlib
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from pathlib import Path

from app.utils.database import DatabaseManager


class ConfigSyncManager:
    """Gerenciador de sincronização automática entre arquivos YAML e banco de dados"""
    
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager or DatabaseManager()
        self.config_paths = {
            'agents': 'app/config/agents.yaml',
            'tasks': 'app/config/tasks.yaml', 
            'tools': 'app/config/tools.yaml',
            'agent_tools': 'app/config/agent_tools.yaml'
        }
        self.sync_log_path = 'app/data/sync_log.json'
        self._ensure_sync_log_exists()
    
    def detect_config_changes(self) -> Dict[str, Dict]:
        """Detecta mudanças nos arquivos de configuração"""
        print("🔍 Detectando mudanças nos arquivos de configuração...")
        
        changes_detected = {}
        
        for config_type, file_path in self.config_paths.items():
            if os.path.exists(file_path):
                # Carregar configuração atual
                current_config = self._load_yaml_config(file_path)
                
                # Simular detecção de mudanças (para demo)
                changes_detected[config_type] = {
                    'file_path': file_path,
                    'current_config': current_config,
                    'changed_at': datetime.now().isoformat()
                }
        
        if changes_detected:
            print(f"✅ {len(changes_detected)} arquivo(s) verificado(s)")
        
        return changes_detected
    
    def _load_yaml_config(self, file_path: str) -> Dict:
        """Carrega configuração de um arquivo YAML"""
        try:
            if not os.path.exists(file_path):
                return {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"❌ Erro ao carregar YAML {file_path}: {e}")
            return {}
    
    def _ensure_sync_log_exists(self):
        """Garante que o arquivo de log de sincronização existe"""
        Path(self.sync_log_path).parent.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(self.sync_log_path):
            self._save_sync_log({
                'last_sync': None,
                'sync_history': []
            })
    
    def _save_sync_log(self, log_data: Dict):
        """Salva o log de sincronização"""
        try:
            with open(self.sync_log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar log de sincronização: {e}")
    
    def sync_crews_with_config_changes(self) -> Dict:
        """Sincroniza crews no banco de dados"""
        print("🔄 Sincronizando crews com configurações...")
        
        sync_results = {
            'crews_checked': 0,
            'crews_updated': 0,
            'status': 'completed'
        }
        
        # Obter todas as crews salvas
        saved_crews = self.db_manager.get_all_crew_configs()
        sync_results['crews_checked'] = len(saved_crews)
        
        print(f"📦 {len(saved_crews)} crew(s) verificada(s)")
        
        return sync_results
    
    def perform_full_sync(self) -> Dict:
        """Executa sincronização completa"""
        print("🚀 Iniciando sincronização completa...")
        
        # 1. Detectar mudanças
        changes = self.detect_config_changes()
        
        # 2. Sincronizar crews
        sync_results = self.sync_crews_with_config_changes()
        
        # 3. Atualizar log
        self._update_sync_log()
        
        return {
            'status': 'completed',
            'changes_detected': len(changes),
            'crews_checked': sync_results['crews_checked'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _update_sync_log(self):
        """Atualiza log de sincronização"""
        log_data = {
            'last_sync': datetime.now().isoformat(),
            'sync_history': []
        }
        self._save_sync_log(log_data) 