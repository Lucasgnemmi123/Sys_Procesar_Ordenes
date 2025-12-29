# Sistema de Gestión de Productos 📦

## Descripción

El sistema de gestión de productos reemplaza el antiguo archivo Excel `Items.xlsx` con una solución moderna basada en JSON, completamente integrada en la aplicación.

## Características Principales

### ✨ Gestión de Productos
- **Agregar productos**: Ingresa SKU y descripción manualmente
- **Editar productos**: Doble clic en la tabla para cargar datos al editor
- **Eliminar productos**: Selecciona uno o varios productos y elimínalos
- **Buscar productos**: Filtrado en tiempo real por SKU o descripción

### 📥 Carga Masiva
- **Importar desde Excel**: Importa productos desde archivos Excel existentes
- **Exportar a Excel**: Exporta tu catálogo completo
- **Descargar Template**: Obtén un archivo de ejemplo con 3 productos
- **Detección automática**: El sistema detecta columnas automáticamente (SKU, CODIGO, CODE, etc.)

### 📊 Estadísticas
- Total de productos registrados
- Fecha de última actualización

## Archivos del Sistema

```
products_manager.py      # Backend - Gestión de datos en JSON
products_dialog.py       # Frontend - Interfaz gráfica
products.json            # Base de datos de productos
migrate_items_to_products.py  # Script de migración
```

## Migración desde Items.xlsx

Si tienes un archivo `Items.xlsx` existente, puedes migrar tus datos:

### Opción 1: Script de Migración Automática

```bash
python migrate_items_to_products.py
```

Este script:
1. Lee tu archivo `Items.xlsx`
2. Detecta automáticamente las columnas SKU y DESCRIPCION
3. Importa todos los productos a `products.json`
4. Crea un backup del archivo original

### Opción 2: Importación Manual desde la App

1. Abre la aplicación
2. Haz clic en **"📦 Gestión de Productos"**
3. Ve a la pestaña **"Carga Masiva"**
4. Haz clic en **"📂 Importar desde Excel"**
5. Selecciona tu archivo `Items.xlsx`

## Uso en la Aplicación

### Acceso al Gestor de Productos

El gestor se puede abrir desde:
- **Botón principal**: "📦 Gestión de Productos" (Paso 2)
- **Acceso rápido**: "📦 Gestión de Productos" (sección inferior)

### Agregar Productos Manualmente

1. En el panel "Agregar/Editar Producto"
2. Ingresa el **SKU** (código del producto)
3. Ingresa la **DESCRIPCION**
4. Haz clic en **"✅ Agregar Producto"**

### Editar Productos

1. Encuentra el producto en la tabla
2. **Doble clic** sobre el producto
3. Los datos se cargarán en el editor
4. Modifica la descripción
5. Haz clic en **"💾 Actualizar Producto"**

### Eliminar Productos

1. Selecciona uno o varios productos en la tabla
2. Haz clic en **"🗑️ Eliminar Seleccionados"**
3. Confirma la eliminación

### Buscar Productos

1. Usa el cuadro de búsqueda en la parte superior de la tabla
2. Escribe parte del SKU o descripción
3. La tabla se filtrará automáticamente en tiempo real

## Formato del Template Excel

Cuando descargas el template, obtienes un archivo con estas columnas:

| SKU | DESCRIPCION |
|-----|-------------|
| PROD001 | Producto de Ejemplo 1 |
| PROD002 | Producto de Ejemplo 2 |
| PROD003 | Producto de Ejemplo 3 |

### Columnas Soportadas para Importación

El sistema detecta automáticamente estas variantes:

**Para SKU:**
- `SKU`, `sku`, `Sku`
- `CODIGO`, `codigo`, `Codigo`
- `CODE`, `code`, `Code`

**Para DESCRIPCION:**
- `DESCRIPCION`, `descripcion`, `Descripcion`
- `DESC`, `desc`
- `NOMBRE`, `nombre`, `Nombre`
- `DESCRIPTION`, `description`

## Validación en el Procesamiento

Durante el procesamiento de pedidos, el sistema:

1. ✅ Carga automáticamente la lista de productos desde `products.json`
2. 🔍 Valida que cada SKU del pedido exista en la maestra de productos
3. ❌ Rechaza productos con SKU no registrado
4. 📝 Genera observación: `"//Falta Producto en Maestra C.Calzada//"`

### Ventajas sobre Items.xlsx

| Característica | Items.xlsx | products.json |
|---------------|------------|---------------|
| Edición | Excel externo | Dentro de la app |
| Búsqueda | Manual | Automática con filtro |
| Carga masiva | No disponible | ✅ Import/Export |
| Validación | Requiere Excel | JSON nativo |
| Velocidad | Lenta (lectura Excel) | Rápida (JSON) |
| Duplicados | Posibles | Prevención automática |
| Historial | No | Timestamp en cada producto |

## Estructura de products.json

```json
{
  "products": [
    {
      "sku": "PROD001",
      "descripcion": "Producto de Ejemplo 1",
      "created": "2024-01-15 10:30:45"
    }
  ]
}
```

## Troubleshooting

### ❌ "No products found in master list"

**Problema**: El sistema no encuentra productos registrados.

**Solución**:
1. Abre "📦 Gestión de Productos"
2. Verifica que haya productos en la tabla
3. Si está vacía, importa desde Excel o agrega manualmente

### ⚠️ "SKUs faltan en Maestra C.Calzada"

**Problema**: Algunos productos del pedido no están registrados.

**Solución**:
1. Revisa el log para ver qué SKUs faltan
2. Abre "📦 Gestión de Productos"
3. Agrega los SKUs faltantes

### 📝 Columna no detectada en importación

**Problema**: El sistema no detecta tu columna de SKU o descripción.

**Solución**:
1. Renombra las columnas en Excel a: `SKU` y `DESCRIPCION`
2. O usa los nombres soportados (ver "Columnas Soportadas")

## Backups y Seguridad

- El archivo `products.json` se actualiza automáticamente
- Se recomienda hacer backup periódico del archivo
- El script de migración crea `Items_BACKUP.xlsx` automáticamente
- Puedes exportar a Excel en cualquier momento como backup

## Mejores Prácticas

1. **Mantén SKUs únicos**: No duplicar códigos
2. **Descripciones claras**: Facilita búsquedas futuras
3. **Backup regular**: Exporta a Excel periódicamente
4. **Validación previa**: Antes de procesar pedidos, verifica que todos los SKUs estén registrados
5. **Migración inicial**: Usa el script de migración para datos existentes

## Soporte

Para más información o problemas, contacta al equipo de desarrollo.

---

**Versión**: 2.0  
**Última actualización**: 2024  
**Compatibilidad**: Reemplaza completamente Items.xlsx
