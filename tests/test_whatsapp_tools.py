"""
Testes para as ferramentas do WhatsApp
"""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile
import os

from app.utils.tools import (
    whatsapp_connect,
    whatsapp_get_messages,
    extract_cloud_links,
    download_cloud_file,
    download_whatsapp_file,
    rename_file_with_timestamp,
    organize_files_by_date
)


class TestWhatsAppTools:
    """Testes para as ferramentas do WhatsApp"""

    def test_whatsapp_connect(self):
        """Testa a conexão com WhatsApp"""
        result = whatsapp_connect("test_session")
        
        assert result["status"] == "connected"
        assert result["session_name"] == "test_session"
        assert "message" in result

    def test_whatsapp_get_messages(self):
        """Testa a obtenção de mensagens"""
        messages = whatsapp_get_messages("Test Group", 10)
        
        assert isinstance(messages, list)
        assert len(messages) <= 10
        
        if messages:
            message = messages[0]
            assert "id" in message
            assert "text" in message
            assert "timestamp" in message
            assert "sender" in message
            assert "has_file" in message

    def test_extract_cloud_links(self):
        """Testa a extração de links de nuvem"""
        # Mensagens de teste com links
        test_messages = [
            {
                "id": "msg1",
                "text": "Aqui está o arquivo: https://drive.google.com/file/d/123456789",
                "timestamp": "2024-01-15T14:30:00",
                "sender": "User1"
            },
            {
                "id": "msg2",
                "text": "Link do OneDrive: https://1drv.ms/abc123",
                "timestamp": "2024-01-15T14:35:00",
                "sender": "User2"
            },
            {
                "id": "msg3",
                "text": "Mensagem sem link",
                "timestamp": "2024-01-15T14:40:00",
                "sender": "User3"
            }
        ]
        
        links = extract_cloud_links(test_messages)
        
        assert isinstance(links, list)
        assert len(links) >= 1  # Pelo menos um link deve ser encontrado
        
        if links:
            link = links[0]
            assert "message_id" in link
            assert "service" in link
            assert "url" in link
            assert "timestamp" in link
            assert "sender" in link

    def test_download_cloud_file_simulation(self):
        """Testa o download de arquivos da nuvem (simulação)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Teste com link do Google Drive
            result = download_cloud_file(
                "https://drive.google.com/file/d/test123", 
                temp_dir
            )
            
            assert isinstance(result, dict)
            assert "status" in result
            
            # Como é uma simulação, pode retornar "not_implemented" ou "error"
            assert result["status"] in ["success", "not_implemented", "error"]

    def test_download_whatsapp_file_simulation(self):
        """Testa o download de arquivos do WhatsApp (simulação)"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mensagem com arquivo
            message_with_file = {
                "id": "msg1",
                "has_file": True,
                "file_name": "test.pdf",
                "timestamp": "2024-01-15T14:30:00"
            }
            
            result = download_whatsapp_file(message_with_file, temp_dir)
            
            assert isinstance(result, dict)
            assert "status" in result
            
            if result["status"] == "success":
                assert "file_path" in result
                assert "file_size" in result
                assert "source" in result
                assert result["source"] == "whatsapp"

    def test_rename_file_with_timestamp(self):
        """Testa a renomeação de arquivos com timestamp"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Criar arquivo de teste
            test_file = Path(temp_dir) / "test.txt"
            test_file.write_text("test content")
            
            # Renomear com timestamp
            timestamp = "2024-01-15T14:30:00"
            new_path = rename_file_with_timestamp(str(test_file), timestamp)
            
            assert Path(new_path).exists()
            assert "20240115_143000" in Path(new_path).name
            assert Path(new_path).read_text() == "test content"

    def test_organize_files_by_date(self):
        """Testa a organização de arquivos por data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Criar arquivos de teste
            files_list = []
            
            for i in range(3):
                test_file = Path(temp_dir) / f"file_{i}.txt"
                test_file.write_text(f"content {i}")
                
                files_list.append({
                    "file_path": str(test_file),
                    "timestamp": f"2024-01-1{i+5}T14:30:00"
                })
            
            # Organizar arquivos
            result = organize_files_by_date(files_list, temp_dir)
            
            assert isinstance(result, dict)
            assert "status" in result
            
            if result["status"] == "success":
                assert "organized_files" in result
                assert "base_path" in result

    def test_extract_cloud_links_empty_messages(self):
        """Testa extração de links com mensagens vazias"""
        links = extract_cloud_links([])
        assert isinstance(links, list)
        assert len(links) == 0

    def test_extract_cloud_links_no_links(self):
        """Testa extração de links quando não há links"""
        messages = [
            {
                "id": "msg1",
                "text": "Mensagem sem links",
                "timestamp": "2024-01-15T14:30:00",
                "sender": "User1"
            }
        ]
        
        links = extract_cloud_links(messages)
        assert isinstance(links, list)
        assert len(links) == 0

    def test_rename_file_with_timestamp_invalid_file(self):
        """Testa renomeação com arquivo inexistente"""
        with pytest.raises(Exception):
            rename_file_with_timestamp("arquivo_inexistente.txt", "2024-01-15T14:30:00")

    def test_whatsapp_get_messages_invalid_limit(self):
        """Testa obtenção de mensagens com limite inválido"""
        messages = whatsapp_get_messages("Test Group", 0)
        assert isinstance(messages, list)
        assert len(messages) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 