@echo off
echo ========================================
echo    APP_AGENTES - Sistema de Agentes
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo Erro: Ambiente virtual nao encontrado!
    echo Execute: python setup.py
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Executar a aplicação usando o script Python
echo Iniciando aplicacao Streamlit...
python run_app.py

pause 