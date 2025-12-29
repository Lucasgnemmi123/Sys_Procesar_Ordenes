# 🎯 Guía Rápida: Sistema de Actualización Inteligente

## ¿Qué hace el nuevo sistema?

El sistema ahora **verifica archivo por archivo** contra GitHub y te dice:
- ✅ Si estás al día (y NO te deja actualizar innecesariamente)
- 📋 Exactamente qué archivos cambiaron
- ➕ Qué archivos nuevos hay
- ➖ Qué archivos se eliminaron

## 🚀 Cómo Usar

### Opción 1: Verificación Rápida (Recomendado)
```powershell
# Simplemente ejecuta:
.\Verificar_Actualizacion.ps1
```

**¿Qué verás?**
- ✅ Si está actualizado: "SISTEMA ACTUALIZADO [OK]"
- ⚠️ Si hay actualizaciones: "ACTUALIZACIÓN DISPONIBLE [!]"

### Opción 2: Sistema Completo con Menú
```powershell
# Ejecuta:
.\Actualizar.bat
# o
.\Actualizar_Sistema.ps1
```

**Menú de opciones:**
1. **Verificar actualizaciones** - Ver qué cambió en GitHub
2. **Actualizar sistema** - Descargar última versión
3. **Verificar archivos** - Comprobar integridad
4. **Ver información** - Versión actual y detalles

### Opción 3: Desde el Launcher Principal
```powershell
# Ejecuta el launcher:
.\EXE_Procesar_Ordenes.bat

# Selecciona: ⟳ ACTUALIZAR SISTEMA
```

## 📊 Ejemplo Real de Verificación

### Caso 1: Ya estás al día
```
  ================================================
   VERIFICACIÓN DE ARCHIVOS DEL PROYECTO
  ================================================

  ✓ El sistema está ACTUALIZADO
  ✓ Todos los archivos coinciden con GitHub

  Versión actual: 9bebf16
```

**Resultado**: Si intentas actualizar, el sistema te BLOQUEARÁ diciendo:
```
  ================================================
   NO SE PUEDE ACTUALIZAR
  ================================================

  ✓ Ya tienes la última versión
  ✓ Todos los archivos están actualizados
```

### Caso 2: Hay actualizaciones disponibles
```
  ================================================
   VERIFICACIÓN DE ARCHIVOS DEL PROYECTO
  ================================================

  ⚠ HAY UNA NUEVA VERSIÓN DISPONIBLE

  ARCHIVOS MODIFICADOS:
    [M] gui_moderna_v2.py
    [M] Actualizar_Sistema.ps1

  ARCHIVOS NUEVOS:
    [+] Verificar_Actualizacion.ps1
    [+] docs/SISTEMA_ACTUALIZACION.md

  CAMBIOS RECIENTES:
    • abc1234 Sistema de actualización inteligente
    • def5678 Verificación archivo por archivo

  RESUMEN: 4 archivo(s) con cambios
  Versión local: 9bebf16
  Versión remota: abc1234
```

**Resultado**: El sistema te permite actualizar y te pregunta si deseas hacerlo.

## 🔐 ¿Qué pasa con mis archivos?

### Archivos que se ACTUALIZAN:
- Código Python (gui_moderna_v2.py, procesamiento_v2.py, etc.)
- Scripts PowerShell
- Documentación
- Librerías

### Archivos que NUNCA se tocan:
- ✅ `agenda_config.json` - Tu agenda personalizada
- ✅ `rules.json` - Tus reglas especiales
- ✅ `products.json` - Tu catálogo de productos
- ✅ Carpeta `Ordenes/` - Tus PDFs
- ✅ Carpeta `Salidas/` - Tus resultados

**El sistema hace respaldo automático antes de actualizar y los restaura después.**

## 💡 Casos de Uso

### 1. Verificación Diaria/Semanal
```powershell
# Ejecutar cada mañana o semanalmente:
.\Verificar_Actualizacion.ps1
```

### 2. Antes de Procesar Pedidos Importantes
```powershell
# Asegurarte de tener la última versión:
.\Actualizar.bat
# Opción 1: Verificar
# Si hay actualización, Opción 2: Actualizar
```

### 3. Automatización
```powershell
# En un script batch:
powershell -File ".\Verificar_Actualizacion.ps1"
if %ERRORLEVEL% EQU 2 (
    echo Hay actualización disponible
    REM Notificar al usuario
)
```

## ❓ Preguntas Frecuentes

### P: ¿Puedo actualizar si ya estoy al día?
**R**: NO. El sistema te bloqueará automáticamente para evitar operaciones innecesarias.

### P: ¿Qué pasa si tengo cambios locales en mis archivos de código?
**R**: Git sobrescribirá los archivos de código. Pero tus configuraciones (JSON) siempre se respetan.

### P: ¿Cómo sé si realmente necesito actualizar?
**R**: Ejecuta `.\Verificar_Actualizacion.ps1` y verás la lista exacta de archivos modificados. Si son archivos que no usas, puedes decidir no actualizar.

### P: ¿Qué pasa si la actualización falla?
**R**: El sistema restaura automáticamente los respaldos. Además, puedes volver a ejecutar o descargar el proyecto completo desde GitHub.

### P: ¿Necesito Git instalado?
**R**: Sí, el sistema requiere Git. Si no lo tienes, descárgalo de: https://git-scm.com/download/win

## 🔧 Solución de Problemas

### "Git no está instalado"
1. Descargar Git: https://git-scm.com/download/win
2. Instalar con opciones por defecto
3. Reiniciar PowerShell
4. Intentar nuevamente

### "No es un repositorio Git válido"
1. Verificar que descargaste el proyecto completo desde GitHub
2. No uses copias parciales de archivos
3. Si persiste, clona de nuevo:
   ```
   git clone https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes.git
   ```

### "Error de conexión"
1. Verificar conexión a Internet
2. Comprobar que puedes acceder a github.com
3. Intentar más tarde

## 📝 Log de Actualizaciones

Todas las operaciones se registran en:
```
actualizacion.log
```

Puedes revisar este archivo para ver el historial completo de verificaciones y actualizaciones.

## 🎓 Tips Profesionales

1. **Verifica antes de actualizar**: Usa siempre la opción de verificación primero
2. **Lee los cambios**: Revisa qué archivos cambiaron antes de actualizar
3. **Actualiza en horarios bajos**: No actualices mientras procesas pedidos importantes
4. **Mantén respaldos externos**: Aunque el sistema hace respaldos, siempre es bueno tener copias de seguridad

---

## 📞 ¿Necesitas Ayuda?

- **Documentación Completa**: `docs/SISTEMA_ACTUALIZACION.md`
- **Resumen Técnico**: `docs/RESUMEN_ACTUALIZACION.md`
- **README Principal**: `README.md`

---

**¡El sistema ahora es más inteligente y seguro!** 🚀
