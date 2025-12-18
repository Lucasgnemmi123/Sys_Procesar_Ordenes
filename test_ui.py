#!/usr/bin/env python3
"""
Prueba rápida del sistema actualizado
Creado por Lucas Gnemmi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🎨 Probando el sistema actualizado...")
print("   • Tema moderno (colores púrpura y cyan)")
print("   • Textos en español")
print("   • Barra de progreso integrada")

try:
    import gui_moderna_v2
    print("✅ Importación exitosa")
    
    # Crear instancia de la GUI
    app = gui_moderna_v2.ModernGUI()
    
    print("🚀 Iniciando interfaz...")
    print("   • Ventana: 1400x900")
    print("   • Barra de progreso entre log y vista previa")
    print("   • Botones en español")
    
    # Iniciar el loop principal
    app.run()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()