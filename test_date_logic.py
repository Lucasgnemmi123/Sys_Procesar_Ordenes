#!/usr/bin/env python3
"""
Test script para verificar la lógica corregida de procesamiento de fechas
Created by Lucas Gnemmi - DHL Order Processing System
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Añadir ruta del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from procesamiento_v2 import rellenar_fecha_entrega_y_observacion
    print("✅ Function imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)

def test_date_processing():
    """Test the corrected date processing logic"""
    
    print("🧪 Testing date processing logic...")
    print("=" * 50)
    
    # Crear datos de prueba
    test_data = {
        'PROVEEDOR': ['PROVEEDOR_A', 'PROVEEDOR_B', 'PROVEEDOR_C'],
        'SKU': ['SKU001', 'SKU002', 'SKU003'],
        'CANTIDAD': [10, 20, 15],
        'CENTRO_COSTO': ['CD001', 'CD002', 'CD003'],
        'NOMBRE_LUGAR': ['OVIEDO', 'MADRID', 'BARCELONA']
    }
    
    df_test = pd.DataFrame(test_data)
    print(f"📊 Test data created: {len(df_test)} records")
    print(df_test)
    print()
    
    # Verificar archivos necesarios
    agenda_path = "Full-Agenda/Agenda.xlsm"
    
    if not os.path.exists(agenda_path):
        print(f"⚠️ WARNING: {agenda_path} not found")
        print("   This test will use fallback logic")
    else:
        print(f"✅ Found agenda file: {agenda_path}")
    
    print("\n🔄 Processing dates and observations...")
    
    try:
        # Ejecutar el procesamiento
        df_valid, df_errors = rellenar_fecha_entrega_y_observacion(df_test, agenda_path)
        
        print(f"\n📋 Results:")
        print(f"   Valid records: {len(df_valid)}")
        print(f"   Error records: {len(df_errors)}")
        
        if len(df_valid) > 0:
            print("\n✅ Valid records:")
            print(df_valid[['PROVEEDOR', 'FECHA_ENTREGA', 'OBSERVACION']])
        
        if len(df_errors) > 0:
            print("\n⚠️ Error records:")
            print(df_errors[['PROVEEDOR', 'OBSERVACION']])
        
        print("\n🎯 Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_date_processing()