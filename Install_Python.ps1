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

# Funcion para verificar conectividad
function Test-InternetConnection {
    Write-Host "[TEST] Verificando conexion a internet..." -ForegroundColor Cyan
    try {
        $null = [System.Net.WebRequest]::Create("https://www.github.com").GetResponse()
        Write-Host "[OK] Conexion a internet: OK" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[ERROR] No hay conexion a internet o GitHub no es accesible" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
        return $false
    }
}

# Funcion para verificar si existe un release
function Test-ReleaseExists {
    param([string]$RepoName)
    
    Write-Host "[TEST] Verificando release en GitHub..." -ForegroundColor Cyan
    try {
        $apiUrl = "https://api.github.com/repos/$RepoName/releases/latest"
        $headers = @{
            "User-Agent" = "PowerShell/DHL-System"
        }
        
        $response = Invoke-RestMethod -Uri $apiUrl -Headers $headers -TimeoutSec 30
        
        if ($response -and $response.tag_name) {
            Write-Host "[OK] Release encontrado: $($response.tag_name)" -ForegroundColor Green
            Write-Host "   Publicado: $($response.published_at)" -ForegroundColor DarkGray
            
            # Verificar si existen los assets necesarios
            $pythonAsset = $response.assets | Where-Object { $_.name -eq "python-portable.zip" }
            $libsAsset = $response.assets | Where-Object { $_.name -eq "libs-portable.zip" }
            
            if (-not $pythonAsset) {
                Write-Host "[WARNING] No se encontro python-portable.zip en el release" -ForegroundColor Yellow
                return $false
            }
            
            if (-not $libsAsset) {
                Write-Host "[WARNING] No se encontro libs-portable.zip en el release" -ForegroundColor Yellow
                return $false
            }
            
            Write-Host "[OK] Todos los archivos necesarios estan disponibles" -ForegroundColor Green
            return $true
        }
        return $false
    }
    catch {
        Write-Host "[ERROR] No se pudo verificar el release" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor DarkRed
        return $false
    }
}

# URLs de descarga desde GitHub Release
$GITHUB_REPO = "Lucasgnemmi123/Sys_Procesar_Ordenes"
$GITHUB_RELEASE_URL = "https://github.com/$GITHUB_REPO/releases/latest/download"
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
        
        # Configurar timeout
        $webClient.Proxy.Credentials = [System.Net.CredentialCache]::DefaultNetworkCredentials
        
        # Descargar archivo
        Write-Host "   Descargando..." -ForegroundColor DarkGray
        $webClient.DownloadFile($Url, $OutputPath)
        
        # Verificar que el archivo se descargo correctamente
        if (Test-Path $OutputPath) {
            $fileSize = (Get-Item $OutputPath).Length
            if ($fileSize -gt 1000) {  # Al menos 1KB
                $sizeMB = [math]::Round($fileSize/1MB, 2)
                Write-Host "[OK] Descarga completada: $sizeMB MB" -ForegroundColor Green
                return $true
            } else {
                Write-Host "[ERROR] Archivo descargado esta vacio o corrupto ($fileSize bytes)" -ForegroundColor Red
                if (Test-Path $OutputPath) {
                    Remove-Item $OutputPath -Force
                }
                return $false
            }
        } else {
            Write-Host "[ERROR] Archivo no se creo" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "[ERROR] Error al descargar: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.InnerException) {
            Write-Host "   Detalles: $($_.Exception.InnerException.Message)" -ForegroundColor DarkRed
        }
        
        # Sugerencias segun el tipo de error
        if ($_.Exception.Message -match "404") {
            Write-Host ""
            Write-Host "[AYUDA] Error 404: El archivo no existe en el servidor" -ForegroundColor Yellow
            Write-Host "   Verifica que el release este publicado correctamente" -ForegroundColor White
        }
        elseif ($_.Exception.Message -match "proxy") {
            Write-Host ""
            Write-Host "[AYUDA] Problema con proxy detectado" -ForegroundColor Yellow
            Write-Host "   Contacta al administrador de red para configurar el proxy" -ForegroundColor White
        }
        
        return $false
    }
}

