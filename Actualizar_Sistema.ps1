# ====================================================================
# SISTEMA DE ACTUALIZACIÓN AUTOMÁTICA - DHL Procesar Pedidos
# ====================================================================
# Este script actualiza el sistema a la última versión desde GitHub
# NO requiere credenciales (repositorio público)
# ====================================================================

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Configuración
$repoUrl = "https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes.git"
$logFile = Join-Path $scriptDir "actualizacion.log"

# Función para escribir log
function Write-Log {
    param($Message, $Color = "White")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage -ForegroundColor $Color
    Add-Content -Path $logFile -Value $logMessage
}

# Función para mostrar menú
function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "  ================================================" -ForegroundColor Cyan
    Write-Host "   DHL - Sistema de Actualización v3.0" -ForegroundColor Yellow
    Write-Host "  ================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  [1] Verificar actualizaciones disponibles" -ForegroundColor Green
    Write-Host "  [2] Actualizar a la última versión" -ForegroundColor Green
    Write-Host "  [3] Verificar y reparar archivos" -ForegroundColor Yellow
    Write-Host "  [4] Ver información del sistema" -ForegroundColor Cyan
    Write-Host "  [0] Salir" -ForegroundColor Red
    Write-Host ""
    Write-Host "  ================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Función para verificar si hay actualizaciones (archivo por archivo)
function Check-Updates {
    Write-Log "Verificando actualizaciones disponibles..." "Cyan"
    
    try {
        # Verificar si Git está instalado
        $gitVersion = git --version 2>$null
        if (-not $gitVersion) {
            Write-Log "ERROR: Git no está instalado" "Red"
            Write-Host ""
            Write-Host "  Instala Git desde: https://git-scm.com/download/win" -ForegroundColor Yellow
            return $false
        }
        
        # Verificar si estamos en un repositorio Git
        $isGitRepo = Test-Path (Join-Path $scriptDir ".git")
        if (-not $isGitRepo) {
            Write-Log "ERROR: No es un repositorio Git válido" "Red"
            Write-Host ""
            Write-Host "  Descarga el proyecto completo desde GitHub" -ForegroundColor Yellow
            return $false
        }
        
        # Obtener información remota
        Write-Log "Consultando servidor GitHub..." "Gray"
        git fetch origin main 2>&1 | Out-Null
        
        # Comparar versiones
        $localCommit = git rev-parse HEAD
        $remoteCommit = git rev-parse origin/main
        
        Write-Host ""
        Write-Host "  ================================================" -ForegroundColor Cyan
        Write-Host "   VERIFICACIÓN DE ARCHIVOS DEL PROYECTO" -ForegroundColor Yellow
        Write-Host "  ================================================" -ForegroundColor Cyan
        Write-Host ""
        
        # Obtener lista de archivos diferentes
        $filesChanged = git diff --name-status HEAD origin/main
        
        if ($localCommit -eq $remoteCommit -or [string]::IsNullOrWhiteSpace($filesChanged)) {
            Write-Host "  ✓ El sistema está ACTUALIZADO" -ForegroundColor Green
            Write-Host "  ✓ Todos los archivos coinciden con GitHub" -ForegroundColor Green
            Write-Log "Sistema actualizado - Versión: $($localCommit.Substring(0,7))" "Green"
            Write-Log "Todos los archivos verificados - Sin cambios" "Green"
            
            Write-Host ""
            Write-Host "  Versión actual: $($localCommit.Substring(0,7))" -ForegroundColor Gray
            
            return @{
                UpdateAvailable = $false
                IsUpToDate = $true
                LocalCommit = $localCommit
                RemoteCommit = $remoteCommit
            }
        } else {
            Write-Host "  ⚠ HAY UNA NUEVA VERSIÓN DISPONIBLE" -ForegroundColor Yellow
            Write-Log "Actualización disponible - Local: $($localCommit.Substring(0,7)), Remoto: $($remoteCommit.Substring(0,7))" "Yellow"
            
            # Analizar cambios por tipo
            $filesModified = @()
            $filesAdded = @()
            $filesDeleted = @()
            
            $filesChanged -split "`n" | ForEach-Object {
                if ($_ -match '^M\s+(.+)$') {
                    $filesModified += $Matches[1]
                } elseif ($_ -match '^A\s+(.+)$') {
                    $filesAdded += $Matches[1]
                } elseif ($_ -match '^D\s+(.+)$') {
                    $filesDeleted += $Matches[1]
                }
            }
            
            Write-Host ""
            Write-Host "  ARCHIVOS MODIFICADOS:" -ForegroundColor Cyan
            if ($filesModified.Count -gt 0) {
                $filesModified | ForEach-Object {
                    Write-Host "    [M] $_" -ForegroundColor Yellow
                    Write-Log "  Modificado: $_" "Yellow"
                }
            } else {
                Write-Host "    (ninguno)" -ForegroundColor Gray
            }
            
            if ($filesAdded.Count -gt 0) {
                Write-Host ""
                Write-Host "  ARCHIVOS NUEVOS:" -ForegroundColor Cyan
                $filesAdded | ForEach-Object {
                    Write-Host "    [+] $_" -ForegroundColor Green
                    Write-Log "  Agregado: $_" "Green"
                }
            }
            
            if ($filesDeleted.Count -gt 0) {
                Write-Host ""
                Write-Host "  ARCHIVOS ELIMINADOS:" -ForegroundColor Cyan
                $filesDeleted | ForEach-Object {
                    Write-Host "    [-] $_" -ForegroundColor Red
                    Write-Log "  Eliminado: $_" "Red"
                }
            }
            
            # Mostrar resumen de commits
            Write-Host ""
            Write-Host "  CAMBIOS RECIENTES:" -ForegroundColor Cyan
            git log HEAD..origin/main --oneline --max-count=5 | ForEach-Object {
                Write-Host "    • $_" -ForegroundColor Gray
            }
            
            # Estadísticas
            $totalChanges = $filesModified.Count + $filesAdded.Count + $filesDeleted.Count
            Write-Host ""
            Write-Host "  RESUMEN: $totalChanges archivo(s) con cambios" -ForegroundColor Yellow
            Write-Host "  Versión local: $($localCommit.Substring(0,7))" -ForegroundColor Gray
            Write-Host "  Versión remota: $($remoteCommit.Substring(0,7))" -ForegroundColor Gray
            
            Write-Log "Total de archivos con cambios: $totalChanges" "Yellow"
            
            return @{
                UpdateAvailable = $true
                IsUpToDate = $false
                LocalCommit = $localCommit
                RemoteCommit = $remoteCommit
                TotalChanges = $totalChanges
                FilesModified = $filesModified
                FilesAdded = $filesAdded
                FilesDeleted = $filesDeleted
            }
        }
        
    } catch {
        Write-Log "ERROR al verificar actualizaciones: $_" "Red"
        return @{
            UpdateAvailable = $false
            IsUpToDate = $false
            Error = $_.Exception.Message
        }
    }
}

