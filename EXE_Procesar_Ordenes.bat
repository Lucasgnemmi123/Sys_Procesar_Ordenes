@echo off
REM ========================================
REM   Sistema de Procesamiento de Pedidos
REM   Created by Lucas Gnemmi
REM ========================================

title Sistema de Procesamiento de Pedidos DHL

echo.
echo ===================================
echo  🚚 SISTEMA DE PROCESAMIENTO DE PEDIDOS
echo ===================================
echo.
echo Iniciando aplicacion...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar el ejecutable (si existe) o Python como fallback
if exist "DHL_Procesamiento_Pedidos.exe" (
    echo 📦 Ejecutando version empaquetada...
    start "" "DHL_Procesamiento_Pedidos.exe"
    echo.
    echo ✅ Aplicacion iniciada correctamente
    echo.
) else if exist "gui_moderna_v2.py" (
    echo 🐍 Ejecutando version Python...
    python gui_moderna_v2.py
    
    if errorlevel 1 (
        echo.
        echo ❌ ERROR: No se pudo ejecutar la aplicacion
        echo.
        echo Posibles causas:
        echo - Python no esta instalado
        echo - El archivo gui_moderna_v2.py no existe
        echo - Faltan dependencias de Python
        echo.
        pause
        exit /b 1
    )
    
    echo.
    echo ✅ Aplicacion finalizada correctamente
    echo.
) else (
    echo.
    echo ❌ ERROR: No se encontro ni el ejecutable ni el archivo Python
    echo.
    echo Por favor verifica que el archivo este en la carpeta:
    echo - DHL_Procesamiento_Pedidos.exe (version empaquetada)
    echo - gui_moderna_v2.py (version Python)
    echo.
    pause
    exit /b 1
)

pause