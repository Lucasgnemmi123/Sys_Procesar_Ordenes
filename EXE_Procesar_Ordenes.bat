@echo off
REM ========================================
REM   Sistema de Procesamiento de Pedidos
REM   DHL v3.0 - Launcher Híbrido
REM ========================================

title DHL - Procesar Pedidos

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Intentar usar Python del sistema primero (tiene tkinter)
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Usando Python del sistema:
    python --version
    echo.
    echo Iniciando launcher...
    python launcher.py
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo ejecutar el launcher
        pause
    )
    exit /b 0
)

REM Si no hay Python del sistema, intentar usar Python empaquetado
set PYTHON_HOME=%~dp0python
set PYTHON_EXE=%PYTHON_HOME%\python.exe

if exist "%PYTHON_EXE%" (
    echo Usando Python empaquetado:
    "%PYTHON_EXE%" --version
    echo.
    echo Iniciando launcher...
    "%PYTHON_EXE%" launcher.py
    if errorlevel 1 (
        echo.
        echo ERROR: No se pudo ejecutar el launcher
        echo.
        echo Si ves un error de tkinter, necesitas Python del sistema.
        echo Descarga desde: https://www.python.org/downloads/
        echo.
        pause
    )
    exit /b 0
)

REM Si no hay ningún Python disponible
echo.
echo ERROR: No se encuentra Python en el sistema
echo.
echo Por favor instala Python desde:
echo https://www.python.org/downloads/
echo.
echo O coloca Python empaquetado en la carpeta 'python'
echo.
pause
exit /b 1
