@echo off
REM ====================================================================
REM Actualización Simple - DHL Procesar Pedidos
REM NO REQUIERE GIT - Descarga directamente desde GitHub
REM ====================================================================

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\Actualizar_Directo.ps1"
pause
