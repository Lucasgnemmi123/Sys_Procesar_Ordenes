# 👤 Guía para Usuarios Finales - Instalación Paso a Paso

## 🎯 ¿Qué vas a instalar?

El **Sistema de Procesamiento de Pedidos DHL** - Una aplicación portable que:
- ✅ Procesa archivos PDF de pedidos
- ✅ Genera archivos Excel automáticamente
- ✅ NO requiere Python instalado en tu PC
- ✅ NO necesita permisos de administrador

---

## 🚀 Instalación Rápida (RECOMENDADA)

### 📥 Paso 1: Descargar el Sistema

1. **Abre tu navegador** (Chrome, Edge, Firefox, etc.)

2. **Ve a la página del proyecto:**
   ```
   https://github.com/TU_USUARIO/TU_REPO
   ```

3. **Descarga el código:**
   - Busca el botón verde que dice **"<> Code"**
   - Click en él
   - Click en **"Download ZIP"**
   - Guarda el archivo (se llamará algo como `TU_REPO-main.zip`)

4. **Espera a que termine la descarga** (~2 MB, es rápido)

---

### 📂 Paso 2: Extraer los Archivos

1. **Busca el archivo descargado**
   - Normalmente está en tu carpeta `Descargas`

2. **Click derecho sobre el archivo ZIP**

3. **Selecciona "Extraer todo..."**

4. **Elige dónde extraer:**
   - Puedes dejarlo en Descargas
   - O llevarlo a Escritorio
   - O crear una carpeta "DHL" en Documentos
   - ¡Da igual! Funciona desde cualquier lugar

5. **Click en "Extraer"**

6. **Se abrirá una carpeta con los archivos**

---

### ⚡ Paso 3: Instalar Python (AUTOMÁTICO)

**¡IMPORTANTE! Este es el paso clave:**

1. **Dentro de la carpeta extraída**, busca este archivo:
   ```
   Descargar_Python.bat
   ```

2. **Doble click sobre él**

3. **Se abrirá una ventana negra** que dirá:
   ```
   ================================================
     DHL Order Processing System - Setup
     Descargador de Python Portable v3.13
   ================================================
   
   Descargando Python 3.13 Portable...
   ```

4. **Espera pacientemente** (2-5 minutos):
   - Descargará Python (~50 MB)
   - Descargará librerías (~100 MB)
   - Todo se descarga de GitHub automáticamente

5. **Cuando termine verás:**
   ```
   ================================================
     ✅ INSTALACIÓN COMPLETADA CON ÉXITO
   ================================================
   
   El sistema está listo para usar.
   Ejecuta: EXE_Procesar_Ordenes.bat
   
   Presiona Enter para salir
   ```

6. **Presiona Enter** para cerrar la ventana

---

### 🎉 Paso 4: Usar el Sistema

1. **En la misma carpeta**, busca el archivo:
   ```
   EXE_Procesar_Ordenes.bat
   ```

2. **Doble click sobre él**

3. **Se abrirá el sistema:**
   - Interfaz moderna con Dark Mode
   - Botones para procesar pedidos
   - Gestión de productos y agenda

4. **¡Ya puedes trabajar!**

---

## ✅ Verificar que Todo Está Bien

Después de instalar, tu carpeta debe tener:

```
📁 Tu carpeta del sistema/
├── 📁 python/                    ✅ (creada por el instalador)
├── 📁 libs/                      ✅ (creada por el instalador)
├── 📁 Ordenes/                   ✅ (donde pones los PDFs)
├── 📁 Salidas/                   ✅ (donde salen los Excel)
├── 📄 EXE_Procesar_Ordenes.bat   ✅ (para ejecutar el sistema)
├── 📄 Descargar_Python.bat       ✅ (ya lo usaste)
└── ... otros archivos ...
```

Si ves las carpetas `python/` y `libs/`, ¡todo está perfecto!

---

## 🔧 Instalación Manual (Plan B)

