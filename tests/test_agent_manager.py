"""
Testes para o AgentManager
"""


from app.agents.agent_manager import AgentManager


class TestAgentManager:
    """Testes para a classe AgentManager"""

    def setup_method(self):
        """Setup para cada teste"""
        self.agent_manager = AgentManager()

    def test_agent_manager_initialization(self):
        """Testa a inicialização do AgentManager"""
        assert self.agent_manager is not None
        assert isinstance(self.agent_manager.agents, dict)
        assert isinstance(self.agent_manager.available_agents, dict)

    def test_list_available_agent_types(self):
        """Testa a listagem de tipos de agentes disponíveis"""
        agent_types = self.agent_manager.list_available_agent_types()
        assert isinstance(agent_types, list)
        assert len(agent_types) > 0
        assert "researcher" in agent_types
        assert "analyst" in agent_types

    def test_get_agent_info(self):
        """Testa a obtenção de informações de agentes"""
        info = self.agent_manager.get_agent_info("researcher")
        assert info is not None
        assert "name" in info
        assert "role" in info
        assert "goal" in info
        assert "backstory" in info

    def test_get_agent_info_invalid(self):
        """Testa a obtenção de informações de agente inválido"""
        info = self.agent_manager.get_agent_info("invalid_agent")
        assert info is None
