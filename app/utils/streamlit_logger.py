"""
Componente Streamlit para exibir logs em tempo real
"""

import streamlit as st
import time
from typing import List, Dict
from datetime import datetime
from app.utils.log_manager import log_manager


class StreamlitLogger:
    """Componente para exibir logs em tempo real no Streamlit"""

    def __init__(self, container=None):
        self.container = container or st.container()
        self.displayed_logs = []
        self.last_update = datetime.now()

    def display_logs_realtime(self, max_logs: int = 50, auto_scroll: bool = True):
        """Exibe logs em tempo real com formatação adequada"""
        current_logs = log_manager.get_recent_logs(max_logs)

        # Verificar se há novos logs
        if len(current_logs) != len(self.displayed_logs):
            self.displayed_logs = current_logs
            self._update_display()

    def _update_display(self):
        """Atualiza a exibição dos logs"""
        with self.container:
            if self.displayed_logs:
                # Criar HTML personalizado para melhor formatação
                html_content = self._create_log_html()

                # Usar HTML para exibição mais rica
                st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.info("🔄 Aguardando logs de execução...")

    def _create_log_html(self) -> str:
        """Cria HTML formatado para os logs"""
        html = """
        <div style="
            max-height: 400px; 
            overflow-y: auto; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
            padding: 10px;
            background-color: #f8f9fa;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        ">
        """

        for log_entry in self.displayed_logs[-30:]:  # Últimos 30 logs
            timestamp = log_entry["timestamp"]
            message = log_entry["message"]
            level = log_entry["level"]

            # Definir cor baseada no nível
            color = self._get_color_for_level(level)
            icon = self._get_icon_for_level(level)

            html += f"""
            <div style="margin-bottom: 5px; padding: 3px; border-left: 3px solid {color};">
                <span style="color: {color}; font-weight: bold;">{icon} {timestamp}</span>
                <span style="margin-left: 10px;">{message}</span>
            </div>
            """

        html += "</div>"
        return html

    def _get_color_for_level(self, level: str) -> str:
        """Retorna cor baseada no nível do log"""
        colors = {"ERROR": "#dc3545", "WARNING": "#ffc107", "INFO": "#007bff", "DEBUG": "#6c757d"}
        return colors.get(level, "#6c757d")

    def _get_icon_for_level(self, level: str) -> str:
        """Retorna ícone baseado no nível do log"""
        icons = {"ERROR": "🔴", "WARNING": "🟡", "INFO": "🔵", "DEBUG": "⚪"}
        return icons.get(level, "⚪")

    def display_summary_stats(self):
        """Exibe estatísticas resumidas dos logs"""
        logs = self.displayed_logs

        if not logs:
            return

        # Contar por nível
        level_counts = {}
        for log in logs:
            level = log["level"]
            level_counts[level] = level_counts.get(level, 0) + 1

        # Criar métricas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total de Logs", len(logs))

        with col2:
            st.metric("Erros", level_counts.get("ERROR", 0))

        with col3:
            st.metric("Avisos", level_counts.get("WARNING", 0))

        with col4:
            st.metric("Informações", level_counts.get("INFO", 0))

    def clear_logs(self):
        """Limpa os logs exibidos"""
        log_manager.clear_logs()
        self.displayed_logs = []
        self._update_display()

    def export_logs_to_text(self) -> str:
        """Exporta logs para texto"""
        if not self.displayed_logs:
            return "Nenhum log disponível para exportar."

        text_content = "=== LOGS DE EXECUÇÃO ===\n\n"

        for log_entry in self.displayed_logs:
            timestamp = log_entry["timestamp"]
            level = log_entry["level"]
            message = log_entry["message"]

            text_content += f"[{timestamp}] {level}: {message}\n"

        return text_content


def create_log_viewer_component(title: str = "📊 Logs de Execução", height: int = 400):
    """Cria um componente completo de visualização de logs"""

    st.markdown(f"### {title}")

    # Controles
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        auto_refresh = st.checkbox("🔄 Atualização Automática", value=True)

    with col2:
        max_logs = st.selectbox("Max Logs", [20, 50, 100], index=1)

    with col3:
        if st.button("🗑️ Limpar Logs"):
            log_manager.clear_logs()
            st.rerun()

    # Container para logs
    logs_container = st.container()

    # Criar instância do logger
    logger = StreamlitLogger(logs_container)

    # Exibir estatísticas
    logger.display_summary_stats()

    # Exibir logs
    logger.display_logs_realtime(max_logs)

    # Auto-refresh se habilitado
    if auto_refresh:
        time.sleep(1)
        st.rerun()

    # Botão de exportação
    if st.button("📥 Exportar Logs"):
        log_text = logger.export_logs_to_text()
        st.download_button(
            label="💾 Baixar Logs",
            data=log_text,
            file_name=f"logs_execucao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

    return logger
