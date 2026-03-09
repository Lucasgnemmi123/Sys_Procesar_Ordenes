@echo off
:: ========================================
:: Sistema de Procesamiento de Pedidos DHL
:: Iniciador Directo (sin VBS)
:: ========================================

cd /d "%~dp0"

:: Usar Python embebido (prioridad 1)
if exist "%~dp0\python\python\pythonw.exe" (
    start "" "%~dp0\python\python\pythonw.exe" "%~dp0\gui_moderna_v2.py"
    exit /b 0
)

if exist "%~dp0\python\python\python.exe" (
    start "" "%~dp0\python\python\python.exe" "%~dp0\gui_moderna_v2.py"
    exit /b 0
)

:: Fallback: Python del sistema
pythonw.exe "%~dp0\gui_moderna_v2.py" 2>nul
if errorlevel 1 (
    python.exe "%~dp0\gui_moderna_v2.py"
)