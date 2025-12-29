# 🎯 GUÍA COMPLETA DE EMPAQUETADO - Sistema DHL v3.0

## ✅ Estado Actual del Sistema

Tu sistema **YA ESTÁ CONFIGURADO** para ser completamente portable con:

- ✅ **Python 3.13** empaquetado en `python/`
- ✅ **Librerías** en `libs/`
- ✅ **Scripts de arranque** actualizados para usar Python empaquetado
- ✅ **Sin dependencias externas**

---

## 📦 ¿QUÉ SE HA CONFIGURADO?

### 1. **Python Empaquetado** (`python/`)
- Contiene Python 3.13 completo y portable
- Archivo `python313._pth` configurado para usar `libs/`
- No requiere instalación en el sistema

### 2. **Librerías Empaquetadas** (`libs/`)
- Todas las dependencias necesarias:
  - pandas
  - openpyxl
  - customtkinter
  - numpy
  - xlwings
  - pytz
  - python-dateutil
  - darkdetect

### 3. **Scripts de Arranque Actualizados**

#### ✅ `EXE_Procesar_Ordenes.bat`
```batch
Usa: python\python.exe launcher.py
```

#### ✅ `Start_DHL_System.ps1`
```powershell
Usa: python\python.exe gui_moderna_v2.py
```

#### ✅ `Launcher.vbs`
```vbscript
Usa: python\pythonw.exe launcher.py
```

### 4. **Scripts de Utilidad**

#### ✅ `verificar_dependencias.py` / `verificar.bat`
Verifica que todo esté correctamente instalado:
- Python empaquetado
- Librerías en libs/
- Archivos del proyecto
- Estructura de carpetas

#### ✅ `instalar_dependencias.bat`
Instala todas las librerías en `libs/` si faltara alguna

#### ✅ `empaquetar_sistema.py` / `empaquetar.bat`
Crea un paquete portable completo listo para distribuir

---

## 🚀 CÓMO USAR EL SISTEMA

### Opción 1: Ejecución Normal
```batch
Doble clic en: EXE_Procesar_Ordenes.bat
```

### Opción 2: PowerShell
```batch
Doble clic en: Start_DHL_System.ps1
```

### Opción 3: Launcher Silencioso
```batch
Doble clic en: Launcher.vbs
```

---

## 🔍 VERIFICAR QUE TODO ESTÉ BIEN

### Paso 1: Ejecutar Verificador
```batch
Doble clic en: verificar.bat
```

O desde CMD:
```cmd
python\python.exe verificar_dependencias.py
```

### Paso 2: Revisar Resultados
El verificador te mostrará:
- ✅ Python empaquetado encontrado
- ✅ Carpeta libs/ con todas las librerías
- ✅ Todos los archivos del proyecto
- ✅ Estructura de carpetas correcta

---

## 📦 CÓMO EMPAQUETAR PARA DISTRIBUIR

### Opción 1: Usar Script Automático (Recomendado)

```batch
Doble clic en: empaquetar.bat
```

Esto creará:
1. Carpeta `Sistema_DHL_Portable/` con todo lo necesario
2. Opcionalmente, un archivo `.zip` para distribuir

### Opción 2: Empaquetar Manualmente

1. **Crea una carpeta nueva** (ej: `Sistema_DHL_Portable`)

2. **Copia estas carpetas:**
   - `python/` (completa)
   - `libs/` (completa)
   - `Ordenes/`
   - `Salidas/`
   - `Templates/`
   - `docs/`

3. **Copia estos archivos:**
   - `*.py` (todos los archivos Python)
   - `*.json` (configuraciones)
   - `*.bat` (scripts de arranque)
   - `*.ps1` (scripts PowerShell)
   - `*.vbs` (launcher)
   - `*.md` (documentación)

4. **Comprime en ZIP** (opcional)

---

## 🚚 CÓMO DISTRIBUIR A OTRO EQUIPO

### Método 1: Carpeta Completa
1. Copia toda la carpeta del sistema a USB/Red
2. Pega en el equipo destino
3. Ejecuta `EXE_Procesar_Ordenes.bat`
4. ¡Listo!

### Método 2: Archivo ZIP
1. Ejecuta `empaquetar.bat` y genera el ZIP
2. Envía el archivo ZIP (por correo, USB, etc.)
3. En el equipo destino, descomprime el ZIP
4. Ejecuta `EXE_Procesar_Ordenes.bat`
5. ¡Listo!

---

## ⚠️ IMPORTANTE: LO QUE DEBE INCLUIRSE

