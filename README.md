# 🚚 DHL Order Processing System v3.0 - PORTABLE

**Professional Order Management Solution - 100% Portable**  
*Created by Lucas Gnemmi*

---

## 📋 Overview

Sistema profesional de procesamiento de pedidos DHL completamente portable. **No requiere instalación de Python** - todo está empaquetado dentro del sistema.

**Características v3.0 Portable**:
- 📦 **Python 3.13 Empaquetado** - Sin instalación requerida
- 🔌 **100% Portable** - Copia y ejecuta en cualquier Windows
- 📚 **Librerías Incluidas** - pandas, openpyxl, customtkinter, numpy, xlwings
- 🎯 **Launcher Unificado** con 3 opciones: Iniciar, Actualizar, Verificar
- 🔄 **Sistema de Actualización Inteligente** con verificación archivo por archivo
- ✅ **Verificación de Dependencias** - Herramienta integrada
- ✨ Sistema de Gestión de Productos integrado (JSON-based)
- 📅 Gestor de Agenda avanzado con múltiples fechas de entrega
- 📋 Sistema de Reglas Especiales para SKUs con proveedores personalizados
- 🎨 Interfaz moderna Dark Mode con CustomTkinter
- ⚡ Estructura de proyecto organizada y optimizada

## 🚀 Primera Instalación

### 📥 Opción 1: Instalación Automática (RECOMENDADA)

**Para nuevos usuarios que descargan el sistema por primera vez:**

1. **Descargar el código fuente** del repositorio
   - Click en el botón verde "Code" → "Download ZIP"
   - O clona el repositorio: `git clone https://github.com/TU_USUARIO/TU_REPO.git`

2. **Ejecutar el instalador automático**
   ```batch
   Doble clic en: Descargar_Python.bat
   ```
   
   Esto descargará e instalará automáticamente:
   - ✅ Python 3.13 Portable (~50 MB)
   - ✅ Todas las librerías necesarias (~100 MB)
   
3. **¡Listo!** El sistema está configurado y funcional

### 📥 Opción 2: Instalación Manual

**Si prefieres control total o la instalación automática falla:**

