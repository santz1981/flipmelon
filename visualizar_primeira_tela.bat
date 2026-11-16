@echo off
setlocal
cd /d "%~dp0"
if exist "dist\Flipmelon\Flipmelon.exe" (
    start "" "dist\Flipmelon\Flipmelon.exe" --setup
    exit /b 0
)
where py >nul 2>nul
if errorlevel 1 (
    echo Python nao encontrado. Primeiro execute build-windows.bat.
    pause
    exit /b 1
)
py "Flipmelon.py" --setup
if errorlevel 1 pause
