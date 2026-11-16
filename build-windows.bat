@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Flipmelon v1.0.8.9-diagnostico - Compilacao para desenvolvedores
if not exist "vendor\windows\scrcpy.exe" goto missing
if not exist "vendor\windows\adb.exe" goto missing
where py >nul 2>nul
if errorlevel 1 (
  echo ERRO: Python nao encontrado. Instale Python 3.11 ou superior nesta maquina de desenvolvimento.
  goto fail
)
echo.
echo [1/6] Instalando ferramentas de compilacao...
py -m pip install --disable-pip-version-check --only-binary=:all: PySide6 pyinstaller rlottie-python
if errorlevel 1 goto fail
echo [2/6] Gerando Flipmelon.exe sem janela de terminal...
py -m PyInstaller --noconfirm --clean --onedir --windowed --name Flipmelon --icon "flipmelon.ico" --add-data "vendor;vendor" --add-data "assets;assets" --add-data "locales;locales" --add-data "flipmelon.ico;." --exclude-module PySide6.QtWebEngineWidgets --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtWebEngineQuick --collect-all rlottie_python --hidden-import rlottie_python --hidden-import lottie_window Flipmelon.py
if errorlevel 1 goto fail
if not exist "dist\Flipmelon\Flipmelon.exe" goto fail
echo [3/6] Criando pacote PORTATIL (nao usa o motor temporario do Inno Setup)...
if not exist "output" mkdir "output"
if exist "output\Flipmelon_v1.0.8.9_Portable_Windows.zip" del /q "output\Flipmelon_v1.0.8.9_Portable_Windows.zip"
powershell -NoProfile -Command "Compress-Archive -Path 'dist\Flipmelon' -DestinationPath 'output\Flipmelon_v1.0.8.9_Portable_Windows.zip' -CompressionLevel Optimal -Force"
if errorlevel 1 goto fail
if not exist "output\Flipmelon_v1.0.8.9_Portable_Windows.zip" goto fail
echo [4/6] Procurando Inno Setup 6...
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC (
  for /f "delims=" %%i in ('where ISCC.exe 2^>nul') do if not defined ISCC set "ISCC=%%i"
)
if not defined ISCC (
  echo INFO: Inno Setup 6 nao encontrado. O ZIP portatil foi criado.
  goto done
)
echo [5/6] Gerando instalador MULTIARQUIVO sem carregador temporario...
"%ISCC%" "Flipmelon.iss"
if errorlevel 1 (
  echo AVISO: Inno Setup falhou; mantenha o ZIP portatil.
  goto done
)
if not exist "output\Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED.exe" goto done
echo.
echo ===============================================================
echo SUCESSO: output\Flipmelon_Setup_v1.0.8.9_NoTemp_UNSIGNED.exe
echo ATENCAO: mantenha os arquivos .exe E .bin NA MESMA PASTA.
echo Continua NAO ASSINADO; o Windows ainda pode bloquear o aplicativo.
echo ===============================================================
:done
echo.
echo PACOTE PORTATIL: output\Flipmelon_v1.0.8.9_Portable_Windows.zip
echo Alternativa de teste: abra o Setup.exe mantendo todos os .bin juntos.
echo Se houver bloqueio, use o portatil apenas se o Windows permitir.
echo Nao desative a protecao do Windows para testar.
explorer "output"
pause
exit /b 0
:missing
echo ERRO: vendor\windows\scrcpy.exe ou adb.exe nao foram encontrados.
:fail
echo.
echo FALHA: o instalador NAO foi gerado.
echo Copie o erro acima. Nao distribua o executavel sem verificar.
pause
exit /b 1
