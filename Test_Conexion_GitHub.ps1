# ============================================
# Script de Prueba de Conexión a GitHub
# ============================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Test de Conexión - GitHub Releases  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Habilitar TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$GITHUB_REPO = "Lucasgnemmi123/Sys_Procesar_Ordenes"
$PYTHON_ZIP_URL = "https://github.com/$GITHUB_REPO/releases/latest/download/python-portable.zip"
$LIBS_ZIP_URL = "https://github.com/$GITHUB_REPO/releases/latest/download/libs-portable.zip"

Write-Host "Repositorio: $GITHUB_REPO" -ForegroundColor White
Write-Host ""

# Test 1: Verificar conectividad a GitHub
Write-Host "📡 Test 1: Verificando conectividad a GitHub..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "https://github.com" -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Conectividad OK - Status: $($response.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error de conectividad: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Verifica tu conexión a internet" -ForegroundColor Yellow
}

Write-Host ""

# Test 2: Verificar que el repositorio existe
Write-Host "📡 Test 2: Verificando repositorio..." -ForegroundColor Cyan
try {
    $repoUrl = "https://github.com/$GITHUB_REPO"
    $response = Invoke-WebRequest -Uri $repoUrl -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Repositorio existe - Status: $($response.StatusCode)" -ForegroundColor Green
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   El repositorio podría no existir o ser privado" -ForegroundColor Yellow
}

Write-Host ""

# Test 3: Verificar releases
Write-Host "📡 Test 3: Verificando releases..." -ForegroundColor Cyan
try {
    $releasesUrl = "https://github.com/$GITHUB_REPO/releases/latest"
    $response = Invoke-WebRequest -Uri $releasesUrl -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Releases OK - Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Redirigido a: $($response.BaseResponse.ResponseUri)" -ForegroundColor DarkGray
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   No se encontró ningún release en el repositorio" -ForegroundColor Yellow
}

Write-Host ""

# Test 4: Verificar archivo python-portable.zip
Write-Host "📡 Test 4: Verificando python-portable.zip..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $PYTHON_ZIP_URL -Method Head -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Archivo existe - Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($response.Headers.'Content-Length'/1MB, 2)) MB" -ForegroundColor DarkGray
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   El archivo python-portable.zip no existe en el release" -ForegroundColor Yellow
}

Write-Host ""

# Test 5: Verificar archivo libs-portable.zip
Write-Host "📡 Test 5: Verificando libs-portable.zip..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $LIBS_ZIP_URL -Method Head -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ Archivo existe - Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Tamaño: $([math]::Round($response.Headers.'Content-Length'/1MB, 2)) MB" -ForegroundColor DarkGray
}
catch {
    Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   El archivo libs-portable.zip no existe en el release" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Diagnóstico completo  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Si todos los tests pasaron, el problema podría ser:" -ForegroundColor Yellow
Write-Host "  • Firewall o antivirus bloqueando la descarga" -ForegroundColor White
Write-Host "  • Permisos insuficientes en la carpeta de destino" -ForegroundColor White
Write-Host ""

Write-Host "Si los tests 4 o 5 fallaron:" -ForegroundColor Yellow
Write-Host "  • Los archivos no están en el release de GitHub" -ForegroundColor White
Write-Host "  • Necesitas crear un release con esos archivos" -ForegroundColor White
Write-Host ""

Read-Host "Presiona Enter para salir"
