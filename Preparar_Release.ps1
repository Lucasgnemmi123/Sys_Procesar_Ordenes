# ============================================
# Preparar Archivos para GitHub Release
# Sistema DHL - Lucas Gnemmi
# ============================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DHL System - Preparar Release para GitHub  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Verificar que existen las carpetas
Write-Host "Verificando carpetas..." -ForegroundColor Yellow

if (-not (Test-Path (Join-Path $ScriptDir "python"))) {
    Write-Host "❌ Error: No se encontró la carpeta 'python/'" -ForegroundColor Red
    Write-Host "   Asegúrate de que la carpeta python/ existe en el directorio actual." -ForegroundColor White
    exit 1
}

if (-not (Test-Path (Join-Path $ScriptDir "libs"))) {
    Write-Host "❌ Error: No se encontró la carpeta 'libs/'" -ForegroundColor Red
    Write-Host "   Asegúrate de que la carpeta libs/ existe en el directorio actual." -ForegroundColor White
    exit 1
}

Write-Host "✅ Carpetas encontradas" -ForegroundColor Green
Write-Host ""

# Crear carpeta de salida para los ZIPs
$OutputDir = Join-Path $ScriptDir "Release"
if (Test-Path $OutputDir) {
    Write-Host "Eliminando Release anterior..." -ForegroundColor Yellow
    Remove-Item -Path $OutputDir -Recurse -Force
}
New-Item -ItemType Directory -Path $OutputDir | Out-Null
Write-Host "✅ Carpeta Release creada: $OutputDir" -ForegroundColor Green
Write-Host ""

# Comprimir Python
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Comprimiendo Python (esto puede tardar...)  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$PythonSource = Join-Path $ScriptDir "python"
$PythonZip = Join-Path $OutputDir "python-portable.zip"

Write-Host "Origen: $PythonSource" -ForegroundColor White
Write-Host "Destino: $PythonZip" -ForegroundColor White
Write-Host ""

try {
    $startTime = Get-Date
    Write-Host "⏳ Comprimiendo Python portable..." -ForegroundColor Cyan
    Compress-Archive -Path $PythonSource -DestinationPath $PythonZip -CompressionLevel Optimal -Force
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    $size = (Get-Item $PythonZip).Length / 1MB
    Write-Host "✅ Python comprimido exitosamente" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($size, 2)) MB" -ForegroundColor White
    Write-Host "   Tiempo: $([math]::Round($duration, 1)) segundos" -ForegroundColor White
}
catch {
    Write-Host "❌ Error al comprimir Python: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Comprimir Librerías
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Comprimiendo Librerías (esto puede tardar...)  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$LibsSource = Join-Path $ScriptDir "libs"
$LibsZip = Join-Path $OutputDir "libs-portable.zip"

Write-Host "Origen: $LibsSource" -ForegroundColor White
Write-Host "Destino: $LibsZip" -ForegroundColor White
Write-Host ""

try {
    $startTime = Get-Date
    Write-Host "⏳ Comprimiendo librerías..." -ForegroundColor Cyan
    Compress-Archive -Path $LibsSource -DestinationPath $LibsZip -CompressionLevel Optimal -Force
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    
    $size = (Get-Item $LibsZip).Length / 1MB
    Write-Host "✅ Librerías comprimidas exitosamente" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($size, 2)) MB" -ForegroundColor White
    Write-Host "   Tiempo: $([math]::Round($duration, 1)) segundos" -ForegroundColor White
}
catch {
    Write-Host "❌ Error al comprimir librerías: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Resumen final
Write-Host "================================================" -ForegroundColor Green
Write-Host "  ✅ ARCHIVOS LISTOS PARA GITHUB RELEASE  " -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Los siguientes archivos están listos para subir:" -ForegroundColor White
Write-Host ""

$pythonSize = (Get-Item $PythonZip).Length / 1MB
$libsSize = (Get-Item $LibsZip).Length / 1MB
$totalSize = $pythonSize + $libsSize

Write-Host "  📦 $PythonZip" -ForegroundColor Cyan
Write-Host "     Tamaño: $([math]::Round($pythonSize, 2)) MB" -ForegroundColor White
Write-Host ""
Write-Host "  📦 $LibsZip" -ForegroundColor Cyan
Write-Host "     Tamaño: $([math]::Round($libsSize, 2)) MB" -ForegroundColor White
Write-Host ""
Write-Host "  📊 Total: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Yellow
Write-Host ""

# Instrucciones
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Proximos Pasos  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ve a tu repositorio en GitHub" -ForegroundColor White
Write-Host "2. Click en Releases y luego Create a new release" -ForegroundColor White
Write-Host "3. Tag: v3.0.0" -ForegroundColor White
Write-Host "4. Titulo: DHL Order Processing System v3.0.0 - Portable" -ForegroundColor White
Write-Host "5. Arrastra y suelta estos archivos:" -ForegroundColor White
Write-Host "   - python-portable.zip" -ForegroundColor Cyan
Write-Host "   - libs-portable.zip" -ForegroundColor Cyan
Write-Host "6. Publica el release" -ForegroundColor White
Write-Host ""
Write-Host "7. Actualiza Descargar_Python.ps1 con tu URL de GitHub" -ForegroundColor White
Write-Host ""
Write-Host "Mas detalles en: docs/GUIA_DISTRIBUCION.md" -ForegroundColor Yellow
Write-Host ""
Read-Host "Presiona Enter para salir"
