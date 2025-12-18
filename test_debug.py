"""
Script de debugging para investigar los problemas del sistema
"""
import os
import pandas as pd
from procesamiento_v2 import procesar_pdfs, mapear_proveedor_por_sku, rellenar_fecha_entrega_y_observacion

def test_lectura_excel():
    """Test la lectura del Excel en Ordenes"""
    print("=" * 60)
    print("🔍 TESTING EXCEL READING")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ordenes_dir = os.path.join(base_dir, "Ordenes")
    
    print(f"📂 Directorio Ordenes: {ordenes_dir}")
    
    if not os.path.exists(ordenes_dir):
        print("❌ Directorio Ordenes no existe")
        return None
    
    # Listar archivos Excel
    excel_files = [f for f in os.listdir(ordenes_dir) if f.lower().endswith(('.xlsx', '.xls'))]
    print(f"📄 Archivos Excel encontrados: {excel_files}")
    
    if not excel_files:
        print("❌ No hay archivos Excel en Ordenes")
        return None
    
    # Procesar
    try:
        df = procesar_pdfs(ordenes_dir)
        print(f"✅ Registros procesados: {len(df)}")
        
        if len(df) > 0:
            print(f"📊 Columnas: {list(df.columns)}")
            print(f"📋 Primeros 5 registros:")
            print(df.head())
            
            # Verificar proveedores únicos si ya están mapeados
            if 'PROVEEDOR' in df.columns:
                print(f"🏭 Proveedores únicos: {len(df['PROVEEDOR'].unique())}")
                for prov in sorted(df['PROVEEDOR'].unique()):
                    count = len(df[df['PROVEEDOR'] == prov])
                    print(f"   • '{prov}': {count} registros")
        
        return df
        
    except Exception as e:
        print(f"❌ Error procesando Excel: {e}")
        return None

def test_mapeo_proveedores(df):
    """Test el mapeo de proveedores"""
    if df is None or len(df) == 0:
        print("⚠️ No hay datos para mapear proveedores")
        return None
        
    print("\n" + "=" * 60)
    print("🗺️ TESTING SUPPLIER MAPPING")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_xlsx = os.path.join(base_dir, "Full-Agenda", "Full.xlsx")
    
    print(f"📂 Archivo Full.xlsx: {full_xlsx}")
    
    if not os.path.exists(full_xlsx):
        print("❌ Full.xlsx no existe")
        return None
    
    try:
        df_mapped, df_errors, warnings = mapear_proveedor_por_sku(df, full_xlsx, "119")
        
        print(f"✅ Registros mapeados: {len(df_mapped)}")
        print(f"❌ Registros con errores: {len(df_errors)}")
        
        for warning in warnings:
            print(f"⚠️ {warning}")
        
        if len(df_mapped) > 0:
            print(f"🏭 Proveedores encontrados:")
            for prov in sorted(df_mapped['PROVEEDOR'].unique()):
                count = len(df_mapped[df_mapped['PROVEEDOR'] == prov])
                print(f"   • '{prov}': {count} registros")
        
        return df_mapped
        
    except Exception as e:
        print(f"❌ Error mapeando proveedores: {e}")
        return None

def test_agenda(df_mapped):
    """Test el procesamiento de la Agenda"""
    if df_mapped is None or len(df_mapped) == 0:
        print("⚠️ No hay datos para procesar Agenda")
        return None
        
    print("\n" + "=" * 60)
    print("📅 TESTING AGENDA PROCESSING")
    print("=" * 60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agenda_xlsm = os.path.join(base_dir, "Full-Agenda", "Agenda.xlsm")
    
    print(f"📂 Archivo Agenda.xlsm: {agenda_xlsm}")
    
    if not os.path.exists(agenda_xlsm):
        print("❌ Agenda.xlsm no existe")
        return None
    
    try:
        df_final, df_errors = rellenar_fecha_entrega_y_observacion(df_mapped, agenda_xlsm)
        
        print(f"✅ Registros finales: {len(df_final)}")
        print(f"❌ Registros con errores: {len(df_errors)}")
        
        if len(df_final) > 0:
            print(f"📋 Sample final records:")
            print(df_final[['SKU', 'PROVEEDOR', 'FECHA_ENTREGA', 'OBSERVACION']].head())
        
        if len(df_errors) > 0:
            print(f"❌ Sample error records:")
            print(df_errors[['SKU', 'PROVEEDOR', 'OBSERVACION']].head())
        
        return df_final, df_errors
        
    except Exception as e:
        print(f"❌ Error procesando Agenda: {e}")
        return None, None

def main():
    """Ejecutar todos los tests"""
    print("🚀 INICIANDO DEBUGGING DEL SISTEMA")
    
    # Test 1: Lectura Excel
    df = test_lectura_excel()
    
    # Test 2: Mapeo proveedores
    df_mapped = test_mapeo_proveedores(df)
    
    # Test 3: Agenda
    df_final, df_errors = test_agenda(df_mapped)
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    if df is not None:
        print(f"📄 Registros leídos del Excel: {len(df)}")
    if df_mapped is not None:
        print(f"🗺️ Registros con proveedor mapeado: {len(df_mapped)}")
    if df_final is not None:
        print(f"✅ Registros finales válidos: {len(df_final)}")
    if df_errors is not None:
        print(f"❌ Registros con errores: {len(df_errors)}")

if __name__ == "__main__":
    main()