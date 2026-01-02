@echo off
REM ====================================================================
REM Actualización Automática - DHL Procesar Pedidos
REM NO REQUIERE GIT - Descarga directamente desde GitHub
REM ====================================================================

cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\Actualizar_Directo.ps1" -Automatico
exit
