"""
Testes úteis para o AgentManager (apenas lógica relevante e atual)
"""


from app.agents.agent_manager import AgentManager


class TestAgentManager:
    """Testes para a classe AgentManager (apenas lógica útil)"""

    def setup_method(self):
        self.agent_manager = AgentManager()

    def test_agent_manager_initialization(self):
        assert self.agent_manager is not None
        assert isinstance(self.agent_manager.agents, dict)
        assert isinstance(self.agent_manager.available_agents, dict)

    def test_list_available_agent_types(self):
        agent_types = self.agent_manager.list_available_agent_types()
        assert isinstance(agent_types, list)
        assert len(agent_types) > 0
        # Verifica se há agentes técnicos ou engenheiros
        assert any("technical" in agent_type for agent_type in agent_types) or any("engineer" in agent_type for agent_type in agent_types)

    def test_get_agent_info(self):
        agent_types = self.agent_manager.list_available_agent_types()
        if agent_types:
            first_agent = agent_types[0]
            info = self.agent_manager.get_agent_info(first_agent)
            assert info is not None
            assert "name" in info
            assert "role" in info
            assert "goal" in info
            assert "backstory" in info

    def test_get_agent_info_invalid(self):
        info = self.agent_manager.get_agent_info("invalid_agent")
        assert info is None

    def test_agent_configs_structure(self):
        configs = self.agent_manager.get_agent_configs()
        assert isinstance(configs, dict)
        for agent_type, config in configs.items():
            assert isinstance(agent_type, str)
            assert isinstance(config, dict)
            assert "name" in config
            assert "role" in config
            assert "goal" in config
            assert "backstory" in config

    def test_agent_tools_configuration(self):
        agent_types = self.agent_manager.list_available_agent_types()
        if agent_types:
            first_agent = agent_types[0]
            tools = self.agent_manager.get_agent_tools(first_agent)
            assert isinstance(tools, list)