# Función para actualizar el sistema
function Update-System {
    Write-Log "Iniciando proceso de actualización..." "Cyan"
    
    try {
        # Primero verificar si hay actualizaciones disponibles
        Write-Host ""
        Write-Host "  Verificando estado del sistema..." -ForegroundColor Gray
        
        $checkResult = Check-Updates
        
        # Si no hay actualizaciones disponibles, no permitir actualizar
        if ($checkResult.IsUpToDate -eq $true) {
            Write-Host ""
            Write-Host "  ================================================" -ForegroundColor Cyan
            Write-Host "   NO SE PUEDE ACTUALIZAR" -ForegroundColor Red
            Write-Host "  ================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  ✓ Ya tienes la última versión" -ForegroundColor Green
            Write-Host "  ✓ Todos los archivos están actualizados" -ForegroundColor Green
            Write-Host ""
            Write-Log "Actualización cancelada - Sistema ya está al día" "Yellow"
            return $false
        }
        
        if (-not $checkResult.UpdateAvailable) {
            Write-Host ""
            Write-Host "  No se puede actualizar en este momento" -ForegroundColor Red
            Write-Log "Actualización cancelada - No disponible" "Red"
            return $false
        }
        
        # Mostrar resumen de cambios antes de actualizar
        Write-Host ""
        Write-Host "  ================================================" -ForegroundColor Cyan
        Write-Host "   RESUMEN DE ACTUALIZACIÓN" -ForegroundColor Yellow
        Write-Host "  ================================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  Se actualizarán $($checkResult.TotalChanges) archivo(s):" -ForegroundColor Cyan
        Write-Host "    • Modificados: $($checkResult.FilesModified.Count)" -ForegroundColor Yellow
        Write-Host "    • Nuevos: $($checkResult.FilesAdded.Count)" -ForegroundColor Green
        Write-Host "    • Eliminados: $($checkResult.FilesDeleted.Count)" -ForegroundColor Red
        Write-Host ""
        
        # Verificar conexión
        Write-Log "Verificando conexión con GitHub..." "Gray"
        $testConnection = Test-Connection github.com -Count 2 -Quiet
        if (-not $testConnection) {
            Write-Log "ERROR: No hay conexión a Internet" "Red"
            return $false
        }
        
        # Guardar archivos locales importantes
        Write-Log "Guardando configuraciones locales..." "Gray"
        $backupFiles = @(
            "agenda_config.json",
            "rules.json",
            "products.json"
        )
        
        $backupDir = Join-Path $scriptDir "backup_temp"
        if (Test-Path $backupDir) {
            Remove-Item $backupDir -Recurse -Force
        }
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        
        foreach ($file in $backupFiles) {
            $filePath = Join-Path $scriptDir $file
            if (Test-Path $filePath) {
                Copy-Item $filePath (Join-Path $backupDir $file) -Force
                Write-Log "  Respaldo: $file" "Gray"
            }
        }
        
        # Actualizar desde GitHub
        Write-Log "Descargando última versión desde GitHub..." "Yellow"
        Write-Host "  Descargando archivos..." -ForegroundColor Yellow
        Write-Host ""
        git fetch origin main
        git reset --hard origin/main
        
        # Restaurar archivos locales
        Write-Log "Restaurando configuraciones locales..." "Gray"
        foreach ($file in $backupFiles) {
            $backupFile = Join-Path $backupDir $file
            if (Test-Path $backupFile) {
                Copy-Item $backupFile (Join-Path $scriptDir $file) -Force
                Write-Log "  Restaurado: $file" "Gray"
            }
        }
        
        # Limpiar backup temporal
        Remove-Item $backupDir -Recurse -Force
        
        # Verificar actualización exitosa
        $newCommit = git rev-parse HEAD
        if ($newCommit -eq $checkResult.RemoteCommit) {
            Write-Host ""
            Write-Host "  ================================================" -ForegroundColor Cyan
            Write-Host "   ✓ ACTUALIZACIÓN COMPLETADA" -ForegroundColor Green
            Write-Host "  ================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  Versión instalada: $($newCommit.Substring(0,7))" -ForegroundColor Gray
            Write-Host "  Archivos actualizados: $($checkResult.TotalChanges)" -ForegroundColor Gray
            Write-Host ""
            Write-Log "Sistema actualizado correctamente a versión: $($newCommit.Substring(0,7))" "Green"
            return $true
        } else {
            Write-Host "  ⚠ Actualización completada con advertencias" -ForegroundColor Yellow
            Write-Log "Actualización completada - Verificar estado" "Yellow"
            return $true
        }
        
    } catch {
        Write-Log "ERROR durante la actualización: $_" "Red"
        Write-Host ""
        Write-Host "  ❌ Error durante la actualización" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Si el error persiste, descarga el proyecto nuevamente desde:" -ForegroundColor Yellow
        Write-Host "  $repoUrl" -ForegroundColor Cyan
        return $false
    }
}