# Funcion para extraer ZIP con metodos alternativos
function Extract-Zip {
    param (
        [string]$ZipPath,
        [string]$DestinationPath
    )
    
    Write-Host "Extrayendo: $(Split-Path $ZipPath -Leaf)" -ForegroundColor Yellow
    Write-Host "   Destino: $DestinationPath" -ForegroundColor DarkGray
    
    # Verificar que el ZIP existe y no esta vacio
    if (-not (Test-Path $ZipPath)) {
        Write-Host "[ERROR] Archivo ZIP no existe: $ZipPath" -ForegroundColor Red
        return $false
    }
    
    $zipSize = (Get-Item $ZipPath).Length
    if ($zipSize -lt 1000) {
        Write-Host "[ERROR] Archivo ZIP corrupto o vacio ($zipSize bytes)" -ForegroundColor Red
        return $false
    }
    
    # Crear directorio de destino si no existe
    if (-not (Test-Path $DestinationPath)) {
        New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
    }
    
    # METODO 1: Usar .NET System.IO.Compression
    Write-Host "   [Metodo 1] Extraccion con .NET..." -ForegroundColor DarkGray
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        [System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $DestinationPath)
        Write-Host "[OK] Extraccion completada exitosamente" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[WARNING] Metodo 1 fallo: $($_.Exception.Message)" -ForegroundColor Yellow
        
        # Si el error es por directorio existente, limpiar e intentar de nuevo
        if ($_.Exception.Message -match "already exists") {
            Write-Host "   Limpiando directorio existente..." -ForegroundColor Yellow
            Remove-Item -Path $DestinationPath -Recurse -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
            
            try {
                New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
                [System.IO.Compression.ZipFile]::ExtractToDirectory($ZipPath, $DestinationPath)
                Write-Host "[OK] Extraccion completada (segundo intento)" -ForegroundColor Green
                return $true
            }
            catch {
                Write-Host "[WARNING] Segundo intento fallo" -ForegroundColor Yellow
            }
        }
    }
    
    # METODO 2: Usar Expand-Archive (PowerShell nativo)
    Write-Host "   [Metodo 2] Extraccion con PowerShell..." -ForegroundColor DarkGray
    try {
        # Limpiar destino
        if (Test-Path $DestinationPath) {
            Remove-Item -Path $DestinationPath -Recurse -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        }
        
        New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
        Expand-Archive -Path $ZipPath -DestinationPath $DestinationPath -Force
        Write-Host "[OK] Extraccion completada con metodo alternativo" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[WARNING] Metodo 2 fallo: $($_.Exception.Message)" -ForegroundColor Yellow
    }
    
    # METODO 3: Usar Shell.Application (metodo COM)
    Write-Host "   [Metodo 3] Extraccion con Shell.Application..." -ForegroundColor DarkGray
    try {
        # Limpiar destino
        if (Test-Path $DestinationPath) {
            Remove-Item -Path $DestinationPath -Recurse -Force -ErrorAction SilentlyContinue
            Start-Sleep -Milliseconds 500
        }
        
        New-Item -ItemType Directory -Path $DestinationPath -Force | Out-Null
        
        $shell = New-Object -ComObject Shell.Application
        $zip = $shell.NameSpace($ZipPath)
        $dest = $shell.NameSpace($DestinationPath)
        
        # 16 = responder "Si a todo" automaticamente
        $dest.CopyHere($zip.Items(), 16)
        
        # Esperar a que complete
        Start-Sleep -Seconds 2
        
        Write-Host "[OK] Extraccion completada con Shell.Application" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "[ERROR] Metodo 3 fallo: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Si todos los metodos fallaron
    Write-Host ""
    Write-Host "[ERROR CRITICO] No se pudo extraer el archivo ZIP con ningun metodo" -ForegroundColor Red
    Write-Host "   Archivo: $ZipPath" -ForegroundColor White
    Write-Host "   Tamaño: $([math]::Round($zipSize/1MB, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "Intenta extraer manualmente:" -ForegroundColor Yellow
    Write-Host "1. Haz clic derecho en el archivo ZIP" -ForegroundColor White
    Write-Host "2. Selecciona 'Extraer todo...'" -ForegroundColor White
    Write-Host "3. Extrae en: $DestinationPath" -ForegroundColor White
    Write-Host ""
    
    return $false
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

# ==== BUSCAR ARCHIVOS LOCALES PRIMERO ====
$LocalPythonZip = Join-Path $ScriptDir "python-portable.zip"
$LocalLibsZip = Join-Path $ScriptDir "libs-portable.zip"

$PythonZip = Join-Path $TempDir "python-portable.zip"
$LibsZip = Join-Path $TempDir "libs-portable.zip"

# Python
Write-Host "[BUSCAR 1/2] Buscando python-portable.zip..." -ForegroundColor Cyan

if (Test-Path $LocalPythonZip) {
    $localSize = [math]::Round((Get-Item $LocalPythonZip).Length/1MB, 2)
    Write-Host "[OK] Encontrado localmente ($localSize MB)" -ForegroundColor Green
    Write-Host "   Copiando desde archivo local..." -ForegroundColor DarkGray
    Copy-Item -Path $LocalPythonZip -Destination $PythonZip -Force
} else {
    Write-Host "[INFO] No encontrado localmente, descargando desde GitHub..." -ForegroundColor Yellow
    Write-Host "   URL: $PYTHON_ZIP_URL" -ForegroundColor DarkGray
    
    if (-not (Download-File -Url $PYTHON_ZIP_URL -OutputPath $PythonZip)) {
        Write-Host ""
        Write-Host "[ERROR CRITICO] No se pudo descargar Python portable" -ForegroundColor Red
        Write-Host ""
        Write-Host "El archivo NO existe en GitHub (Error 404)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "SOLUCION:" -ForegroundColor Cyan
        Write-Host "1. Debes crear el release primero ejecutando: Preparar_Release.bat" -ForegroundColor White
        Write-Host "   (Esto empaqueta python y libs en archivos .zip)" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "2. Luego sube esos archivos a GitHub:" -ForegroundColor White
        Write-Host "   a) Ve a: https://github.com/$GITHUB_REPO/releases/new" -ForegroundColor DarkGray
        Write-Host "   b) Crea un nuevo release" -ForegroundColor DarkGray
        Write-Host "   c) Sube python-portable.zip y libs-portable.zip" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "3. O ALTERNATIVA RAPIDA: Copia los archivos ZIP manualmente" -ForegroundColor White
        Write-Host "   - Copia python-portable.zip a este directorio: $ScriptDir" -ForegroundColor DarkGray
        Write-Host "   - Copia libs-portable.zip a este directorio: $ScriptDir" -ForegroundColor DarkGray
        Write-Host "   - Vuelve a ejecutar Install_Python.bat" -ForegroundColor DarkGray
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Librerias
Write-Host ""
Write-Host "[BUSCAR 2/2] Buscando libs-portable.zip..." -ForegroundColor Cyan

if (Test-Path $LocalLibsZip) {
    $localSize = [math]::Round((Get-Item $LocalLibsZip).Length/1MB, 2)
    Write-Host "[OK] Encontrado localmente ($localSize MB)" -ForegroundColor Green
    Write-Host "   Copiando desde archivo local..." -ForegroundColor DarkGray
    Copy-Item -Path $LocalLibsZip -Destination $LibsZip -Force
} else {
    Write-Host "[INFO] No encontrado localmente, descargando desde GitHub..." -ForegroundColor Yellow
    Write-Host "   URL: $LIBS_ZIP_URL" -ForegroundColor DarkGray
    
    if (-not (Download-File -Url $LIBS_ZIP_URL -OutputPath $LibsZip)) {
        Write-Host ""
        Write-Host "[ERROR CRITICO] No se pudo descargar las librerias" -ForegroundColor Red
        Write-Host ""
        Write-Host "El archivo NO existe en GitHub (Error 404)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "SOLUCION:" -ForegroundColor Cyan
        Write-Host "1. Debes crear el release primero ejecutando: Preparar_Release.bat" -ForegroundColor White
        Write-Host "   (Esto empaqueta python y libs en archivos .zip)" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "2. Luego sube esos archivos a GitHub:" -ForegroundColor White
        Write-Host "   a) Ve a: https://github.com/$GITHUB_REPO/releases/new" -ForegroundColor DarkGray
        Write-Host "   b) Crea un nuevo release" -ForegroundColor DarkGray
        Write-Host "   c) Sube python-portable.zip y libs-portable.zip" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "3. O ALTERNATIVA RAPIDA: Copia los archivos ZIP manualmente" -ForegroundColor White
        Write-Host "   - Copia python-portable.zip a este directorio: $ScriptDir" -ForegroundColor DarkGray
        Write-Host "   - Copia libs-portable.zip a este directorio: $ScriptDir" -ForegroundColor DarkGray
        Write-Host "   - Vuelve a ejecutar Install_Python.bat" -ForegroundColor DarkGray
        Write-Host ""
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Instalando Componentes...  " -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Extraer Python
Write-Host "[INSTALAR 1/2] Python..." -ForegroundColor Cyan
$pythonExtractPath = $PythonDir
if (-not (Extract-Zip -ZipPath $PythonZip -DestinationPath $pythonExtractPath)) {
    Write-Host ""
    Write-Host "[ERROR] Error al instalar Python" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solucion manual:" -ForegroundColor Yellow
    Write-Host "1. El archivo esta en: $PythonZip" -ForegroundColor White
    Write-Host "2. Extraelo manualmente a: $pythonExtractPath" -ForegroundColor White
    Write-Host "3. Asegurate que python.exe este en: $pythonExtractPath\python.exe" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que Python se extrajo correctamente
$pythonExeCheck = Join-Path $PythonDir "python.exe"
if (-not (Test-Path $pythonExeCheck)) {
    Write-Host "[WARNING] python.exe no encontrado en ubicacion esperada" -ForegroundColor Yellow
    Write-Host "   Buscando python.exe..." -ForegroundColor DarkGray
    
    # Buscar python.exe en subdirectorios
    $foundPython = Get-ChildItem -Path $PythonDir -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if ($foundPython) {
        Write-Host "[OK] python.exe encontrado en: $($foundPython.DirectoryName)" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] No se encontro python.exe despues de la extraccion" -ForegroundColor Red
        exit 1
    }
}

# Extraer Librerias
Write-Host ""
Write-Host "[INSTALAR 2/2] Librerias..." -ForegroundColor Cyan
$libsExtractPath = $LibsDir
if (-not (Extract-Zip -ZipPath $LibsZip -DestinationPath $libsExtractPath)) {
    Write-Host ""
    Write-Host "[ERROR] Error al instalar librerias" -ForegroundColor Red
    Write-Host ""
    Write-Host "Solucion manual:" -ForegroundColor Yellow
    Write-Host "1. El archivo esta en: $LibsZip" -ForegroundColor White
    Write-Host "2. Extraelo manualmente a: $libsExtractPath" -ForegroundColor White
    Write-Host ""
    Read-Host "Presiona Enter para salir"
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
