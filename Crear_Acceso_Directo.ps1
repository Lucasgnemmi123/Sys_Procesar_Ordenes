$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VbsFile = Join-Path $ScriptDir "Iniciar_Sistema.vbs"
$IconFile = Join-Path $ScriptDir "launcher_icon.ico"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "Sistema Procesar Pedidos.lnk"

Write-Host "Creando acceso directo en el escritorio..." -ForegroundColor Cyan   

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $VbsFile
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "Sistema de Procesamiento de Pedidos v3.0"
$Shortcut.WindowStyle = 1
if (Test-Path $IconFile) { 
    $Shortcut.IconLocation = $IconFile
    Write-Host "[OK] Icono aplicado" -ForegroundColor Green
}
$Shortcut.Save()

Write-Host ""
Write-Host "Acceso directo creado exitosamente!" -ForegroundColor Green
Write-Host "Ubicacion: $ShortcutPath" -ForegroundColor White
Write-Host ""
