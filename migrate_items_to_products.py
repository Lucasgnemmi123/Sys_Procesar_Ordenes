"""
Script de migración: Items.xlsx -> products.json
==========================================

Este script migra los datos del antiguo archivo Items.xlsx
al nuevo sistema de gestión de productos basado en JSON.

Uso:
    python migrate_items_to_products.py
"""

import os
import pandas as pd
from products_manager import ProductsManager


def migrate_items_xlsx():
    """Migrar Items.xlsx a products.json"""
    
    # Ruta al archivo Items.xlsx
    items_path = os.path.join("Full-Agenda", "Items.xlsx")
    
    print("=" * 60)
    print("MIGRACIÓN: Items.xlsx -> products.json")
    print("=" * 60)
    print()
    
    # Verificar que existe Items.xlsx
    if not os.path.exists(items_path):
        print(f"❌ No se encontró el archivo: {items_path}")
        print(f"💡 Si no tienes Items.xlsx, puedes empezar a usar")
        print(f"   el sistema de productos directamente desde la app.")
        return False
    
    print(f"📂 Archivo encontrado: {items_path}")
    
    try:
        # Leer archivo Items.xlsx
        print(f"📖 Leyendo Items.xlsx...")
        df = pd.read_excel(items_path, dtype=str)
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()
        
        print(f"✅ Archivo leído correctamente")
        print(f"📊 Columnas encontradas: {list(df.columns)}")
        print()
        
        # Buscar columna SKU
        possible_sku_columns = ['SKU', 'sku', 'Sku', 'CODIGO', 'codigo', 'Codigo', 'CODE', 'code', 'Code']
        col_sku = None
        
        for col_name in possible_sku_columns:
            if col_name in df.columns:
                col_sku = col_name
                break
        
        if not col_sku:
            # Buscar por coincidencia parcial
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['sku', 'codigo', 'code']):
                    col_sku = col
                    break
        
        if not col_sku:
            print(f"❌ No se encontró columna SKU en el archivo")
            print(f"💡 Columnas disponibles: {list(df.columns)}")
            return False
        
        # Buscar columna DESCRIPCION
        possible_desc_columns = ['DESCRIPCION', 'descripcion', 'Descripcion', 'DESC', 'desc', 
                                  'NOMBRE', 'nombre', 'Nombre', 'DESCRIPTION', 'description']
        col_desc = None
        
        for col_name in possible_desc_columns:
            if col_name in df.columns:
                col_desc = col_name
                break
        
        if not col_desc:
            # Buscar por coincidencia parcial
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['desc', 'nombre', 'name']):
                    col_desc = col
                    break
        
        print(f"✅ Columna SKU: {col_sku}")
        if col_desc:
            print(f"✅ Columna DESCRIPCION: {col_desc}")
        else:
            print(f"⚠️  No se encontró columna DESCRIPCION - se usará SKU como descripción")
        print()
        
        # Preparar datos para importación
        products_list = []
        
        for idx, row in df.iterrows():
            sku = str(row[col_sku]).strip().upper()
            
            # Saltar valores vacíos o inválidos
            if not sku or sku == 'NAN' or len(sku) == 0:
                continue
            
            # Obtener descripción
            if col_desc:
                descripcion = str(row[col_desc]).strip()
                if not descripcion or descripcion == 'nan':
                    descripcion = sku  # Usar SKU si no hay descripción
            else:
                descripcion = sku
            
            products_list.append((sku, descripcion))
        
        print(f"📦 Productos a importar: {len(products_list)}")
        
        if len(products_list) == 0:
            print(f"⚠️  No se encontraron productos válidos en el archivo")
            return False
        
        # Mostrar algunos ejemplos
        print(f"\n📋 Ejemplos de productos:")
        for sku, desc in products_list[:5]:
            print(f"   - {sku}: {desc}")
        if len(products_list) > 5:
            print(f"   ... y {len(products_list) - 5} más")
        
        # Confirmar importación
        print()
        respuesta = input("¿Deseas continuar con la importación? (s/n): ")
        
        if respuesta.lower() != 's':
            print("❌ Importación cancelada")
            return False
        
        # Inicializar ProductsManager
        print("\n📦 Iniciando importación...")
        products_manager = ProductsManager()
        
        # Importar productos
        resultado = products_manager.bulk_import(products_list)
        
        print()
        print("=" * 60)
        print("RESULTADO DE LA MIGRACIÓN")
        print("=" * 60)
        print(f"✅ Productos importados exitosamente: {resultado['added']}")
        print(f"⚠️  Productos duplicados (omitidos): {resultado['duplicates']}")
        print(f"❌ Errores durante importación: {resultado['errors']}")
        print()
        
        # Verificar productos importados
        stats = products_manager.get_stats()
        print(f"📊 Total de productos en sistema: {stats['total_products']}")
        print()
        
        # Crear backup del archivo original
        backup_path = items_path.replace(".xlsx", "_BACKUP.xlsx")
        if not os.path.exists(backup_path):
            import shutil
            shutil.copy(items_path, backup_path)
            print(f"💾 Backup creado: {backup_path}")
        
        print()
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("💡 Ahora puedes gestionar productos desde la app")
        print("   usando el botón '📦 Gestión de Productos'")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        migrate_items_xlsx()
    except KeyboardInterrupt:
        print("\n\n❌ Migración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPresiona ENTER para cerrar...")
