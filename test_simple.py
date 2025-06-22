import streamlit as st

st.title("Teste Simples")
st.write("Se você está vendo esta mensagem, o Streamlit está funcionando!")

# Testar imports do projeto
try:
    from app.agents.agent_manager import AgentManager
    st.success("✅ AgentManager importado com sucesso")
except Exception as e:
    st.error(f"❌ Erro ao importar AgentManager: {e}")

try:
    from app.crews.crew_manager import CrewManager
    st.success("✅ CrewManager importado com sucesso")
except Exception as e:
    st.error(f"❌ Erro ao importar CrewManager: {e}")

try:
    from app.utils.config import Config
    st.success("✅ Config importado com sucesso")
except Exception as e:
    st.error(f"❌ Erro ao importar Config: {e}")

st.write("Teste concluído!") 