Si el instalador automático no funciona o prefieres hacerlo manualmente:

### Paso 1: Ir a Releases

1. Ve a: `https://github.com/TU_USUARIO/TU_REPO/releases/latest`

2. Verás una página con archivos para descargar

### Paso 2: Descargar 3 Archivos

Descarga estos archivos (click en cada uno):

1. **Source code (zip)** 
   - ~2 MB - El código de la aplicación

2. **python-portable.zip**
   - ~50 MB - Python empaquetado

3. **libs-portable.zip**
   - ~100 MB - Librerías necesarias

### Paso 3: Extraer Todo Junto

1. Crea una carpeta nueva (ej: "DHL_System" en el Escritorio)

2. Extrae `Source code.zip` en esa carpeta

3. Extrae `python-portable.zip` **en la misma carpeta**
   - Importante: debe quedar una carpeta `python/` dentro

4. Extrae `libs-portable.zip` **en la misma carpeta**
   - Importante: debe quedar una carpeta `libs/` dentro

### Paso 4: Listo

Ejecuta `EXE_Procesar_Ordenes.bat`

---

## ❓ Preguntas Frecuentes

### ❓ "¿Necesito Python instalado en mi PC?"

**NO.** Este sistema trae su propio Python portable. No necesitas instalar Python en tu sistema Windows. No tocará nada de tu computadora.

### ❓ "¿Necesito permisos de administrador?"

**NO.** Todo funciona sin permisos especiales. Puedes instalarlo en cualquier carpeta que tengas acceso.

### ❓ "¿Necesito estar conectado a internet?"

- **Para instalar:** SÍ (solo la primera vez, para descargar Python)
- **Para usar:** NO (funciona 100% offline)

### ❓ "¿Cuánto espacio ocupa?"

Total en disco: ~150 MB
- Python: ~50 MB
- Librerías: ~100 MB
- Código: ~2 MB

### ❓ "¿Puedo mover la carpeta después?"

**SÍ.** Puedes copiar toda la carpeta a otro lugar, incluso a otro PC con Windows. No hay instalación en el sistema.

### ❓ "¿Funciona en cualquier Windows?"

**SÍ.** Funciona en:
- ✅ Windows 10 (64-bit)
- ✅ Windows 11
- ✅ Windows Server 2016 o superior

### ❓ "Si falla el Descargar_Python.bat, ¿qué hago?"

1. Verifica tu conexión a internet
2. Prueba ejecutarlo de nuevo (a veces falla por conexión)
3. Si sigue fallando, usa la **Instalación Manual** (arriba)

### ❓ "¿Cómo actualizo el sistema?"

Ejecuta el sistema y usa la opción de actualización desde el launcher.

### ❓ "¿Dónde pongo los PDFs para procesar?"

En la carpeta `Ordenes/` que está dentro del sistema.

### ❓ "¿Dónde salen los archivos procesados?"

En la carpeta `Salidas/` que está dentro del sistema.

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que seguiste todos los pasos
2. Revisa la sección de Preguntas Frecuentes
3. Asegúrate de tener Windows 10 o superior
4. Verifica que tienes conexión a internet (para instalar)

---

## 📋 Checklist Rápido

Marca cada paso conforme lo completes:

- [ ] Descargué el ZIP del repositorio
- [ ] Extraje los archivos en una carpeta
- [ ] Ejecuté `Descargar_Python.bat`
- [ ] Esperé a que termine la instalación
- [ ] Vi el mensaje "INSTALACIÓN COMPLETADA"
- [ ] Veo las carpetas `python/` y `libs/`
- [ ] Ejecuté `EXE_Procesar_Ordenes.bat`
- [ ] El sistema abrió correctamente

¡Si marcaste todo, estás listo para usar el sistema! 🎉

---

**Documentación creada por:** Lucas Gnemmi  
**Sistema:** DHL Order Processing System v3.0  
**Última actualización:** Diciembre 2025