1. Ve a la página de [**Releases**](https://github.com/TU_USUARIO/TU_REPO/releases/latest) del repositorio

2. Descarga estos 3 archivos:
   - `Source code (zip)` - Código de la aplicación
   - `python-portable.zip` - Python 3.13 empaquetado
   - `libs-portable.zip` - Librerías Python

3. Extrae `Source code` en una carpeta

4. Extrae `python-portable.zip` en la misma carpeta
   - Debe quedar una carpeta llamada `python/` en la raíz

5. Extrae `libs-portable.zip` en la misma carpeta
   - Debe quedar una carpeta llamada `libs/` en la raíz

6. ¡Listo! Ya puedes usar el sistema

### 📦 ¿Qué incluyen estos archivos?

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| **Source code** | ~2 MB | Tu aplicación y scripts |
| **python-portable.zip** | ~50 MB | Python 3.13 completo |
| **libs-portable.zip** | ~100 MB | pandas, openpyxl, customtkinter, numpy, xlwings, etc. |

---

## 🚀 Inicio Rápido

### ⚡ Ejecución Inmediata (después de instalar)

**Opción 1: Archivo BAT (Recomendado)**
```batch
Doble clic en: EXE_Procesar_Ordenes.bat
```

**Opción 2: PowerShell**
```powershell
Doble clic en: Start_DHL_System.ps1
```

**Opción 3: Launcher Silencioso**
```batch
Doble clic en: Launcher.vbs
```

### ✅ Requisitos del Sistema

**Lo que SÍ necesitas:**
- ✅ Windows 10 o superior (64-bit)
- ✅ 500 MB de espacio en disco
- ✅ 4 GB de RAM (recomendado)

**Lo que NO necesitas:**
- ❌ Python instalado en el sistema
- ❌ Permisos de administrador
- ❌ Instalar librerías con pip
- ❌ Configurar variables de entorno
- ❌ Conexión a internet (para usar, no para actualizar)

### 🔍 Verificar Instalación

Para verificar que todo esté correctamente configurado:

```batch
verificar.bat
```

Esto verificará:
- ✅ Python empaquetado (python/)
- ✅ Librerías instaladas (libs/)
- ✅ Archivos del proyecto
- ✅ Estructura de carpetas

## 📁 Estructura del Proyecto

```
Sys_Procesar_Ordenes/
│
├── � python/                        # Python 3.13 Empaquetado (PORTABLE)
│   ├── python.exe                    # Intérprete Python
│   ├── pythonw.exe                   # Python sin consola
│   ├── python313.dll
│   ├── python313._pth                # Configuración de paths
│   └── Lib/                          # Librería estándar de Python
│
├── 📚 libs/                          # Librerías Empaquetadas
│   ├── customtkinter/                # UI moderna (v5.2.2)
│   ├── pandas/                       # Procesamiento de datos (v2.3.3)
│   ├── numpy/                        # Computación numérica (v2.4.0)
│   ├── openpyxl/                     # Manejo de Excel (v3.1.5)
│   ├── xlwings/                      # Excel avanzado (v0.33.19)
│   ├── pytz/                         # Zonas horarias (v2025.2)
│   ├── dateutil/                     # Manejo de fechas (v2.9.0)
│   └── darkdetect/                   # Detección tema oscuro (v0.8.0)
│
├── 📄 gui_moderna_v2.py              # Aplicación principal
├── 📄 procesamiento_v2.py            # Motor de procesamiento
├── 📄 launcher.py                    # Launcher del sistema
├── 📄 agenda_manager.py              # Gestión de agenda
├── 📄 products_manager.py            # Gestión de productos
├── 📄 rules_manager.py               # Gestión de reglas
│
├── 🎨 agenda_dialog.py               # UI: Diálogo de agenda
├── 🎨 products_dialog.py             # UI: Diálogo de productos
├── 🎨 rules_dialog.py                # UI: Diálogo de reglas
├── 🎨 proveedor_editor.py            # UI: Editor de proveedores
│
├── 📋 agenda_config.json             # Configuración de agenda
├── 📋 products.json                  # Base de datos de productos
├── 📋 rules.json                     # Reglas especiales
│
├── 🚀 EXE_Procesar_Ordenes.bat       # Launcher Windows
├── 🚀 Start_DHL_System.ps1           # Launcher PowerShell
├── 🚀 Launcher.vbs                   # Launcher silencioso
│
├── 🔧 verificar_dependencias.py      # Verificador de sistema
├── 🔧 verificar.bat                  # Ejecutar verificador
├── 🔧 instalar_dependencias.bat      # Instalar librerías
├── 🔧 empaquetar_sistema.py          # Crear paquete portable
├── 🔧 empaquetar.bat                 # Ejecutar empaquetador
│
├── 📁 Ordenes/                       # Input: PDFs de órdenes
├── 📁 Salidas/                       # Output: Excel procesados
├── 📁 Templates/                     # Plantillas Excel
├── 📁 Full-Agenda/                   # Archivos de referencia
├── 📁 docs/                          # Documentación adicional
│   ├── GUIA_EMPAQUETADO.md          # Guía completa de empaquetado
│   ├── PRODUCTOS_README.md          # Documentación de productos
│   └── [más documentación...]
│
├── 📖 README.md                      # Esta guía
├── 📖 LEEME_PORTABLE.md              # Guía de versión portable
├── 📖 SISTEMA_LISTO.md               # Resumen del sistema
│
├── 🎨 dhl_icon.ico                   # Icono de la aplicación
└── 🔒 .gitignore                     # Control de versiones
```

## 🎯 Sistema Portable

### ¿Qué significa "Portable"?

Este sistema está **completamente autocontenido**:
- ✅ Python incluido - no necesita instalación
- ✅ Todas las librerías incluidas
- ✅ Copia la carpeta y funciona inmediatamente
- ✅ Sin dependencias externas
- ✅ Sin permisos de administrador

### Cómo Distribuir

**Para copiar a otro equipo:**
1. Copia toda la carpeta `Sys_Procesar_Ordenes`
2. Pégala en cualquier lugar del nuevo PC
3. Ejecuta `EXE_Procesar_Ordenes.bat`
4. ¡Funciona!

**Para crear un paquete ZIP:**
1. Ejecuta `empaquetar.bat`
2. Se creará un ZIP automáticamente
3. Compártelo por correo, USB, etc.

### Herramientas Incluidas

#### `verificar.bat`
Verifica que el sistema esté correctamente configurado:
- Python empaquetado
- Librerías instaladas
- Archivos del proyecto
- Estructura de carpetas

#### `empaquetar.bat`
Crea un paquete portable listo para distribuir:
- Copia todos los archivos necesarios
- Crea documentación
- Opcionalmente genera ZIP

#### `instalar_dependencias.bat`
Instala o repara librerías en `libs/` si faltara alguna

## ✨ Key Features

### 🎨 Modern Professional Interface
- **Elegant Theme**: Professional deep indigo theme (#1a237e) with modern design
- **Responsive Design**: Optimized 1400x900 window with professional layout
- **Real-time Activity Logging**: Terminal-style log with timestamps
- **Results Preview**: Live preview of processed data
- **Hover Effects**: Interactive buttons with smooth transitions
- **Integrated Managers**: Built-in dialogs for Products, Agenda, and Special Rules

### 📄 Advanced PDF Processing
- **Multi-format Support**: Handles various PDF order formats
- **Intelligent Text Extraction**: Optimized pattern recognition for SKUs and quantities
- **Error Handling**: Robust processing with detailed error reporting
- **Batch Processing**: Process multiple PDFs simultaneously
- **File Size Tracking**: Display file sizes and processing statistics

### 🔍 Smart Validation System
- **SKU Validation**: Cross-reference with integrated Products database (JSON-based)
- **Supplier Mapping**: Automatic supplier assignment from Full.xlsx
- **Special Rules**: Custom supplier assignments for specific SKUs
- **Region Filtering**: Configurable region-based processing (default: 099)
- **Duplicate Detection**: Intelligent consolidation of duplicate orders

### 📅 Advanced Agenda Management
- **Multiple Delivery Dates**: Support for multiple suppliers and delivery dates
- **Date Configuration**: Visual interface to manage delivery schedules
- **Auto-detection**: Automatic SKU-to-supplier mapping
- **Export/Import**: Save and load agenda configurations (JSON)

### 📦 Integrated Product Management
- **JSON-based Database**: Modern replacement for Items.xlsx
- **Real-time Search**: Filter products by SKU or description
- **Bulk Import**: Import from Excel files (auto-detects columns)
- **Export Capability**: Export product catalog to Excel
- **Visual Editor**: Add, edit, and delete products with intuitive interface

### 📋 Special Rules System
- **Custom Supplier Mapping**: Override default supplier for specific SKUs
- **Visual Management**: Dedicated dialog to manage special rules
- **Import/Export**: Save configurations in JSON format

### 📊 Professional Excel Output
- **Dynamic Naming**: Automatic filename based on agenda dates
- **Corporate Formatting**: Professional styling with DHL branding
- **Multi-sheet Reports**: Separate sheets for valid orders and errors
- **Optimized Layouts**: Column widths and formatting for readability

## 🛠 Technical Specifications

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (optimized for PowerShell)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 100MB free space for application and temporary files

### Dependencies
```
pandas>=1.3.0
openpyxl>=3.0.0
PyMuPDF>=1.18.0
xlwings>=0.24.0
tkinter (included with Python)
```

### File Structure
```
📁 DHL Order Processing System/
├── 📄 gui_moderna_v2.py          # Main GUI application
├── 📄 procesamiento_v2.py        # Optimized processing module
├── 📄 products_manager.py        # Product database manager
├── 📄 products_dialog.py         # Product management UI
├── 📄 agenda_manager.py          # Agenda configuration manager
├── 📄 agenda_dialog.py           # Agenda management UI
├── 📄 rules_manager.py           # Special rules manager
├── 📄 rules_dialog.py            # Special rules UI
├── 📄 proveedor_editor.py        # Supplier editor component
├── 📄 config.py                  # Configuration settings
├── 📄 products.json              # Products database
├── 📄 agenda_config.json         # Agenda configurations
├── 📄 rules.json                 # Special rules configurations
├── 📄 README.md                  # This documentation
├── 📄 PRODUCTOS_README.md        # Products system documentation
├── 📄 MEJORAS_AGENDA.md          # Agenda improvements documentation
├── 📁 Ordenes/                   # PDF input folder
├── 📁 Full-Agenda/              # Excel configuration files
│   └── 📊 Full.xlsx             # Supplier database
└── 📁 Salidas/                  # Output folder for processed files
```

## 🚀 Quick Start Guide

### 1. Installation
1. Ensure Python 3.8+ is installed
2. Install required dependencies:
   ```bash
   pip install pandas openpyxl PyMuPDF xlwings
   ```
3. Download all application files to your working directory

### 2. Configuration
1. Place your Excel configuration files in `Full-Agenda/` folder:
   - `Full.xlsx`: Supplier database with region mapping
2. Configure your products database:
   - Use the built-in Product Manager (🔧 Tools menu)
   - Or import from Excel files
3. Set up your agenda:
   - Use the built-in Agenda Manager (🔧 Tools menu)
   - Configure delivery dates for each supplier
4. Optional: Define special rules for specific SKUs (🔧 Tools menu)

### 3. Running the Application
```bash
python gui_moderna_v2.py
```

### 4. Processing Workflow
1. **Configure Tools**: Access 🔧 Tools menu to set up:
   - Products database (replaces Items.xlsx)
   - Agenda with delivery dates
   - Special rules for SKUs (optional)
2. **Add PDF Files**: Click "➕ Add PDFs" to upload order files
3. **Open Configuration**: Use step 1 to open Full.xlsx
4. **Set Region**: Configure target region (default: 099)
5. **Process Orders**: Click "🚀 PROCESS ORDERS" to start automated processing
6. **Review Results**: Check the activity log and results preview
7. **Access Output**: Use "📁 Open Output Folder" to view generated files

## 📖 Detailed Usage

### PDF Processing
The system automatically extracts:
- **SKU Codes**: Product codes starting with 'A' followed by 4-6 digits
- **Quantities**: Numeric values with support for European format (1.234,56)
- **Center Codes**: 3-6 digit location identifiers
- **Location Names**: Destination facility names

### Validation Process
1. **SKU Verification**: Checks against Items.xlsx for valid C.Calzada items
2. **Supplier Mapping**: Matches SKUs to suppliers from Full.xlsx
3. **Region Filtering**: Applies region-specific supplier assignments
4. **Date Processing**: Extracts delivery dates from Agenda.xlsm cell M1

### Output Generation
- **Main Report**: `PEDIDOS_CD_OVIEDO_DD-MM-YYYY.xlsx`
  - Sheet 1: "PEDIDOS_CD" - Valid processed orders
  - Sheet 2: "Errors" - Items requiring manual review
- **Professional Formatting**: Corporate colors, optimized column widths
- **ID Assignment**: Automatic order ID generation grouped by supplier/observation

## 🔧 Advanced Configuration

### Region Settings
Modify the region filter in the GUI or directly in the code:
```python
region_seleccionada = "099"  # Change to your target region
```

### Custom File Paths
Update paths in `setup_paths()` method for custom folder structures:
```python
self.ORDENES_DIR = "custom/orders/path"
self.AGENDA_XLSM = "custom/agenda/path.xlsm"
```

### Excel Template Customization
The system supports various Excel formats. Key requirements:
- **products.json**: JSON database with SKU and description fields (replaces Items.xlsx)
- **Full.xlsx**: Requires supplier and SKU columns
- **agenda_config.json**: Delivery dates configuration per supplier
- **rules.json**: Special rules for SKU-to-supplier overrides

## 🔧 Integrated Management Tools

### 📦 Product Manager
Access via 🔧 Tools → "Manage Products"
- **Add Products**: Enter SKU and description
- **Search/Filter**: Real-time search by SKU or description
- **Bulk Import**: Import from Excel files (auto-detects columns)
- **Export**: Generate Excel file with all products
- **Statistics**: View total products and last update date

### 📅 Agenda Manager
Access via 🔧 Tools → "Manage Agenda"
- **Configure Dates**: Set delivery dates for each supplier
- **Multiple Suppliers**: Support for multiple suppliers and dates
- **Visual Interface**: Easy-to-use calendar and date pickers
- **Export/Import**: Save and load agenda configurations

### 📋 Special Rules Manager
Access via 🔧 Tools → "Manage Special Rules"
- **Custom Mappings**: Override default supplier for specific SKUs
- **Visual Editor**: Add, edit, and delete rules with intuitive interface
- **Bulk Operations**: Import rules from Excel templates
- **Export**: Save rules to JSON format

## � Sistema de Actualización Inteligente

### Características Principales

El sistema incluye un sistema de actualización automática que verifica **archivo por archivo** contra GitHub:

- ✅ **Verificación Completa**: Compara todos los archivos del proyecto con GitHub
- 🔒 **Protección Inteligente**: Bloquea actualizaciones si ya tienes la última versión
- 📊 **Reporte Detallado**: Muestra exactamente qué archivos han cambiado
- 🔐 **Respaldo Automático**: Guarda configuraciones locales antes de actualizar
- 📝 **Registro Completo**: Log detallado de todas las operaciones

### Métodos de Actualización

#### 1. Desde el Launcher Principal
```bash
# Ejecutar el launcher
EXE_Procesar_Ordenes.bat
# o
.\Start_DHL_System.ps1

# Seleccionar opción: ⟳ ACTUALIZAR SISTEMA
```

#### 2. Script de Actualización Directo
```bash
# Ejecutar el actualizador
.\Actualizar.bat
# o
.\Actualizar_Sistema.ps1

# Menú de opciones:
# [1] Verificar actualizaciones disponibles
# [2] Actualizar a la última versión
# [3] Verificar y reparar archivos
# [4] Ver información del sistema
```

#### 3. Verificación Rápida
```bash
# Solo verificar si hay actualizaciones
.\Verificar_Actualizacion.ps1

# Códigos de salida:
# 0 = Sistema actualizado
# 2 = Actualización disponible
# 1 = Error
```

### Funcionamiento del Sistema

#### Verificación de Actualizaciones
Cuando ejecutas la verificación, el sistema:

1. **Conecta con GitHub** para obtener la última versión
2. **Compara commit por commit** entre local y remoto
3. **Analiza cada archivo** para detectar cambios:
   - 📝 **Modificados**: Archivos que cambiaron
   - ➕ **Agregados**: Archivos nuevos en GitHub
   - ➖ **Eliminados**: Archivos removidos
4. **Muestra estadísticas detalladas**:
   ```
   VERIFICACIÓN DE ARCHIVOS DEL PROYECTO
   ================================================
   
   ⚠ HAY UNA NUEVA VERSIÓN DISPONIBLE
   
   ARCHIVOS MODIFICADOS:
     [M] gui_moderna_v2.py
     [M] procesamiento_v2.py
   
   ARCHIVOS NUEVOS:
     [+] nueva_funcionalidad.py
   
   CAMBIOS RECIENTES:
     • Mejora en sistema de validación
     • Corrección de bugs en exportación
   
   RESUMEN: 3 archivo(s) con cambios
   ```

#### Proceso de Actualización

Si hay actualizaciones disponibles:

1. **Pre-verificación**:
   - ✅ Verifica conexión a Internet
   - ✅ Confirma que Git está instalado
   - ✅ Valida que es un repositorio Git válido

2. **Respaldo Automático**:
   - Guarda archivos de configuración locales:
     - `agenda_config.json`
     - `rules.json`
     - `products.json`

3. **Descarga de GitHub**:
   - Obtiene la última versión de todos los archivos
   - Actualiza código, scripts y dependencias

4. **Restauración**:
   - Restaura tus configuraciones locales
   - Mantiene tus datos personalizados intactos

5. **Verificación Post-Actualización**:
   - Confirma que la actualización fue exitosa
   - Muestra versión instalada y archivos actualizados

#### Protección contra Actualizaciones Innecesarias

Si ya tienes la última versión:

```
================================================
 NO SE PUEDE ACTUALIZAR
================================================

✓ Ya tienes la última versión
✓ Todos los archivos están actualizados

Actualización cancelada - Sistema ya está al día
```

El sistema **BLOQUEA** la actualización para evitar:
- Descargas innecesarias
- Pérdida de tiempo
- Riesgo de sobrescribir archivos sin cambios

### Archivos Protegidos

Estos archivos **NUNCA** se sobrescriben durante actualizaciones:
- `agenda_config.json` - Tu configuración de agenda
- `rules.json` - Tus reglas especiales personalizadas
- `products.json` - Tu base de datos de productos
- Archivos en `Ordenes/` y `Salidas/` - Tus datos de trabajo

### Requisitos

Para usar el sistema de actualización necesitas:
- **Git**: Instalado en el sistema ([Descargar](https://git-scm.com/download/win))
- **Internet**: Conexión activa para consultar GitHub
- **Permisos**: Derechos de escritura en la carpeta del proyecto

### Solución de Problemas

#### "Git no está instalado"
- Descarga e instala Git desde: https://git-scm.com/download/win
- Reinicia PowerShell después de instalar

#### "No es un repositorio Git válido"
- Descarga el proyecto completo desde GitHub
- No uses archivos parciales o copias manuales

#### "No hay conexión a Internet"
- Verifica tu conexión de red
- Intenta nuevamente cuando tengas acceso

#### Error durante la actualización
- El sistema automáticamente restaura respaldos
- Si persiste, descarga el proyecto completo desde:
  ```
  https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes.git
  ```

### Logs de Actualización

Todas las operaciones se registran en:
```
actualizacion.log
```

Ejemplo de log:
```
[2024-12-29 14:30:15] === Inicio del sistema de actualización ===
[2024-12-29 14:30:16] Verificando actualizaciones disponibles...
[2024-12-29 14:30:18] Actualización disponible - Local: abc1234, Remoto: def5678
[2024-12-29 14:30:18]   Modificado: gui_moderna_v2.py
[2024-12-29 14:30:18] Total de archivos con cambios: 3
```

---

## �🐛 Troubleshooting

### Common Issues

**Issue**: "File not found" errors
- **Solution**: Verify all Excel files are in the `Full-Agenda/` folder
- **Check**: File permissions and path accessibility

**Issue**: PDF processing fails
- **Solution**: Ensure PDFs contain readable text (not scanned images)
- **Check**: File format and text extraction capability

**Issue**: Excel formatting errors
- **Solution**: Close any open Excel files before processing
- **Check**: Excel application isn't locked by other processes

**Issue**: Xlwings connection problems
- **Solution**: Ensure Excel is properly installed and accessible
- **Alternative**: Use fallback processing mode

### Debug Mode
Enable detailed logging by modifying the log level:
```python
# In procesamiento_v2.py
def log_processing_step(step_name, status="DEBUG", details=""):
```

## 📊 Performance Optimization

### Processing Speed
- **PDF Batch Size**: Optimal for 10-50 PDFs per batch
- **Memory Usage**: ~50MB base + 1MB per PDF
- **Processing Time**: ~2-5 seconds per PDF file

### Excel Performance
- **File Size Limits**: Up to 100,000 rows supported
- **Sheet Optimization**: Automatic column width adjustment
- **Format Caching**: Reduced formatting overhead

## 🔐 Security & Data Protection

### Data Handling
- **Local Processing**: All data remains on local machine
- **No External Connections**: No internet required for core functionality
- **Temporary Files**: Automatic cleanup of processing artifacts
- **Error Logging**: Sensitive data excluded from logs

### File Safety
- **Backup Creation**: Original files remain unchanged
- **Error Recovery**: Graceful handling of processing failures
- **Validation Checks**: Input data integrity verification

## 🆕 Version History

### v2.5 (Current) - Advanced Integration Release
- ✨ Sistema de Gestión de Productos (JSON-based, replaces Items.xlsx)
- 📅 Gestor de Agenda avanzado con soporte multi-fecha
- 📋 Sistema de Reglas Especiales para mapeos personalizados
- 🎨 Nuevo tema elegante azul índigo (#1a237e)
- 🔧 Menú de herramientas integrado con 3 gestores
- 📊 Mejoras en la interfaz de usuario y usabilidad
- ⚡ Optimizaciones de rendimiento y estabilidad
- 💻 Created by Lucas Gnemmi

### v2.0 - Professional Release
- ✨ Complete UI redesign with DHL corporate branding
- 🚀 Optimized processing engine with 50% performance improvement
- 📊 Enhanced Excel formatting with professional layouts
- 🔍 Advanced error handling and validation
- 📝 Comprehensive logging and debugging tools
- 💻 Created by Lucas Gnemmi

### v1.0 - Initial Release
- Basic PDF processing functionality
- Simple GUI interface
- Excel output generation

## 👨‍💻 Developer Information

**Created by**: Lucas Gnemmi  
**Version**: 2.5  
**Last Updated**: December 2025  
**Language**: Python 3.8+  
**Framework**: Tkinter GUI + Pandas + OpenPyXL

### Architecture
- **Modern JSON-based storage**: Products, Agenda, and Rules stored in JSON format
- **Modular design**: Separate managers for each functionality
- **Event-driven GUI**: Responsive interface with real-time updates
- **Professional theme**: Elegant indigo design with modern components

### Contributing
This is a professional solution developed by Lucas Gnemmi. For feature requests or issues, please contact the developer directly.

### License
Copyright © 2025 Lucas Gnemmi. All rights reserved.  
Professional business solution - unauthorized reproduction prohibited.

---

## 📞 Support

For technical support, feature requests, or customization services, please contact:

**Lucas Gnemmi**  
Professional Software Developer  
Specialized in Business Process Automation

---

*🚚 DHL Order Processing System v2.5 - Streamlining logistics with professional excellence*

---

## 📚 Additional Documentation

- [PRODUCTOS_README.md](PRODUCTOS_README.md) - Complete Product Management System guide
- [MEJORAS_AGENDA.md](MEJORAS_AGENDA.md) - Agenda System improvements and features
- [PRODUCTOS_IMPLEMENTACION_COMPLETA.md](PRODUCTOS_IMPLEMENTACION_COMPLETA.md) - Technical implementation details