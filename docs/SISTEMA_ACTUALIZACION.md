# 🔄 Sistema de Actualización Inteligente - Documentación Técnica

## Descripción General

Sistema avanzado de actualización automática que verifica **archivo por archivo** contra el repositorio de GitHub, proporcionando control completo sobre el proceso de actualización y protegiendo contra actualizaciones innecesarias.

## Características Clave

### ✅ Verificación Archivo por Archivo
- Compara cada archivo del proyecto con su versión en GitHub
- Detecta modificaciones, adiciones y eliminaciones
- Muestra estadísticas detalladas de cambios

### 🔒 Protección Inteligente
- **Bloquea actualizaciones** si ya tienes la última versión
- Evita descargas y operaciones innecesarias
- Protege la integridad del sistema

### 📊 Reportes Detallados
- Lista completa de archivos modificados
- Archivos nuevos agregados al proyecto
- Archivos eliminados de la versión actual
- Historial de commits recientes

### 🔐 Respaldo Automático
- Guarda configuraciones locales antes de actualizar
- Restaura automáticamente después de la actualización
- Protege datos personalizados del usuario

## Arquitectura del Sistema

### Componentes Principales

```
Sistema de Actualización
├── Actualizar_Sistema.ps1      # Script principal con menú interactivo
├── Actualizar.bat              # Launcher Windows
├── Verificar_Actualizacion.ps1 # Verificador rápido
└── actualizacion.log           # Log de operaciones
```

### Flujo de Trabajo

```
┌─────────────────────────────────────────────┐
│  Usuario ejecuta verificación/actualización │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Verificar Git instalado                    │
│  Verificar repositorio válido               │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  git fetch origin main                      │
│  Obtener commits local y remoto             │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│  Comparar commits                           │
│  ¿Son iguales?                             │
└────────────┬───────────┬────────────────────┘
             │           │
         SÍ  │           │  NO
             │           │
             ▼           ▼
   ┌──────────────┐  ┌──────────────────────┐
   │ Sistema al   │  │ git diff --name-     │
   │ día          │  │ status HEAD origin/  │
   │ BLOQUEAR     │  │ main                 │
   │ actualización│  │                      │
   └──────────────┘  └─────────┬────────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │ Analizar cambios:    │
                     │ - Modificados        │
                     │ - Agregados          │
                     │ - Eliminados         │
                     └─────────┬────────────┘
                               │
                               ▼
                     ┌──────────────────────┐
                     │ Mostrar estadísticas │
                     │ Ofrecer actualizar   │
                     └─────────┬────────────┘
                               │
                               ▼
              ┌────────────────┴────────────────┐
              │                                  │
           CANCELAR                         ACTUALIZAR
              │                                  │
              ▼                                  ▼
       ┌─────────────┐              ┌────────────────────┐
       │ Salir       │              │ 1. Backup configs  │
       └─────────────┘              │ 2. git reset --hard│
                                    │ 3. Restaurar       │
                                    │ 4. Verificar       │
                                    └────────────────────┘
```

## Funciones Principales

### 1. Check-Updates

**Propósito**: Verificar si hay actualizaciones disponibles comparando archivo por archivo.

**Retorno**: Objeto hashtable con información detallada:
```powershell
@{
    UpdateAvailable = $true/$false
    IsUpToDate = $true/$false
    LocalCommit = "abc1234567..."
    RemoteCommit = "def8901234..."
    TotalChanges = 5
    FilesModified = @("file1.py", "file2.ps1")
    FilesAdded = @("new_feature.py")
    FilesDeleted = @("old_module.py")
}
```

**Proceso**:
1. Verifica Git instalado
2. Valida repositorio Git
3. Ejecuta `git fetch origin main`
4. Compara commits: `git rev-parse HEAD` vs `git rev-parse origin/main`
5. Si son diferentes:
   - Ejecuta `git diff --name-status HEAD origin/main`
   - Parsea resultados (M=Modificado, A=Agregado, D=Eliminado)
   - Genera estadísticas y reportes
6. Si son iguales:
   - Marca como actualizado
   - Retorna sin cambios

### 2. Update-System

**Propósito**: Actualizar el sistema a la última versión de GitHub.

**Protecciones**:
- **Pre-verificación**: Ejecuta Check-Updates primero
- **Bloqueo automático**: Si `IsUpToDate = $true`, muestra mensaje y cancela
- **Confirmación**: Requiere confirmación del usuario

**Proceso de Actualización**:

```powershell
# 1. Verificación previa
$checkResult = Check-Updates
if ($checkResult.IsUpToDate) {
    Write-Host "NO SE PUEDE ACTUALIZAR - Ya está al día"
    return $false
}

# 2. Backup de configuraciones
$backupFiles = @(
    "agenda_config.json",
    "rules.json",
    "products.json"
)
# Copiar a backup_temp/

# 3. Actualización desde GitHub
git fetch origin main
git reset --hard origin/main

# 4. Restauración de configuraciones
# Copiar desde backup_temp/ de vuelta

# 5. Verificación post-actualización
$newCommit = git rev-parse HEAD
if ($newCommit -eq $checkResult.RemoteCommit) {
    # Éxito
}
```

