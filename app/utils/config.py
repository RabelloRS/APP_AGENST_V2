"""
Módulo de configuração do sistema
"""

import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    """Classe para gerenciar configurações do sistema"""

    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(dotenv_path=env_path)

        # API Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        # Model Configuration
        self.default_model = os.getenv("DEFAULT_MODEL", "gpt-4")
        self.default_temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))

        # Application Configuration
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Streamlit Configuration
        self.streamlit_port = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
        self.streamlit_address = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")

    def is_api_configured(self) -> bool:
        """Verifica se as APIs estão configuradas"""
        return bool(
            self.openai_api_key and self.openai_api_key != "your_openai_api_key_here"
        )

    def get_openai_config(self) -> dict:
        """Retorna configuração para OpenAI"""
        return {
            "api_key": self.openai_api_key,
            "model": self.default_model,
            "temperature": self.default_temperature,
        }

    def validate_config(self) -> list:
        """Valida a configuração e retorna lista de erros"""
        errors = []

        if not self.is_api_configured():
            errors.append("Chave da API OpenAI não configurada")

        if not self.openai_api_key:
            errors.append("OPENAI_API_KEY não encontrada no arquivo .env")

        return errors
