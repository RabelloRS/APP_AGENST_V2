#!/usr/bin/env python3
"""
Script para executar a aplicação APP_AGENTES
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Função principal para executar a aplicação"""
    
    # Obter o diretório raiz do projeto
    project_root = Path(__file__).resolve().parent
    
    # Adicionar o diretório raiz ao Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Verificar se o ambiente virtual existe
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("❌ Ambiente virtual não encontrado!")
        print("Execute: python setup.py")
        return False
    
    # Verificar se o arquivo .env existe
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️ Arquivo .env não encontrado!")
        print("Copiando template...")
        template_file = project_root / "env_template.txt"
        if template_file.exists():
            import shutil
            shutil.copy(template_file, env_file)
            print("✅ Arquivo .env criado a partir do template")
            print("⚠️ Lembre-se de configurar suas chaves de API no arquivo .env")
        else:
            print("❌ Template env_template.txt não encontrado")
            return False
    
    # Determinar o comando streamlit correto
    if os.name == 'nt':  # Windows
        streamlit_cmd = venv_path / "Scripts" / "streamlit.exe"
    else:  # Unix/Linux/Mac
        streamlit_cmd = venv_path / "bin" / "streamlit"
    
    if not streamlit_cmd.exists():
        print("❌ Streamlit não encontrado no ambiente virtual!")
        print("Execute: python setup.py")
        return False
    
    # Configurar variáveis de ambiente
    env = os.environ.copy()
    env['PYTHONPATH'] = f"{project_root}{os.pathsep}{env.get('PYTHONPATH', '')}"
    
    # Executar a aplicação
    print("🚀 Iniciando aplicação Streamlit...")
    print(f"📁 Diretório do projeto: {project_root}")
    print("🌐 A aplicação será aberta em: http://localhost:8501")
    print("⏹️ Pressione Ctrl+C para parar a aplicação")
    print()
    
    try:
        subprocess.run([
            str(streamlit_cmd), 
            "run", 
            str(project_root / "app" / "main.py")
        ], env=env, cwd=project_root)
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar a aplicação: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 