### 3. Verify-Files

**Propósito**: Verificar integridad de archivos críticos del sistema.

**Archivos Verificados**:
```powershell
@(
    @{Path="gui_moderna_v2.py"; Desc="Interfaz principal"},
    @{Path="procesamiento_v2.py"; Desc="Motor de procesamiento"},
    @{Path="agenda_manager.py"; Desc="Gestor de agenda"},
    @{Path="rules_manager.py"; Desc="Gestor de reglas"},
    @{Path="products_manager.py"; Desc="Gestor de productos"},
    @{Path="libs"; Desc="Librerías empaquetadas"; IsDir=$true},
    @{Path="EXE_Procesar_Ordenes.bat"; Desc="Launcher principal"}
)
```

**Resultado**:
- ✅ [OK] para archivos presentes
- ❌ [FALTA] para archivos ausentes
- Ofrece reparación automática si faltan archivos

## Formato de Salida

### Verificación de Actualizaciones

#### Sistema Actualizado
```
================================================
 VERIFICACIÓN DE ARCHIVOS DEL PROYECTO
================================================

✓ El sistema está ACTUALIZADO
✓ Todos los archivos coinciden con GitHub

Versión actual: abc1234
```

#### Actualización Disponible
```
================================================
 VERIFICACIÓN DE ARCHIVOS DEL PROYECTO
================================================

⚠ HAY UNA NUEVA VERSIÓN DISPONIBLE

ARCHIVOS MODIFICADOS:
  [M] gui_moderna_v2.py
  [M] procesamiento_v2.py

ARCHIVOS NUEVOS:
  [+] nueva_funcionalidad.py

ARCHIVOS ELIMINADOS:
  [-] modulo_obsoleto.py

CAMBIOS RECIENTES:
  • abc1234 Mejora en sistema de validación
  • def5678 Corrección de bugs
  • ghi9012 Nueva funcionalidad X

RESUMEN: 5 archivo(s) con cambios
Versión local: abc1234
Versión remota: jkl3456
```

### Actualización Bloqueada

```
================================================
 NO SE PUEDE ACTUALIZAR
================================================

✓ Ya tienes la última versión
✓ Todos los archivos están actualizados

Actualización cancelada - Sistema ya está al día
```

### Actualización Exitosa

```
================================================
 ✓ ACTUALIZACIÓN COMPLETADA
================================================

Versión instalada: jkl3456
Archivos actualizados: 5
```

## Seguridad y Respaldos

### Archivos Protegidos

**Siempre respaldados y restaurados**:
- `agenda_config.json` - Configuración de agenda del usuario
- `rules.json` - Reglas especiales personalizadas
- `products.json` - Base de datos de productos

**Nunca modificados**:
- Archivos en `Ordenes/` - PDFs de entrada
- Archivos en `Salidas/` - Resultados procesados
- `actualizacion.log` - Historial de actualizaciones

### Proceso de Respaldo

```powershell
# 1. Crear carpeta temporal
$backupDir = "backup_temp"
New-Item -ItemType Directory -Path $backupDir

# 2. Copiar archivos protegidos
foreach ($file in $backupFiles) {
    Copy-Item $file $backupDir/$file
}

# 3. Ejecutar actualización
git reset --hard origin/main

# 4. Restaurar archivos
foreach ($file in $backupFiles) {
    Copy-Item $backupDir/$file $file
}

# 5. Limpiar temporal
Remove-Item $backupDir -Recurse -Force
```

## Logging

### Formato de Log

```
[2024-12-29 14:30:15] === Inicio del sistema de actualización ===
[2024-12-29 14:30:16] Verificando actualizaciones disponibles...
[2024-12-29 14:30:17] Consultando servidor GitHub...
[2024-12-29 14:30:18] Actualización disponible - Local: abc1234, Remoto: def5678
[2024-12-29 14:30:18]   Modificado: gui_moderna_v2.py
[2024-12-29 14:30:18]   Modificado: procesamiento_v2.py
[2024-12-29 14:30:18]   Agregado: nueva_funcionalidad.py
[2024-12-29 14:30:18] Total de archivos con cambios: 3
[2024-12-29 14:30:25] Iniciando proceso de actualización...
[2024-12-29 14:30:26] Verificando conexión con GitHub...
[2024-12-29 14:30:27] Guardando configuraciones locales...
[2024-12-29 14:30:27]   Respaldo: agenda_config.json
[2024-12-29 14:30:27]   Respaldo: rules.json
[2024-12-29 14:30:27]   Respaldo: products.json
[2024-12-29 14:30:28] Descargando última versión desde GitHub...
[2024-12-29 14:30:32] Restaurando configuraciones locales...
[2024-12-29 14:30:32]   Restaurado: agenda_config.json
[2024-12-29 14:30:32]   Restaurado: rules.json
[2024-12-29 14:30:32]   Restaurado: products.json
[2024-12-29 14:30:33] Sistema actualizado correctamente a versión: def5678
[2024-12-29 14:30:35] === Fin del sistema de actualización ===
```