# Función para verificar archivos críticos
function Verify-Files {
    Write-Log "Verificando integridad de archivos..." "Cyan"
    
    $criticalFiles = @(
        @{Path="gui_moderna_v2.py"; Desc="Interfaz principal"},
        @{Path="procesamiento_v2.py"; Desc="Motor de procesamiento"},
        @{Path="agenda_manager.py"; Desc="Gestor de agenda"},
        @{Path="rules_manager.py"; Desc="Gestor de reglas"},
        @{Path="products_manager.py"; Desc="Gestor de productos"},
        @{Path="libs"; Desc="Librerías empaquetadas"; IsDir=$true},
        @{Path="EXE_Procesar_Ordenes.bat"; Desc="Launcher principal"}
    )
    
    $missingFiles = @()
    $totalFiles = $criticalFiles.Count
    $checkedFiles = 0
    
    Write-Host ""
    foreach ($file in $criticalFiles) {
        $checkedFiles++
        $filePath = Join-Path $scriptDir $file.Path
        $exists = if ($file.IsDir) { Test-Path $filePath } else { Test-Path $filePath }
        
        $status = if ($exists) { "[OK]" } else { "[FALTA]"; $missingFiles += $file }
        $color = if ($exists) { "Green" } else { "Red" }
        
        Write-Host "  $status $($file.Desc)" -ForegroundColor $color
        Write-Log "$status $($file.Path) - $($file.Desc)" $(if ($exists) {"Green"} else {"Red"})
    }
    
    Write-Host ""
    if ($missingFiles.Count -eq 0) {
        Write-Host "  Todos los archivos están presentes" -ForegroundColor Green
        Write-Log "Verificación completada - OK" "Green"
        return $true
    } else {
        Write-Host "  ¡Atención! Faltan $($missingFiles.Count) archivos críticos" -ForegroundColor Red
        Write-Log "Verificación completada - Faltan $($missingFiles.Count) archivos" "Red"
        
        Write-Host ""
        $response = Read-Host "  ¿Deseas intentar reparar descargando la última versión? (S/N)"
        if ($response -eq "S" -or $response -eq "s") {
            return Update-System
        }
        return $false
    }
}

