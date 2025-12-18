# DHL Order Processing System v2.0 - PowerShell Launcher
# Created by Lucas Gnemmi

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "   DHL Order Processing System v2.0" -ForegroundColor Yellow
Write-Host "   Created by Lucas Gnemmi" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green
Write-Host ""

python gui_moderna_v2.py

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
[Console]::ReadKey()
