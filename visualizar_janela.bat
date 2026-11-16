@echo off
cd /d "%~dp0"
py -c "import PySide6" >nul 2>nul || (echo Instale as dependencias executando build-windows.bat primeiro. & pause & exit /b 1)
py visualizar_janela.py
if errorlevel 1 pause
