# DHL Order Processing System v3.0 - PowerShell Launcher
# Created by Lucas Gnemmi

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "   DHL Order Processing System v3.0" -ForegroundColor Yellow
Write-Host "   Created by Lucas Gnemmi" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Usar Python empaquetado (tiene todas las librerías incluidas)
$PYTHON_HOME = Join-Path $PSScriptRoot "python\python"
$PYTHON_EXE = Join-Path $PYTHON_HOME "python.exe"

if (Test-Path $PYTHON_EXE) {
    Write-Host "Usando Python empaquetado:" -ForegroundColor Green
    & $PYTHON_EXE --version
    Write-Host ""
    Write-Host "Starting application..." -ForegroundColor Green
    Write-Host ""
    
    & $PYTHON_EXE gui_moderna_v2.py
    
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    [Console]::ReadKey()
    exit 0
}

# Fallback: intentar Python del sistema (menos probable que funcione)
try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    Write-Host "FALLBACK - Usando Python del sistema:" -ForegroundColor Yellow
    & python --version
    Write-Host ""
    Write-Host "Starting application..." -ForegroundColor Green
    Write-Host ""
    
    & python gui_moderna_v2.py
    
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    [Console]::ReadKey()
    exit 0
} catch {
    # No hay Python disponible
    Write-Host "ERROR: No se encuentra Python" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor instala Python desde:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    [Console]::ReadKey()
    exit 1
}
