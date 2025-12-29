@echo off
REM ============================================
REM Preparar Release para GitHub - DHL System
REM ============================================

powershell.exe -ExecutionPolicy Bypass -File "%~dp0Preparar_Release.ps1"
pause
