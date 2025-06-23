#!/usr/bin/env python3
import os, sys, subprocess, shutil

def check_python_version():
    if sys.version_info < (3, 10) or sys.version_info > (3, 13, 2):
        print("❌ É necessário Python >=3.10 e <=3.13.2")
        print("Versão atual:", sys.version)
        return False
    print("✅ Python", sys.version.split()[0], "detectado")
    return True

def create_venv():
    if os.path.exists("venv"):
        print("✅ venv já existe")
        return True
    try:
        subprocess.run([sys.executable, "-m", "venv", "--upgrade-deps", "venv"], check=True)
        print("✅ venv criado com dependências principais atualizadas")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ falha ao criar venv:", e)
        return False

def install_deps():
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        pip_cmd = os.path.join("venv", "Scripts" if os.name=='nt' else "bin", "pip")
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ dependências instaladas")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ erro na instalação:", e)
        return False

def create_env():
    if os.path.exists(".env"):
        print("✅ .env já existe"); return True
    if os.path.exists("env_template.txt"):
        shutil.copy("env_template.txt", ".env")
        print("✅ .env criado a partir do template; preencha-o.")
        return True
    print("❌ env_template.txt não encontrado")
    return False

def main():
    print("🚀 Setup APP_AGENTES")
    if not check_python_version(): return False
    if not create_venv(): return False
    if not install_deps(): return False
    if not create_env(): return False
    print("✅ Setup completo! Ative o venv e rode sua aplicação.")
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