# Función para mostrar información del sistema
function Show-SystemInfo {
    Write-Host ""
    Write-Host "  INFORMACIÓN DEL SISTEMA" -ForegroundColor Cyan
    Write-Host "  ===============================================" -ForegroundColor Cyan
    
    try {
        # Versión actual
        $currentCommit = git rev-parse --short HEAD 2>$null
        $currentDate = git log -1 --format=%cd --date=format:"%d/%m/%Y %H:%M" 2>$null
        $currentMessage = git log -1 --format=%s 2>$null
        
        Write-Host ""
        Write-Host "  Versión actual:" -ForegroundColor Yellow
        Write-Host "    Commit: $currentCommit" -ForegroundColor Gray
        Write-Host "    Fecha: $currentDate" -ForegroundColor Gray
        Write-Host "    Mensaje: $currentMessage" -ForegroundColor Gray
        
        # Python
        $pythonPath = Join-Path $scriptDir ".venv\Scripts\python.exe"
        if (Test-Path $pythonPath) {
            $pythonVersion = & $pythonPath --version 2>&1
            Write-Host ""
            Write-Host "  Python: $pythonVersion" -ForegroundColor Gray
        }
        
        # Tamaño del proyecto
        $projectSize = (Get-ChildItem $scriptDir -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "  Tamaño: $([math]::Round($projectSize, 2)) MB" -ForegroundColor Gray
        
        # Repositorio
        Write-Host ""
        Write-Host "  Repositorio: $repoUrl" -ForegroundColor Gray
        
        Write-Log "Información del sistema consultada" "Gray"
        
    } catch {
        Write-Host "  Error al obtener información: $_" -ForegroundColor Red
    }
}

# ====================================================================
# PROGRAMA PRINCIPAL
# ====================================================================

Write-Log "=== Inicio del sistema de actualización ===" "Cyan"

# Bucle principal del menú
do {
    Show-Menu
    $opcion = Read-Host "  Selecciona una opción"
    Write-Host ""
    
    switch ($opcion) {
        "1" {
            $result = Check-Updates
            Write-Host ""
            if ($result.UpdateAvailable -eq $true) {
                Write-Host "  ¿Deseas actualizar ahora? (S/N): " -ForegroundColor Yellow -NoNewline
                $updateNow = Read-Host
                if ($updateNow -eq "S" -or $updateNow -eq "s") {
                    Write-Host ""
                    Update-System
                }
            }
            Write-Host ""
            Read-Host "  Presiona Enter para continuar"
        }
        "2" {
            Write-Host "  ================================================" -ForegroundColor Cyan
            Write-Host "   ACTUALIZAR SISTEMA" -ForegroundColor Yellow
            Write-Host "  ================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "  Esta operación descargará la última versión desde GitHub" -ForegroundColor Gray
            Write-Host "  y actualizará todos los archivos del proyecto." -ForegroundColor Gray
            Write-Host ""
            $confirm = Read-Host "  ¿Confirmas que deseas actualizar el sistema? (S/N)"
            if ($confirm -eq "S" -or $confirm -eq "s") {
                Update-System
            } else {
                Write-Host ""
                Write-Host "  Actualización cancelada por el usuario" -ForegroundColor Yellow
            }
            Write-Host ""
            Read-Host "  Presiona Enter para continuar"
        }
        "3" {
            Verify-Files
            Write-Host ""
            Read-Host "  Presiona Enter para continuar"
        }
        "4" {
            Show-SystemInfo
            Write-Host ""
            Read-Host "  Presiona Enter para continuar"
        }
        "0" {
            Write-Log "=== Fin del sistema de actualización ===" "Cyan"
            Write-Host "  ¡Hasta pronto!" -ForegroundColor Green
            Write-Host ""
        }
        default {
            Write-Host "  Opción no válida" -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
    
} while ($opcion -ne "0")