### Niveles de Log

- **Cyan**: Operaciones principales
- **Green**: Éxitos y confirmaciones
- **Yellow**: Advertencias y actualizaciones disponibles
- **Red**: Errores críticos
- **Gray**: Información detallada

## Códigos de Salida

### Verificar_Actualizacion.ps1

```powershell
exit 0  # Sistema actualizado (IsUpToDate = true)
exit 1  # Error durante verificación
exit 2  # Actualización disponible (UpdateAvailable = true)
```

### Uso en Scripts

```powershell
# Verificar y actuar según resultado
.\Verificar_Actualizacion.ps1
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Todo al día"
} elseif ($exitCode -eq 2) {
    Write-Host "Ejecutando actualización..."
    .\Actualizar_Sistema.ps1
}
```

## Requisitos Técnicos

### Software Necesario

1. **Git for Windows** (v2.30+)
   - Descarga: https://git-scm.com/download/win
   - Debe estar en PATH del sistema

2. **PowerShell** (v5.1+)
   - Incluido en Windows 10/11
   - Execution Policy: Bypass o RemoteSigned

3. **Conexión a Internet**
   - Para consultas a GitHub
   - Puerto 443 (HTTPS) abierto

### Permisos

- **Lectura**: Carpeta del proyecto y subcarpetas
- **Escritura**: Para actualizar archivos
- **Ejecución**: Scripts PowerShell (.ps1)

## Solución de Problemas

### Git no encontrado

**Síntoma**: "Git no está instalado"

**Solución**:
```powershell
# 1. Instalar Git
# Descargar desde: https://git-scm.com/download/win

# 2. Verificar instalación
git --version

# 3. Reiniciar PowerShell
```

### No es repositorio Git

**Síntoma**: "No es un repositorio Git válido"

**Causa**: Carpeta `.git` faltante

**Solución**:
```powershell
# Opción 1: Clonar repositorio completo
git clone https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes.git

# Opción 2: Inicializar repositorio existente
cd Sys_Procesar_Ordenes
git init
git remote add origin https://github.com/Lucasgnemmi123/Sys_Procesar_Ordenes.git
git fetch origin main
git reset --hard origin/main
```

### Error de conexión

**Síntoma**: "No hay conexión a Internet"

**Diagnóstico**:
```powershell
# Verificar conectividad
Test-Connection github.com -Count 4

# Verificar DNS
nslookup github.com

# Verificar proxy (si aplica)
git config --global http.proxy
```

### Conflictos de archivos

**Síntoma**: Error durante `git reset --hard`

**Solución**:
```powershell
# Forzar limpieza
git clean -fdx
git reset --hard origin/main

# Si persiste, respaldar y reclonar
```

## Integración con CI/CD

### Verificación Automática

```powershell
# Script de verificación automática
$result = & .\Verificar_Actualizacion.ps1
if ($LASTEXITCODE -eq 2) {
    Send-MailMessage -To "admin@example.com" `
                     -Subject "Actualización disponible" `
                     -Body "Nueva versión disponible en GitHub"
}
```

### Actualización Programada

```powershell
# Tarea programada (Task Scheduler)
# Ejecutar cada día a las 9:00 AM
schtasks /create /tn "DHL_Update_Check" `
         /tr "powershell.exe -File C:\...\Verificar_Actualizacion.ps1" `
         /sc daily /st 09:00
```

## Mejores Prácticas

### Para Usuarios

1. **Verificar regularmente**: Ejecutar verificación semanalmente
2. **Actualizar en horarios bajos**: Evitar actualizaciones durante procesamiento
3. **Revisar changelog**: Leer cambios antes de actualizar
4. **Respaldar datos**: Aunque el sistema hace respaldo automático

### Para Desarrolladores

1. **Commits descriptivos**: Mensajes claros para el historial
2. **Versioning semántico**: Usar tags para versiones
3. **Testing**: Probar cambios antes de push
4. **Documentación**: Actualizar README con cambios importantes

## Roadmap Futuro

### Funcionalidades Planeadas

- [ ] Auto-actualización opcional (sin confirmación)
- [ ] Rollback a versiones anteriores
- [ ] Descarga diferencial (solo archivos modificados)
- [ ] Notificaciones de escritorio
- [ ] Changelog automático desde commits
- [ ] Verificación de integridad con checksums
- [ ] Soporte para múltiples branches

---

**Versión de Documento**: 1.0  
**Última Actualización**: Diciembre 2024  
**Autor**: Sistema DHL Order Processing
