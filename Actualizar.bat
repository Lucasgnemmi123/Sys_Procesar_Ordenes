@echo off
REM ====================================================================
REM Launcher para Sistema de Actualización - DHL Procesar Pedidos
REM ====================================================================

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0Actualizar_Sistema.ps1"
pause
