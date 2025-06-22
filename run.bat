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

REM Verificar se o arquivo .env existe
if not exist ".env" (
    echo Aviso: Arquivo .env nao encontrado!
    echo Copiando template...
    copy env_template.txt .env
    echo.
    echo IMPORTANTE: Configure suas chaves de API no arquivo .env
    echo.
)

REM Executar a aplicação
echo Iniciando aplicacao Streamlit...
echo.
echo A aplicacao sera aberta em: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar a aplicacao
echo.
set PYTHONPATH=%CD%;%PYTHONPATH%
streamlit run app/main.py

pause 