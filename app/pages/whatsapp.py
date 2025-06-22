"""
Página de Integração com WhatsApp - Download de Arquivos
"""

import streamlit as st
from datetime import datetime
import pandas as pd
import os
import time

# Função auxiliar para simular o download
def simulate_download(file_name, duration=3):
    progress_text = f"Baixando '{file_name}'... Por favor, aguarde."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(duration / 100)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.empty()

def show_whatsapp_tab():
    """Exibe a aba de integração com WhatsApp."""
    st.header("📱 Integração com WhatsApp")
    st.markdown("### Baixe arquivos diretamente de conversas do WhatsApp")

    # Inicializar estado
    if "whatsapp_downloads" not in st.session_state:
        st.session_state.whatsapp_downloads = []
    if "whatsapp_connected" not in st.session_state:
        st.session_state.whatsapp_connected = False

    tools_manager = st.session_state.tools_manager
    download_tool = tools_manager.get_tool_info("whatsapp_download_tool")

    # Status da Conexão
    st.subheader("📶 Status da Conexão")
    status_placeholder = st.empty()

    def update_status():
        if st.session_state.whatsapp_connected:
            status_placeholder.success("✅ Conectado ao WhatsApp")
        else:
            status_placeholder.warning("🔌 Desconectado. Clique no botão abaixo para conectar.")

    update_status()

    # Controle de Conexão
    if not st.session_state.whatsapp_connected:
        if st.button("🔗 Conectar ao WhatsApp", type="primary"):
            with st.spinner("Iniciando conexão... Por favor, escaneie o QR Code no terminal, se solicitado."):
                # Simulação de conexão
                time.sleep(3) 
                st.session_state.whatsapp_connected = True
                st.rerun()
    else:
        if st.button("🔌 Desconectar", type="secondary"):
            st.session_state.whatsapp_connected = False
            st.rerun()

    st.markdown("---")

    # Seção de Download
    st.subheader("📥 Baixar Arquivo")
    if not st.session_state.whatsapp_connected:
        st.info("Você precisa estar conectado para baixar arquivos.")
    else:
        with st.form("download_form", clear_on_submit=True):
            contact_name = st.text_input(
                "Nome do Contato ou Grupo",
                placeholder="Ex: João Silva ou Grupo Família",
                help="Nome exato do contato ou grupo de onde o arquivo será baixado."
            )
            file_name = st.text_input(
                "Nome do Arquivo",
                placeholder="Ex: relatorio_vendas.xlsx",
                help="Nome do arquivo a ser baixado (incluindo extensão)."
            )
            
            submitted = st.form_submit_button("⬇️ Baixar Arquivo")

            if submitted:
                if not contact_name or not file_name:
                    st.error("Por favor, preencha o nome do contato e do arquivo.")
                else:
                    try:
                        # Simula o download e a criação da pasta 'workspace'
                        simulate_download(file_name)
                        workspace_dir = "workspace"
                        if not os.path.exists(workspace_dir):
                            os.makedirs(workspace_dir)
                        
                        # Simula a criação do arquivo
                        file_path = os.path.join(workspace_dir, file_name)
                        with open(file_path, "w") as f:
                            f.write("Este é um arquivo de teste baixado do WhatsApp.")

                        st.success(f"Arquivo '{file_name}' baixado com sucesso para a pasta `{workspace_dir}`!")
                        
                        st.session_state.whatsapp_downloads.append({
                            "Contato": contact_name,
                            "Arquivo": file_name,
                            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Status": "Sucesso"
                        })

                    except Exception as e:
                        st.error(f"Falha no download: {e}")
                        st.session_state.whatsapp_downloads.append({
                            "Contato": contact_name,
                            "Arquivo": file_name,
                            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Status": f"Falha ({e})"
                        })

    st.markdown("---")
    
    # Histórico de Downloads
    st.subheader("📜 Histórico de Downloads da Sessão")
    if not st.session_state.whatsapp_downloads:
        st.info("Nenhum download realizado nesta sessão.")
    else:
        history_df = pd.DataFrame(st.session_state.whatsapp_downloads).sort_index(ascending=False)
        st.dataframe(history_df, use_container_width=True, hide_index=True) 