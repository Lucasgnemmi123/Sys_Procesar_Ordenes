# 📦 Guía de Distribución del Sistema DHL

## 🎯 Problema

La carpeta `python/` y `libs/` son muy grandes (~150-200 MB) para incluirlas en el repositorio de GitHub directamente. GitHub tiene límites para archivos grandes y el repositorio se volvería pesado.

## ✅ Soluciones Implementadas

### **Solución 1: GitHub Releases (RECOMENDADA)**

Esta es la solución profesional más común y la que usa la mayoría de proyectos open source.

#### Pasos para el Desarrollador:

1. **Preparar los archivos ZIP**
   
   Ejecuta estos comandos en PowerShell:
   
   ```powershell
   # Ir al directorio del proyecto
   cd "C:\Users\luezequi\OneDrive - DPDHL\Desktop\Sys_Procesar_Ordenes"
   
   # Comprimir Python (puede tardar unos minutos)
   Compress-Archive -Path "python" -DestinationPath "python-portable.zip" -CompressionLevel Optimal
   
   # Comprimir Libs
   Compress-Archive -Path "libs" -DestinationPath "libs-portable.zip" -CompressionLevel Optimal
   ```

2. **Crear un Release en GitHub**
   
   - Ve a tu repositorio en GitHub
   - Click en "Releases" (lado derecho)
   - Click en "Create a new release"
   - Tag version: `v3.0.0` (o la versión actual)
   - Release title: `DHL Order Processing System v3.0.0 - Portable`
   - Descripción: 
     ```markdown
     ## 🚀 Versión Portable Completa
     
     Sistema completo de procesamiento de pedidos DHL con Python portable incluido.
     
     ### 📦 Archivos de Descarga:
     - `python-portable.zip` - Python 3.13 empaquetado (requerido)
     - `libs-portable.zip` - Librerías Python (requerido)
     
     ### 🔧 Instalación:
     1. Descarga el código fuente (Source code.zip)
     2. Descarga `python-portable.zip` y `libs-portable.zip`
     3. Extrae todo en la misma carpeta
     4. Ejecuta `EXE_Procesar_Ordenes.bat`
     
     ### ⚡ Instalación Automática:
     1. Descarga solo el código fuente
     2. Ejecuta `Descargar_Python.bat`
     3. El script descargará automáticamente Python y las librerías
     ```
   
   - Arrastra y suelta los archivos:
     - `python-portable.zip`
     - `libs-portable.zip`
   
   - Click en "Publish release"

3. **Actualizar el script de descarga automática**
   
   Edita `Descargar_Python.ps1` y actualiza estas líneas con tu información:
   
   ```powershell
   $GITHUB_RELEASE_URL = "https://github.com/TU_USUARIO/TU_REPO/releases/latest/download"
   ```
   
   Reemplaza `TU_USUARIO` y `TU_REPO` con tu información real. Por ejemplo:
   ```powershell
   $GITHUB_RELEASE_URL = "https://github.com/lucastgnemmi/dhl-order-system/releases/latest/download"
   ```

#### Pasos para el Usuario Final:

**Opción A: Instalación Automática (Fácil)**
1. Descargar el código fuente del repositorio (botón verde "Code" → "Download ZIP")
2. Extraer en cualquier carpeta
3. Doble clic en `Descargar_Python.bat`
4. Esperar a que se descargue e instale automáticamente
5. Listo para usar con `EXE_Procesar_Ordenes.bat`

**Opción B: Instalación Manual**
1. Ir a la página de Releases
2. Descargar los 3 archivos:
   - Source code (zip)
   - python-portable.zip
   - libs-portable.zip
3. Extraer Source code en una carpeta
4. Extraer python-portable.zip en la misma carpeta (debe quedar una carpeta `python/`)
5. Extraer libs-portable.zip en la misma carpeta (debe quedar una carpeta `libs/`)
6. Listo para usar

---

### **Solución 2: Almacenamiento en la Nube**

Si no quieres usar GitHub Releases, puedes usar OneDrive, Google Drive, o Dropbox.

#### Con OneDrive (Recomendado porque ya lo usas):

1. **Subir los archivos**
   - Sube `python-portable.zip` y `libs-portable.zip` a tu OneDrive
   - Click derecho → "Compartir" → "Cualquier persona con el enlace"
   - Copia los enlaces de descarga directa

