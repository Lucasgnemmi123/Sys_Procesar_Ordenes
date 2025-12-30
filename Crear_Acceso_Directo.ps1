$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VbsFile = Join-Path $ScriptDir "Iniciar_Sistema.vbs"
$IconFile = Join-Path $ScriptDir "launcher_icon.ico"
# CREAR EN EL DIRECTORIO DE LA APP, no en el escritorio
$ShortcutPath = Join-Path $ScriptDir "Sistema Procesar Pedidos.lnk"

Write-Host "Creando acceso directo en el directorio de la app..." -ForegroundColor Cyan

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $VbsFile
$Shortcut.WorkingDirectory = $ScriptDir
$Shortcut.Description = "Sistema de Procesamiento de Pedidos v3.0"
$Shortcut.WindowStyle = 1
if (Test-Path $IconFile) { $Shortcut.IconLocation = $IconFile }
$Shortcut.Save()

Write-Host ""
Write-Host "Acceso directo creado exitosamente!" -ForegroundColor Green
Write-Host "Ubicacion: $ShortcutPath" -ForegroundColor White
Write-Host ""
Write-Host "Ahora puedes copiar este acceso directo al escritorio o donde quieras" -ForegroundColor Yellow
Write-Host ""
Start-Process "explorer.exe" $ScriptDir
