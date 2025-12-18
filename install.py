"""
DHL Order Processing System - Installation & Setup Script
Created by Lucas Gnemmi
Version: 2.0

Script de instalación automática para configurar el entorno del sistema.
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    """Mostrar encabezado del instalador"""
    print("=" * 80)
    print("🚚 DHL ORDER PROCESSING SYSTEM v2.0")
    print("💻 Installation & Setup Script")
    print("👨‍💻 Created by Lucas Gnemmi")
    print("=" * 80)
    print()

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        print("📥 Please download Python 3.8 or higher from https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Instalar dependencias requeridas"""
    print("\n📦 Installing required dependencies...")
    
    dependencies = [
        "pandas>=1.3.0",
        "openpyxl>=3.0.0", 
        "PyMuPDF>=1.18.0",
        "xlwings>=0.24.0"
    ]
    
    for dep in dependencies:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True, text=True)
            print(f"   ✅ {dep} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error installing {dep}: {e}")
            return False
    
    print("✅ All dependencies installed successfully")
    return True

def create_directory_structure():
    """Crear estructura de directorios"""
    print("\n📁 Creating directory structure...")
    
    directories = [
        "Ordenes",
        "Full-Agenda", 
        "Salidas"
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created: {directory}/")
        else:
            print(f"   ℹ️ Already exists: {directory}/")
    
    print("✅ Directory structure ready")
    return True

def create_sample_files():
    """Crear archivos de ejemplo si no existen"""
    print("\n📄 Setting up configuration files...")
    
    # Crear archivo de configuración de ejemplo
    config_content = """# DHL Order Processing System - Configuration
# Created by Lucas Gnemmi

# Default Settings
DEFAULT_REGION = "099"
DEFAULT_LOCAL = "00000"

# File Paths (relative to application directory)
ORDENES_DIR = "Ordenes"
FULL_AGENDA_DIR = "Full-Agenda"
SALIDAS_DIR = "Salidas"

# Excel Files
AGENDA_FILE = "Agenda.xlsm"
FULL_FILE = "Full.xlsx"
ITEMS_FILE = "Items.xlsx"

# Processing Options
CONSOLIDATE_DUPLICATES = True
AUTO_BACKUP = True
ENABLE_LOGGING = True

# UI Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
THEME = "DHL_CORPORATE"
"""
    
    config_path = Path("config.py")
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("   ✅ Created: config.py")
    else:
        print("   ℹ️ Already exists: config.py")
    
    # Crear archivo README para Full-Agenda
    readme_content = """# 📁 Full-Agenda Folder

This folder contains the Excel configuration files required for the DHL Order Processing System.

## Required Files:

### 📊 Agenda.xlsm
- **Purpose**: Contains delivery schedules and supplier-specific observations
- **Key Cell**: M1 (delivery date)
- **Format**: Excel Macro-Enabled Workbook

### 📊 Full.xlsx
- **Purpose**: Master supplier database with SKU mappings
- **Required Columns**: SKU/Code, Supplier/Proveedor, Region (optional)
- **Format**: Excel Workbook

### 📊 Items.xlsx
- **Purpose**: Valid SKU catalog for C.Calzada items
- **Required Columns**: SKU/Code column
- **Format**: Excel Workbook

## Setup Instructions:

1. Place your actual files in this folder
2. Ensure column names match expected formats
3. Verify data integrity before processing

## Notes:
- Files are automatically detected by the system
- Backup your original files before processing
- Contact Lucas Gnemmi for customization needs

---
Created by Lucas Gnemmi - DHL Order Processing System v2.0
"""
    
    readme_path = Path("Full-Agenda/README.txt")
    if not readme_path.exists():
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("   ✅ Created: Full-Agenda/README.txt")
    
    print("✅ Configuration files ready")
    return True

def create_startup_script():
    """Crear script de inicio rápido"""
    print("\n🚀 Creating startup script...")
    
    # Script para Windows
    bat_content = """@echo off
echo.
echo ========================================
echo   DHL Order Processing System v2.0
echo   Created by Lucas Gnemmi
echo ========================================
echo.
echo Starting application...
echo.

python gui_moderna_v2.py

pause
"""
    
    bat_path = Path("Start_DHL_System.bat")
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    print("   ✅ Created: Start_DHL_System.bat")
    
    # Script para PowerShell
    ps1_content = """# DHL Order Processing System v2.0 - PowerShell Launcher
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
"""
    
    ps1_path = Path("Start_DHL_System.ps1")
    with open(ps1_path, 'w', encoding='utf-8') as f:
        f.write(ps1_content)
    print("   ✅ Created: Start_DHL_System.ps1")
    
    print("✅ Startup scripts ready")
    return True

def verify_installation():
    """Verificar instalación"""
    print("\n🔍 Verifying installation...")
    
    # Verificar archivos principales
    required_files = [
        "gui_moderna_v2.py",
        "procesamiento_v2.py",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"   ✅ Found: {file}")
    
    if missing_files:
        print(f"   ❌ Missing files: {missing_files}")
        return False
    
    # Verificar directorios
    required_dirs = ["Ordenes", "Full-Agenda", "Salidas"]
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"   ✅ Directory: {directory}/")
        else:
            print(f"   ❌ Missing directory: {directory}/")
            return False
    
    # Test de importación
    try:
        print("   🧪 Testing module imports...")
        import pandas
        import openpyxl
        import fitz
        import xlwings
        print("   ✅ All modules import successfully")
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    
    print("✅ Installation verification completed")
    return True

def print_completion_message():
    """Mostrar mensaje de completado"""
    print("\n" + "=" * 80)
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("📋 Next Steps:")
    print("   1. Place your Excel files in the Full-Agenda/ folder:")
    print("      • Agenda.xlsm (delivery schedules)")
    print("      • Full.xlsx (supplier database)")
    print("      • Items.xlsx (valid SKU catalog)")
    print()
    print("   2. Add PDF order files to the Ordenes/ folder")
    print()
    print("   3. Start the application:")
    print("      • Double-click: Start_DHL_System.bat")
    print("      • Or run: python gui_moderna_v2.py")
    print()
    print("📖 Documentation:")
    print("   • Read README.md for detailed usage instructions")
    print("   • Check Full-Agenda/README.txt for file format requirements")
    print()
    print("👨‍💻 Created by Lucas Gnemmi")
    print("🚚 DHL Order Processing System v2.0")
    print("=" * 80)

def main():
    """Función principal de instalación"""
    print_header()
    
    success = True
    
    # Verificar Python
    if not check_python_version():
        success = False
    
    # Instalar dependencias
    if success and not install_dependencies():
        success = False
    
    # Crear estructura de directorios
    if success and not create_directory_structure():
        success = False
    
    # Crear archivos de configuración
    if success and not create_sample_files():
        success = False
    
    # Crear scripts de inicio
    if success and not create_startup_script():
        success = False
    
    # Verificar instalación
    if success and not verify_installation():
        success = False
    
    if success:
        print_completion_message()
    else:
        print("\n❌ Installation encountered errors. Please check the messages above.")
        print("💡 Contact Lucas Gnemmi for technical support.")

if __name__ == "__main__":
    main()