2. **Actualizar el script**
   
   En `Descargar_Python.ps1`, cambia las URLs:
   
   ```powershell
   # Para OneDrive, el enlace de compartir necesita modificarse
   # Enlace original: https://onedrive.live.com/...?id=xxx
   # Enlace directo: https://onedrive.live.com/download?id=xxx
   
   $PYTHON_ZIP_URL = "https://onedrive.live.com/download?id=TU_ID_PYTHON"
   $LIBS_ZIP_URL = "https://onedrive.live.com/download?id=TU_ID_LIBS"
   ```

3. **Usuario final**
   - Ejecuta `Descargar_Python.bat` y descargará de OneDrive

---

### **Solución 3: Python Portable Estándar**

Opción para que cada usuario descargue Python portable directamente de python.org.

1. **Actualizar README.md**
   
   Agregar instrucciones para descargar Python portable manualmente:
   
   ```markdown
   ## 🔧 Instalación Manual de Python
   
   1. Descargar Python 3.13 Embeddable desde:
      https://www.python.org/ftp/python/3.13.0/python-3.13.0-embed-amd64.zip
   
   2. Extraer en la carpeta del proyecto como `python/`
   
   3. Instalar pip y las librerías:
      ```batch
      Instalar_Dependencias.bat
      ```
   ```

2. **Crear script de instalación de librerías**
   
   Un script que instale todas las librerías necesarias automáticamente.

---

## 📊 Comparación de Soluciones

| Solución | Pros | Contras | Recomendado |
|----------|------|---------|-------------|
| **GitHub Releases** | ✅ Profesional<br>✅ Integrado con GitHub<br>✅ Control de versiones<br>✅ Descarga automática | ⚠️ Requiere crear release | ⭐⭐⭐⭐⭐ |
| **OneDrive/Drive** | ✅ Fácil de subir<br>✅ Ya lo usas | ⚠️ Links pueden expirar<br>⚠️ Límites de descarga | ⭐⭐⭐⭐ |
| **Descarga Manual** | ✅ Tamaño repo mínimo | ❌ Usuario debe hacer más pasos<br>❌ Más complejo | ⭐⭐⭐ |

---

## 🎯 Recomendación Final

**Usar GitHub Releases + Script de Descarga Automática**

### Ventajas:
- ✅ Repositorio limpio y rápido de clonar
- ✅ Usuario puede instalar automáticamente con 1 click
- ✅ Profesional y estándar de la industria
- ✅ Control de versiones de Python/librerías
- ✅ Fácil de actualizar

### Flujo de trabajo:
1. **Desarrollador**: Sube código a GitHub + crea Release con ZIPs
2. **Usuario**: Descarga código → ejecuta `Descargar_Python.bat` → listo

---

## 📝 Actualización del README

El README actual ya está bien estructurado, solo necesita agregar:

```markdown
## 🚀 Primera Instalación

### Opción 1: Instalación Automática (Recomendada)

1. Descarga el código fuente del repositorio
2. Ejecuta `Descargar_Python.bat`
3. Espera a que se descargue Python y las librerías
4. ¡Listo! Ejecuta `EXE_Procesar_Ordenes.bat`

### Opción 2: Instalación Manual

1. Ve a [Releases](https://github.com/TU_USUARIO/TU_REPO/releases/latest)
2. Descarga:
   - Source code (zip)
   - python-portable.zip
   - libs-portable.zip
3. Extrae todo en la misma carpeta
4. Ejecuta `EXE_Procesar_Ordenes.bat`

## 📦 ¿Qué incluyen los archivos?

- **python-portable.zip**: Python 3.13 completo (~50 MB)
- **libs-portable.zip**: Todas las librerías necesarias (~100 MB)
- **Source code**: Tu código de la aplicación (~2 MB)
```

---

## 🛠️ Mantenimiento

### Al actualizar Python o librerías:

1. Recomprimir los archivos
2. Crear un nuevo Release
3. GitHub automáticamente actualizará `/releases/latest/download`
4. El script de descarga seguirá funcionando sin cambios

---

## ✅ Checklist de Distribución

- [ ] Crear `python-portable.zip` y `libs-portable.zip`
- [ ] Crear GitHub Release con los archivos
- [ ] Actualizar `Descargar_Python.ps1` con la URL correcta
- [ ] Probar el script de descarga automática
- [ ] Actualizar README.md con instrucciones
- [ ] Compartir el repositorio

---

**Documentación creada por: Lucas Gnemmi**  
**Fecha: 2025-12-29**
