"""
Gerenciador de logs para capturar e exibir logs em tempo real na interface
"""

import logging
from typing import List, Optional
from datetime import datetime
import streamlit as st


class StreamlitLogHandler(logging.Handler):
    """Handler personalizado para capturar logs e exibir no Streamlit"""

    def __init__(self):
        super().__init__()
        self.log_buffer = []
        self.max_logs = 1000  # Máximo de logs para manter em memória

    def emit(self, record):
        """Captura e armazena o log"""
        try:
            log_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "level": record.levelname,
                "message": self.format(record),
                "raw_message": record.getMessage(),
            }

            self.log_buffer.append(log_entry)

            # Manter apenas os últimos logs
            if len(self.log_buffer) > self.max_logs:
                self.log_buffer = self.log_buffer[-self.max_logs :]

        except Exception:
            self.handleError(record)

    def get_logs(self) -> List[dict]:
        """Retorna todos os logs capturados"""
        return self.log_buffer.copy()

    def get_recent_logs(self, count: int = 50) -> List[dict]:
        """Retorna os logs mais recentes"""
        return self.log_buffer[-count:] if self.log_buffer else []

    def clear_logs(self):
        """Limpa todos os logs"""
        self.log_buffer.clear()


class LogManager:
    """Gerenciador principal de logs para a aplicação"""

    def __init__(self):
        self.handler = StreamlitLogHandler()
        self.logger = logging.getLogger("crew_execution")
        self.logger.setLevel(logging.INFO)

        # Configurar formato do log
        formatter = logging.Formatter("%(message)s")
        self.handler.setFormatter(formatter)

        # Adicionar handler se não existir
        if not self.logger.handlers:
            self.logger.addHandler(self.handler)

    def start_capture(self):
        """Inicia a captura de logs"""
        self.handler.clear_logs()

    def stop_capture(self):
        """Para a captura de logs"""
        pass  # Não faz nada, apenas para compatibilidade

    def log_info(self, message: str):
        """Registra uma mensagem de informação"""
        self.logger.info(message)

    def log_debug(self, message: str):
        """Registra uma mensagem de debug"""
        self.logger.debug(message)

    def log_warning(self, message: str):
        """Registra uma mensagem de aviso"""
        self.logger.warning(message)

    def log_error(self, message: str):
        """Registra uma mensagem de erro"""
        self.logger.error(message)

    def get_logs(self) -> List[dict]:
        """Retorna todos os logs capturados"""
        return self.handler.get_logs()

    def get_recent_logs(self, count: int = 50) -> List[dict]:
        """Retorna os logs mais recentes"""
        return self.handler.get_recent_logs(count)

    def clear_logs(self):
        """Limpa todos os logs"""
        self.handler.clear_logs()

    def format_log_for_display(self, log_entry: dict) -> str:
        """Formata um log para exibição"""
        timestamp = log_entry["timestamp"]
        level = log_entry["level"]
        message = log_entry["message"]

        # Aplicar cores baseadas no nível
        if level == "ERROR":
            return f"🔴 **{timestamp}** - {message}"
        elif level == "WARNING":
            return f"🟡 **{timestamp}** - {message}"
        elif level == "INFO":
            return f"🔵 **{timestamp}** - {message}"
        else:
            return f"⚪ **{timestamp}** - {message}"

    def display_logs_in_streamlit(self, container=None, max_logs: int = 100):
        """Exibe os logs em um container do Streamlit"""
        logs = self.get_recent_logs(max_logs)

        if container is None:
            container = st.container()

        with container:
            if logs:
                # Criar uma string com todos os logs formatados
                log_text = ""
                for log_entry in logs[-50:]:  # Mostrar apenas os últimos 50
                    formatted_log = self.format_log_for_display(log_entry)
                    log_text += formatted_log + "\n\n"

                # Exibir em um container scrollável
                st.markdown("### 📊 Logs de Execução em Tempo Real")
                st.markdown(log_text)
            else:
                st.info("Nenhum log disponível ainda.")


# Instância global do gerenciador de logs
log_manager = LogManager()
