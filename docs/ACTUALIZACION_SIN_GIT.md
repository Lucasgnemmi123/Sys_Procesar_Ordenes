# 🔄 Nueva Actualización Sin Git

## ✅ Problema Resuelto

Tu sistema de actualización anterior requería:
- Git instalado en la computadora
- Que la carpeta fuera un repositorio Git clonado
- Conexión configurada a GitHub

**Esto era innecesario para un repositorio público.**

## 🆕 Nueva Solución

He creado **Actualizar_Directo.ps1** que:

### ✨ Ventajas
- ✅ **NO requiere Git instalado**
- ✅ Descarga directamente el ZIP desde GitHub
- ✅ Funciona con cualquier repositorio público
- ✅ Más simple y rápido
- ✅ Preserva tus configuraciones locales

### 🎯 Cómo Funciona

1. Descarga el ZIP de tu repositorio desde:
   ```
   https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes/archive/refs/heads/main.zip
   ```

2. Extrae los archivos en una carpeta temporal

3. Hace backup de:
   - `agenda_config.json`
   - `rules.json`
   - `products.json`

4. Copia los archivos nuevos (excluyendo):
   - Carpetas: `.git`, `Ordenes`, `Salidas`, `python`, `libs`
   - Archivos de logs

5. Restaura tus configuraciones

6. Limpia archivos temporales

### 📋 Cómo Usar

#### Opción 1: Doble clic en el archivo BAT
```
Actualizar.bat
```

#### Opción 2: Desde PowerShell
```powershell
.\Actualizar_Directo.ps1
```

#### Opción 3: Solo verificar (sin actualizar)
```powershell
.\Actualizar_Directo.ps1 -SoloVerificar
```

### 🔧 Qué Se Actualiza

✅ **SÍ se actualizan:**
- Scripts de Python (`.py`)
- Documentación (`.md`)
- Archivos de configuración del sistema
- Plantillas
- Cualquier código fuente

❌ **NO se actualizan (se preservan):**
- `Ordenes/` - Tus archivos de órdenes
- `Salidas/` - Tus archivos procesados
- `python/` - Tu instalación de Python
- `libs/` - Tus librerías instaladas
- `agenda_config.json` - Tu configuración de agenda
- `rules.json` - Tus reglas personalizadas
- `products.json` - Tus productos personalizados

### 🎉 Resultado

El sistema reemplaza todo lo de tu carpeta con lo que está en GitHub, pero **protegiendo** tus datos y configuraciones importantes.

### 📌 Archivos Modificados

1. **Actualizar_Directo.ps1** (NUEVO)
   - Script principal de actualización

2. **Actualizar.bat** (MODIFICADO)
   - Ahora llama a Actualizar_Directo.ps1

3. **Actualizar_Sistema.ps1** (OBSOLETO)
   - Archivo antiguo que requería Git
   - Puedes eliminarlo si quieres

4. **Actualizar_Sistema_Simple.ps1** (BORRAR)
   - Tenía errores de sintaxis
   - Ya no se usa

### 🚀 Siguiente Actualización en GitHub

Cuando subas estos cambios a GitHub, los usuarios solo necesitarán:
1. Ejecutar `Actualizar.bat`
2. Esperar que descargue
3. ¡Listo!

No más "necesitas tener Git instalado" o "debes clonar el repositorio".

### ⚙️ Configuración Actual

```
Repositorio: Lucasgnemmi123/Sys_Procesar_Ordenes
Rama: main
Método: Descarga directa del ZIP
```

Si necesitas cambiar el repositorio o rama, edita estas líneas en **Actualizar_Directo.ps1**:
```powershell
$GITHUB_REPO = "Lucasgnemmi123/Sys_Procesar_Ordenes"
$GITHUB_BRANCH = "main"
```
