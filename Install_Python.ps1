# ============================================
# Descargador Automatico de Python Portable
# Sistema DHL - Lucas Gnemmi
# ============================================

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DHL Order Processing System - Setup  " -ForegroundColor Yellow
Write-Host "  Descargador de Python Portable v3.13  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

# Habilitar TLS 1.2 para todas las conexiones (requerido por GitHub)
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Validar que el directorio del script es valido
if ([string]::IsNullOrWhiteSpace($ScriptDir)) {
    Write-Host "[ERROR] No se pudo determinar el directorio del script" -ForegroundColor Red
    Write-Host "   Intenta ejecutar el script desde una ubicacion local (no desde red)" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[INFO] Directorio de trabajo: $ScriptDir" -ForegroundColor DarkGray
Write-Host ""

$PythonDir = Join-Path $ScriptDir "python"
$LibsDir = Join-Path $ScriptDir "libs"

# URLs de descarga desde GitHub Release
$GITHUB_RELEASE_URL = "https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes/releases/latest/download"
$PYTHON_ZIP_URL = "$GITHUB_RELEASE_URL/python-portable.zip"
$LIBS_ZIP_URL = "$GITHUB_RELEASE_URL/libs-portable.zip"

# Funcion para descargar con progreso
function Download-File {
    param (
        [string]$Url,
        [string]$OutputPath
    )
    
    Write-Host "Descargando desde: $Url" -ForegroundColor Yellow
    
    try {
        # Validar parametros
        if ([string]::IsNullOrWhiteSpace($Url)) {
            Write-Host "[ERROR] URL esta vacia" -ForegroundColor Red
            return $false
        }
        
        if ([string]::IsNullOrWhiteSpace($OutputPath)) {
            Write-Host "[ERROR] Ruta de salida esta vacia" -ForegroundColor Red
            return $false
        }
        
        # Habilitar TLS 1.2 (requerido por GitHub)
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        
        # Crear directorio si no existe
        $outputDir = Split-Path -Parent $OutputPath
        if (-not [string]::IsNullOrWhiteSpace($outputDir) -and -not (Test-Path $outputDir)) {
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }
        
        # Usar WebClient con configuracion mejorada
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.Add("User-Agent", "PowerShell/DHL-System")
        
        # Descargar archivo
        $webClient.DownloadFile($Url, $OutputPath)
        
        # Verificar que el archivo se descargo correctamente
        if (Test-Path $OutputPath) {
            $fileSize = (Get-Item $OutputPath).Length
            if ($fileSize -gt 0) {
                $sizeMB = [math]::Round($fileSize/1MB, 2)
                Write-Host "[OK] Descarga completada: $OutputPath ($sizeMB MB)" -ForegroundColor Green
                return $true
            } else {
                Write-Host "[ERROR] Archivo descargado esta vacio" -ForegroundColor Red
                return $false
            }
        } else {
            Write-Host "[ERROR] Archivo no se creo" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "[ERROR] Error al descargar: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "   Detalles: $($_.Exception.InnerException.Message)" -ForegroundColor DarkRed
        return $false
    }
}

# Funcion para extraer ZIP
function Extract-Zip {
    param (
        [string]$ZipPath,
        [string]$DestinationPath
    )
    
    Write-Host "Extrayendo: $ZipPath -> $DestinationPath" -ForegroundColor Yellow
    
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $DestinationPath)
        Write-Host "[OK] Extraccion completada" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[ERROR] Error al extraer: $_" -ForegroundColor Red
        return $false
    }
}

# Verificar si ya existe Python
if (Test-Path $PythonDir) {
    Write-Host ""
    Write-Host "[AVISO] Python portable ya existe en: $PythonDir" -ForegroundColor Yellow
    $response = Read-Host "Deseas reemplazarlo? (S/N)"
    if ($response -ne "S" -and $response -ne "s") {
        Write-Host "Operacion cancelada por el usuario." -ForegroundColor Yellow
        exit 0
    }
    Write-Host "Eliminando version anterior..." -ForegroundColor Yellow
    Remove-Item -Path $PythonDir -Recurse -Force
}

