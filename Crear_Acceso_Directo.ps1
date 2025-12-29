# Script para crear un acceso directo con icono personalizado
Write-Host "=" -repeat 70 -ForegroundColor Cyan
Write-Host "CREADOR DE ACCESO DIRECTO CON ICONO" -ForegroundColor Yellow
Write-Host "=" -repeat 70 -ForegroundColor Cyan
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$batPath = Join-Path $scriptDir "EXE_Procesar_Ordenes.bat"
$iconPath = Join-Path $scriptDir "launcher_icon.ico"
$shortcutPath = Join-Path $scriptDir "Procesar Pedidos DHL.lnk"

# Crear objeto Shell
$WScriptShell = New-Object -ComObject WScript.Shell

# Crear acceso directo
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $batPath
$Shortcut.WorkingDirectory = $scriptDir
$Shortcut.Description = "Sistema de Procesamiento de Pedidos DHL"

# Asignar icono si existe
if (Test-Path $iconPath) {
    $Shortcut.IconLocation = $iconPath
    Write-Host "Icono asignado: launcher_icon.ico" -ForegroundColor Green
} else {
    Write-Host "No se encontro el icono, usando icono predeterminado" -ForegroundColor Yellow
}

$Shortcut.Save()

Write-Host ""
Write-Host "Acceso directo creado exitosamente!" -ForegroundColor Green
Write-Host "Ubicacion: $shortcutPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ahora puedes:" -ForegroundColor Yellow
Write-Host "   1. Hacer doble clic en el acceso directo" -ForegroundColor White
Write-Host "   2. Moverlo al Escritorio si lo deseas" -ForegroundColor White
Write-Host "   3. Anclarlo a la barra de tareas" -ForegroundColor White
Write-Host ""

# Cleanup
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($WScriptShell) | Out-Null

Write-Host "Presiona Enter para salir..." -ForegroundColor Gray
$null = Read-Host