### ✅ SIEMPRE INCLUIR:
- ✅ Carpeta `python/` **COMPLETA** (con python.exe)
- ✅ Carpeta `libs/` **COMPLETA** (con todas las librerías)
- ✅ Todos los archivos `.py`
- ✅ Todos los archivos `.json`
- ✅ Scripts `.bat`, `.ps1`, `.vbs`
- ✅ Carpetas `Ordenes/`, `Salidas/`, `Templates/`

### ❌ NO INCLUIR (opcional):
- ❌ `__pycache__/` (se regenera automáticamente)
- ❌ Archivos temporales `.pyc`
- ❌ `.git/` (si existe)

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "Python no encontrado"
**Causa:** Falta la carpeta `python/` o el archivo `python.exe`

**Solución:**
1. Verifica que existe `python\python.exe`
2. Si no existe, descarga Python embebido desde:
   https://www.python.org/downloads/windows/
3. Busca "Windows embeddable package (64-bit)"
4. Descomprime en la carpeta `python/`

### Error: "ModuleNotFoundError"
**Causa:** Falta alguna librería en `libs/`

**Solución:**
```batch
instalar_dependencias.bat
```

Esto instalará todas las librerías necesarias en `libs/`

### Error: "No se puede abrir el archivo"
**Causa:** Permisos o ruta incorrecta

**Solución:**
1. Ejecuta como Administrador
2. Verifica que la ruta no tenga caracteres especiales
3. Mueve la carpeta a `C:\Sistema_DHL\`

---

## 📋 CHECKLIST PRE-DISTRIBUCIÓN

Antes de distribuir, verifica:

- [ ] Ejecutar `verificar.bat` - todo OK
- [ ] Probar `EXE_Procesar_Ordenes.bat` - arranca correctamente
- [ ] Carpeta `python/` presente con `python.exe`
- [ ] Carpeta `libs/` presente con todas las librerías
- [ ] Archivos `.json` de configuración presentes
- [ ] Carpetas `Ordenes/`, `Salidas/`, `Templates/` creadas
- [ ] Documentación `README.md` y `LEEME_PORTABLE.md` incluida

---

## 🎯 COMANDOS ÚTILES

### Verificar Python empaquetado:
```cmd
python\python.exe --version
```

### Verificar librería específica:
```cmd
python\python.exe -c "import pandas; print(pandas.__version__)"
```

### Listar todas las librerías instaladas:
```cmd
python\python.exe -m pip list
```

### Instalar librería específica en libs/:
```cmd
python\python.exe -m pip install --target=libs nombre_libreria
```

---

## 💡 MEJORES PRÁCTICAS

### 1. **Mantén la Estructura**
No muevas archivos entre carpetas. La estructura debe permanecer así:
```
Sistema_DHL/
├── python/
├── libs/
├── Ordenes/
├── Salidas/
├── Templates/
└── (archivos .py, .bat, .json, etc.)
```

### 2. **Actualiza las Librerías**
Si necesitas actualizar una librería:
```cmd
python\python.exe -m pip install --upgrade --target=libs nombre_libreria
```

### 3. **Backup Regular**
Crea backups periódicos de:
- `rules.json`
- `products.json`
- `agenda_config.json`

### 4. **Documenta Cambios**
Si modificas el sistema, actualiza:
- `README.md`
- `LEEME_PORTABLE.md`

---

## 🔐 SEGURIDAD

### Archivos Sensibles
Si tu sistema tiene datos sensibles:
1. **No incluyas** archivos con datos reales en la distribución
2. Crea plantillas vacías para `rules.json`, `products.json`
3. Documenta cómo configurar estos archivos

### Permisos
El sistema NO requiere:
- ❌ Permisos de Administrador
- ❌ Instalación en Program Files
- ❌ Modificación del registro de Windows
- ❌ Variables de entorno

---

## 📞 SOPORTE Y AYUDA

### Recursos Incluidos:
- `README.md` - Documentación técnica completa
- `LEEME_PORTABLE.md` - Guía de portabilidad
- `docs/` - Documentación adicional

### Herramientas de Diagnóstico:
- `verificar_dependencias.py` - Verifica instalación
- `instalar_dependencias.bat` - Repara librerías
- `empaquetar_sistema.py` - Crea paquete de distribución

---

## 🎉 CONCLUSIÓN

Tu sistema está **100% LISTO** para ser distribuido de forma portable.

**Pasos Finales:**
1. ✅ Ejecuta `verificar.bat` para confirmar
2. ✅ Ejecuta `empaquetar.bat` para crear paquete
3. ✅ Distribuye la carpeta/ZIP resultante
4. ✅ El sistema funcionará en cualquier PC Windows sin instalación

**¡Éxito con la distribución!** 🚀

---

**Creado por Lucas Gnemmi**  
**Sistema DHL v3.0 - Versión Portable**  
**Última actualización: Diciembre 2025**