# Verificar si ya existe Libs
if (Test-Path $LibsDir) {
    Write-Host ""
    Write-Host "[AVISO] Librerias ya existen en: $LibsDir" -ForegroundColor Yellow
    $response = Read-Host "Deseas reemplazarlas? (S/N)"
    if ($response -ne "S" -and $response -ne "s") {
        Write-Host "Operacion cancelada por el usuario." -ForegroundColor Yellow
        exit 0
    }
    Write-Host "Eliminando version anterior..." -ForegroundColor Yellow
    Remove-Item -Path $LibsDir -Recurse -Force
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Descargando Python Portable...  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Crear directorio temporal
$TempDir = Join-Path $env:TEMP "DHL_Python_Setup"
if (Test-Path $TempDir) {
    Remove-Item -Path $TempDir -Recurse -Force
}
New-Item -ItemType Directory -Path $TempDir | Out-Null

# Descargar Python
$PythonZip = Join-Path $TempDir "python-portable.zip"
Write-Host "[DESCARGA] Python 3.13 Portable..." -ForegroundColor Cyan
Write-Host "   URL: $PYTHON_ZIP_URL" -ForegroundColor DarkGray
if (-not (Download-File -Url $PYTHON_ZIP_URL -OutputPath $PythonZip)) {
    Write-Host ""
    Write-Host "[ERROR] No se pudo descargar Python portable" -ForegroundColor Red
    Write-Host ""
    Write-Host "Opciones alternativas:" -ForegroundColor Yellow
    Write-Host "1. Verifica tu conexion a internet" -ForegroundColor White
    Write-Host "2. Verifica que el Release existe en GitHub" -ForegroundColor White
    Write-Host "3. Contacta al administrador del sistema" -ForegroundColor White
    Write-Host "4. Descarga manualmente desde: $PYTHON_ZIP_URL" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Descargar Librerias
$LibsZip = Join-Path $TempDir "libs-portable.zip"
Write-Host ""
Write-Host "[DESCARGA] Librerias Python..." -ForegroundColor Cyan
Write-Host "   URL: $LIBS_ZIP_URL" -ForegroundColor DarkGray
if (-not (Download-File -Url $LIBS_ZIP_URL -OutputPath $LibsZip)) {
    Write-Host ""
    Write-Host "[ERROR] No se pudo descargar las librerias" -ForegroundColor Red
    Write-Host ""
    Write-Host "Opciones alternativas:" -ForegroundColor Yellow
    Write-Host "1. Verifica tu conexion a internet" -ForegroundColor White
    Write-Host "2. Verifica que el Release existe en GitHub" -ForegroundColor White
    Write-Host "3. Contacta al administrador del sistema" -ForegroundColor White
    Write-Host "4. Descarga manualmente desde: $LIBS_ZIP_URL" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Instalando Componentes...  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Extraer Python
Write-Host "[INSTALAR] Python..." -ForegroundColor Cyan
if (-not (Extract-Zip -ZipPath $PythonZip -DestinationPath $ScriptDir)) {
    Write-Host "[ERROR] Error al instalar Python" -ForegroundColor Red
    exit 1
}

# Extraer Librerias
Write-Host ""
Write-Host "[INSTALAR] Librerias..." -ForegroundColor Cyan
if (-not (Extract-Zip -ZipPath $LibsZip -DestinationPath $ScriptDir)) {
    Write-Host "[ERROR] Error al instalar librerias" -ForegroundColor Red
    exit 1
}

# Limpiar archivos temporales
Write-Host ""
Write-Host "[LIMPIEZA] Archivos temporales..." -ForegroundColor Cyan
Remove-Item -Path $TempDir -Recurse -Force

# Verificar instalacion
Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Verificando Instalacion...  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

$PythonExe = Join-Path $PythonDir "python.exe"
if (Test-Path $PythonExe) {
    Write-Host "[OK] Python instalado correctamente: $PythonExe" -ForegroundColor Green
    
    # Verificar version
    $Version = & $PythonExe --version 2>&1
    Write-Host "   Version: $Version" -ForegroundColor White
} else {
    Write-Host "[ERROR] No se encontro python.exe" -ForegroundColor Red
    exit 1
}

if (Test-Path $LibsDir) {
    Write-Host "[OK] Librerias instaladas correctamente: $LibsDir" -ForegroundColor Green
    
    # Contar librerias
    $LibCount = (Get-ChildItem -Path $LibsDir -Directory).Count
    Write-Host "   Total de paquetes: $LibCount" -ForegroundColor White
} else {
    Write-Host "[ERROR] No se encontro el directorio de librerias" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "  INSTALACION COMPLETADA CON EXITO  " -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "El sistema esta listo para usar." -ForegroundColor White
Write-Host "Ejecuta: EXE_Procesar_Ordenes.bat" -ForegroundColor Cyan
Write-Host ""
Read-Host "Presiona Enter para salir"
