@echo off
REM ========================================
REM   Sistema de Procesamiento de Pedidos
REM   Created by Lucas Gnemmi
REM ========================================

title Sistema de Procesamiento de Pedidos

echo.
echo ===================================
echo  🚚 SISTEMA DE PROCESAMIENTO DE PEDIDOS
echo ===================================
echo.
echo Iniciando aplicacion...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar la aplicacion Python
python gui_moderna_v2.py

REM Si hay error, mostrar mensaje y pausar
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

REM Mensaje de finalizacion
echo.
echo ✅ Aplicacion finalizada correctamente
echo.
pause