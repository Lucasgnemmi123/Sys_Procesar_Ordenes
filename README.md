# 🚚 DHL Order Processing System v2.5

**Professional Order Management Solution**  
*Created by Lucas Gnemmi*

---

## 📋 Overview

The DHL Order Processing System is a comprehensive solution designed to automate and streamline the processing of DHL orders. This professional-grade application features a modern graphical interface built with Python Tkinter and optimized processing algorithms for handling PDF order files, SKU validation, supplier mapping, and Excel report generation.

**Latest Updates (v2.5)**:
- ✨ Sistema de Gestión de Productos integrado (JSON-based)
- 📅 Gestor de Agenda avanzado con múltiples fechas de entrega
- 📋 Sistema de Reglas Especiales para SKUs con proveedores personalizados
- 🎨 Interfaz moderna con tema azul índigo elegante
- ⚡ Mejoras de rendimiento y usabilidad

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

## 🐛 Troubleshooting

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