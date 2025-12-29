# ====================================================================
# VERIFICADOR RAPIDO DE ACTUALIZACIONES - DHL Procesar Pedidos
# ====================================================================
# Script rapido para verificar si hay actualizaciones disponibles
# ====================================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host ""
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "   DHL - Verificador de Actualizaciones" -ForegroundColor Yellow
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Git
$gitCheck = git --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [X] Git no esta instalado" -ForegroundColor Red
    Write-Host "  Instala Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Verificar repositorio
if (-not (Test-Path ".git")) {
    Write-Host "  [X] No es un repositorio Git valido" -ForegroundColor Red
    exit 1
}

Write-Host "  Consultando GitHub..." -ForegroundColor Gray
$fetchResult = git fetch origin main 2>&1
$localCommit = git rev-parse HEAD 2>&1
$remoteCommit = git rev-parse origin/main 2>&1

Write-Host ""

if ($localCommit -eq $remoteCommit) {
    # Sistema actualizado
    Write-Host "  [OK] SISTEMA ACTUALIZADO [OK]" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Version: $($localCommit.Substring(0,7))" -ForegroundColor Gray
    Write-Host "  Estado: Al dia con GitHub" -ForegroundColor Gray
    Write-Host ""
    exit 0
} else {
    # Hay actualizacion disponible
    Write-Host "  [!] ACTUALIZACION DISPONIBLE [!]" -ForegroundColor Yellow
    Write-Host ""
    
    # Contar archivos modificados
    $filesChanged = git diff --name-status HEAD origin/main 2>&1
    $changeLines = $filesChanged -split "`n" | Where-Object { $_ -match '^\w\s+' }
    $changeCount = $changeLines.Count
    
    Write-Host "  Archivos con cambios: $changeCount" -ForegroundColor Cyan
    Write-Host "  Version local: $($localCommit.Substring(0,7))" -ForegroundColor Gray
    Write-Host "  Version remota: $($remoteCommit.Substring(0,7))" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Para actualizar, ejecuta:" -ForegroundColor Yellow
    Write-Host "    - Actualizar.bat" -ForegroundColor Cyan
    Write-Host "    - o usa la opcion del Launcher" -ForegroundColor Cyan
    Write-Host ""
    exit 2
}
