# 📋 Checklist de Distribución - Sistema DHL

## ✅ Pasos para Compartir el Sistema en GitHub

### Paso 1: Preparar los Archivos (en tu PC)

1. **Comprimir Python y Librerías**
   ```batch
   Ejecutar: Preparar_Release.bat
   ```
   
   Esto creará:
   - `Release/python-portable.zip` (~50 MB)
   - `Release/libs-portable.zip` (~100 MB)
   
   ⏱️ Tiempo estimado: 3-5 minutos

---

### Paso 2: Subir Código a GitHub

1. **Asegurar que .gitignore está correcto**
   - ✅ Ya configurado para excluir `python/` y `libs/`
   
2. **Hacer commit y push**
   ```bash
   git add .
   git commit -m "Sistema DHL v3.0 - Portable con instalador automático"
   git push origin main
   ```

---

### Paso 3: Crear GitHub Release

1. **Ir a tu repositorio en GitHub**
   - URL: `https://github.com/TU_USUARIO/TU_REPO`

2. **Click en "Releases"** (lado derecho de la página)

3. **Click en "Create a new release"**

4. **Configurar el Release:**
   
   **Tag version:** `v3.0.0`
   
   **Release title:** `DHL Order Processing System v3.0.0 - Portable`
   
   **Description:**
   ```markdown
   ## 🚀 Sistema Completo de Procesamiento de Pedidos DHL
   
   Versión portable con Python incluido - No requiere instalación previa.
   
   ### 📦 ¿Qué incluye esta versión?
   
   - ✅ Python 3.13 portable empaquetado
   - ✅ Todas las librerías necesarias (pandas, openpyxl, customtkinter, etc.)
   - ✅ Instalador automático con 1 click
   - ✅ Sistema de actualización inteligente
   - ✅ Gestión de productos y agenda
   - ✅ Interfaz moderna con Dark Mode
   
   ### 🚀 Instalación Rápida (Recomendada)
   
   1. Descarga el **Source code (zip)**
   2. Extrae en cualquier carpeta
   3. Ejecuta `Descargar_Python.bat`
   4. ¡Listo! Usa `EXE_Procesar_Ordenes.bat`
   
   ### 🔧 Instalación Manual
   
   Si prefieres control total:
   
   1. Descarga estos 3 archivos:
      - Source code (zip)
      - python-portable.zip
      - libs-portable.zip
   
   2. Extrae todo en la misma carpeta
   
   3. Ejecuta `EXE_Procesar_Ordenes.bat`
   
   ### 📊 Tamaños de Descarga
   
   | Archivo | Tamaño | Descripción |
   |---------|--------|-------------|
   | Source code | ~2 MB | Código de la aplicación |
   | python-portable.zip | ~50 MB | Python 3.13 completo |
   | libs-portable.zip | ~100 MB | Librerías Python |
   | **Total** | **~152 MB** | **Descarga completa** |
   
   ### ✅ Requisitos del Sistema
   
   - Windows 10 o superior (64-bit)
   - 500 MB de espacio en disco
   - 4 GB de RAM (recomendado)
   - No requiere Python instalado
   - No requiere permisos de administrador
   
   ### 📖 Documentación
   
   - [Instalación Rápida](INSTALACION_RAPIDA.md)
   - [README Completo](README.md)
   - [Guía de Distribución](docs/GUIA_DISTRIBUCION.md)
   
   ---
   
   **Creado por:** Lucas Gnemmi  
   **Fecha:** Diciembre 2025
   ```

5. **Subir los archivos**
   - Arrastra `Release/python-portable.zip` 
   - Arrastra `Release/libs-portable.zip`
   
   ⏱️ Tiempo estimado de subida: 5-10 minutos (depende de tu internet)

6. **Click en "Publish release"**

---

### Paso 4: Actualizar el Script de Descarga

1. **Editar** `Descargar_Python.ps1`

2. **Buscar esta línea:**
   ```powershell
   $GITHUB_RELEASE_URL = "https://github.com/TU_USUARIO/TU_REPO/releases/latest/download"
   ```

3. **Reemplazar con tu URL real:**
   ```powershell
   # Ejemplo:
   $GITHUB_RELEASE_URL = "https://github.com/lucastgnemmi/dhl-order-system/releases/latest/download"
   ```

4. **Guardar y hacer commit:**
   ```bash
   git add Descargar_Python.ps1
   git commit -m "Actualizar URL de descarga"
   git push origin main
   ```

---

### Paso 5: Probar Todo

1. **Probar la instalación automática:**
   - Descarga tu repositorio en una nueva carpeta
   - Ejecuta `Descargar_Python.bat`
   - Verifica que descargue e instale correctamente

2. **Probar el sistema:**
   - Ejecuta `EXE_Procesar_Ordenes.bat`
   - Verifica que abra correctamente

---

## 🎉 ¡Listo para Compartir!

Tu repositorio ahora tiene:

✅ Código fuente ligero (~2 MB)  
✅ Release con archivos grandes  
✅ Instalador automático funcional  
✅ Documentación completa  

### Para compartir con otros usuarios:

**Opción 1 - Instalación Automática:**
```
"Ve a: https://github.com/TU_USUARIO/TU_REPO
Descarga el código, ejecuta Descargar_Python.bat y listo!"
```

**Opción 2 - Instalación Manual:**
```
"Ve a: https://github.com/TU_USUARIO/TU_REPO/releases/latest
Descarga los 3 archivos, extrae todo junto y ejecuta EXE_Procesar_Ordenes.bat"
```

---

## 🔄 Para Futuras Actualizaciones

### Actualizar Python o Librerías:

1. Ejecuta `Preparar_Release.bat`
2. Crea un nuevo Release (ej: v3.1.0)
3. Sube los nuevos ZIPs
4. GitHub automáticamente actualizará `/releases/latest/download`
5. El script de descarga seguirá funcionando sin cambios

### Actualizar Solo el Código:

1. Haz commit y push normalmente
2. Los usuarios pueden usar el sistema de actualización del launcher

---

## 📊 Resumen de Archivos Creados

| Archivo | Propósito |
|---------|-----------|
| `Descargar_Python.ps1` | Script de instalación automática |
| `Descargar_Python.bat` | Launcher del instalador |
| `Preparar_Release.ps1` | Comprime python/ y libs/ para release |
| `Preparar_Release.bat` | Launcher del preparador |
| `INSTALACION_RAPIDA.md` | Guía rápida para usuarios |
| `docs/GUIA_DISTRIBUCION.md` | Guía técnica completa |
| `CHECKLIST_DISTRIBUCION.md` | Este archivo |
| `.gitignore` | Actualizado para excluir python/ y libs/ |
| `README.md` | Actualizado con instrucciones de instalación |

---

## 🆘 Solución de Problemas

### Si el instalador automático falla:

1. Verifica que la URL en `Descargar_Python.ps1` es correcta
2. Verifica que el Release está publicado
3. Prueba descarga manual desde el Release
4. Verifica conexión a internet

### Si los archivos son muy grandes:

GitHub acepta archivos hasta 2 GB en Releases. 
Tus archivos (~150 MB total) están muy por debajo del límite.

### Si necesitas hostear en otro lugar:

Puedes usar:
- OneDrive (ya lo usas)
- Google Drive
- Dropbox
- WeTransfer (temporal)

Solo actualiza las URLs en `Descargar_Python.ps1`

---

**¿Necesitas ayuda?** Revisa [docs/GUIA_DISTRIBUCION.md](docs/GUIA_DISTRIBUCION.md)
