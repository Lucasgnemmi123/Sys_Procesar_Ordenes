# ====================================================================
# ACTUALIZADOR SIMPLE - DHL Procesar Pedidos  
# ====================================================================
# Descarga la última versión desde GitHub (repositorio público)
# NO requiere Git instalado
# ====================================================================

param(
    [switch]$SoloVerificar,
    [switch]$Automatico
)

$ErrorActionPreference = "Continue"
$scriptDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $scriptDir

# Configuración
$GITHUB_REPO = "Lucasgnemmi123/Sys_Procesar_Ordenes"
$GITHUB_BRANCH = "main"
$ZIP_URL = "https://github.com/$GITHUB_REPO/archive/refs/heads/$GITHUB_BRANCH.zip"

# Habilitar TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Write-Host ""
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "   DHL - Actualización desde GitHub" -ForegroundColor Yellow
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Repositorio: $GITHUB_REPO" -ForegroundColor Gray
Write-Host "  Rama: $GITHUB_BRANCH" -ForegroundColor Gray
Write-Host ""

# Verificar conexión
Write-Host "  [1/7] Verificando conexion..." -ForegroundColor Cyan
try {
    $testConnection = Test-Connection github.com -Count 2 -Quiet -ErrorAction Stop
    if (-not $testConnection) {
        throw "No hay conexion"
    }
    Write-Host "  [OK] Conexion OK" -ForegroundColor Green
}
catch {
    Write-Host "  [X] No hay conexion a Internet" -ForegroundColor Red
    Write-Host ""
    if (-not $Automatico) {
        Read-Host "Presiona Enter para salir"
    }
    exit 1
}

# Verificar repositorio
Write-Host "  [2/7] Verificando repositorio..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $ZIP_URL -Method Head -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
    $sizeInMB = [math]::Round($response.Headers.'Content-Length'/1MB, 2)
    Write-Host "  [OK] Repositorio accesible ($sizeInMB MB)" -ForegroundColor Green
}
catch {
    Write-Host "  [X] No se puede acceder al repositorio" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
    if (-not $Automatico) {
        Read-Host "Presiona Enter para salir"
    }
    exit 1
}

if ($SoloVerificar) {
    Write-Host ""
    Write-Host "  [OK] Verificacion completada - Listo para actualizar" -ForegroundColor Green
    Write-Host ""
    if (-not $Automatico) {
        Read-Host "Presiona Enter para salir"
    }
    exit 0
}

# Crear carpeta temporal
Write-Host "  [3/7] Preparando..." -ForegroundColor Cyan
$tempDir = Join-Path $env:TEMP "DHL_Update_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
Write-Host "  [OK] Carpeta temporal creada" -ForegroundColor Green

# Descargar ZIP
Write-Host "  [4/7] Descargando desde GitHub..." -ForegroundColor Cyan
$zipFile = Join-Path $tempDir "repo.zip"
try {
    Invoke-WebRequest -Uri $ZIP_URL -OutFile $zipFile -UseBasicParsing -TimeoutSec 300 -ErrorAction Stop
    $zipSizeMB = [math]::Round((Get-Item $zipFile).Length / 1MB, 2)
    Write-Host "  [OK] Descarga completada ($zipSizeMB MB)" -ForegroundColor Green
}
catch {
    Write-Host "  [X] Error al descargar: $($_.Exception.Message)" -ForegroundColor Red
    Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ""
    if (-not $Automatico) {
        Read-Host "Presiona Enter para salir"
    }
    exit 1
}

# Extraer ZIP
Write-Host "  [5/7] Extrayendo archivos..." -ForegroundColor Cyan
$extractDir = Join-Path $tempDir "extracted"
try {
    Expand-Archive -Path $zipFile -DestinationPath $extractDir -Force -ErrorAction Stop
    Write-Host "  [OK] Archivos extraidos" -ForegroundColor Green
}
catch {
    Write-Host "  [X] Error al extraer: $($_.Exception.Message)" -ForegroundColor Red
    Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ""
    if (-not $Automatico) {
        Read-Host "Presiona Enter para salir"
    }
    exit 1
}

# Encontrar carpeta del repositorio
$repoFolderName = "Sys_Procesar_Ordenes-$GITHUB_BRANCH"
$repoFolder = Join-Path $extractDir $repoFolderName

if (-not (Test-Path $repoFolder)) {
    Write-Host "  [X] No se encontro la carpeta del repositorio" -ForegroundColor Red
    Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host ""
    if (-not $Automatico) {
        Read-Host "Presiona Enter para salir"
    }
    exit 1
}

# Backup de configuraciones
Write-Host "  [6/7] Respaldando configuraciones..." -ForegroundColor Cyan
$backupFiles = @("agenda_config.json", "rules.json", "products.json")
$backupDir = Join-Path $tempDir "backup_config"
New-Item -ItemType Directory -Path $backupDir -Force | Out-Null

$backedUpCount = 0
foreach ($file in $backupFiles) {
    $filePath = Join-Path $scriptDir $file
    if (Test-Path $filePath) {
        Copy-Item $filePath (Join-Path $backupDir $file) -Force
        $backedUpCount++
    }
}
Write-Host "  [OK] $backedUpCount configuracion(es) respaldadas" -ForegroundColor Green

# Copiar archivos actualizados
Write-Host "  [7/7] Actualizando archivos..." -ForegroundColor Cyan

# Excluir estas carpetas/archivos
$excludeItems = @(".git", ".gitignore", ".github", "Ordenes", "Salidas", "actualizacion.log", "python", "libs")

$updatedCount = 0
$errorCount = 0

Get-ChildItem -Path $repoFolder -Recurse -Force | ForEach-Object {
    $relativePath = $_.FullName.Substring($repoFolder.Length + 1)
    
    # Verificar exclusiones
    $shouldExclude = $false
    foreach ($exclude in $excludeItems) {
        if ($relativePath -like "$exclude*") {
            $shouldExclude = $true
            break
        }
    }
    
    if ($shouldExclude) {
        return
    }
    
    $destPath = Join-Path $scriptDir $relativePath
    
    try {
        if ($_.PSIsContainer) {
            if (-not (Test-Path $destPath)) {
                New-Item -ItemType Directory -Path $destPath -Force | Out-Null
            }
        }
        else {
            $destDir = Split-Path -Parent $destPath
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Copy-Item $_.FullName $destPath -Force
            $updatedCount++
        }
    }
    catch {
        $errorCount++
    }
}

Write-Host "  [OK] $updatedCount archivo(s) actualizados" -ForegroundColor Green
if ($errorCount -gt 0) {
    Write-Host "  [!] $errorCount error(es) menores" -ForegroundColor Yellow
}

# Restaurar configuraciones
$restoredCount = 0
foreach ($file in $backupFiles) {
    $backupFile = Join-Path $backupDir $file
    if (Test-Path $backupFile) {
        Copy-Item $backupFile (Join-Path $scriptDir $file) -Force
        $restoredCount++
    }
}

# Limpiar
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

# Resultado final
Write-Host ""
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host "   [OK] ACTUALIZACION COMPLETADA" -ForegroundColor Green
Write-Host "  ================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Archivos actualizados: $updatedCount" -ForegroundColor White
Write-Host "  Configuraciones preservadas: $restoredCount" -ForegroundColor White
Write-Host ""
Write-Host "  Sistema actualizado a la ultima version de GitHub" -ForegroundColor Green
Write-Host ""

if (-not $Automatico) {
    Read-Host "Presiona Enter para salir"
} else {
    Write-Host "  Cerrando en 3 segundos..." -ForegroundColor Gray
    Start-Sleep -Seconds 3
}
