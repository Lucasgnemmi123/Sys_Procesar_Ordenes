"""
Sistema de Gestión de Reglas Especiales
Created by Lucas Gnemmi
Version: 1.0

Maneja dos tipos de reglas:
1. Reglas de LOCAL → Proveedor forzado
2. Reglas de Bloqueo por Quiebre de Stock (SKU + Proveedor)
"""

import json
import os
from datetime import datetime

class RulesManager:
    """Gestiona las reglas especiales del sistema"""
    
    def __init__(self, rules_file="rules.json"):
        """Inicializa el gestor de reglas"""
        self.rules_file = rules_file
        self.rules = self.load_rules()
        
    def load_rules(self):
        """Carga las reglas desde el archivo JSON"""
        if not os.path.exists(self.rules_file):
            # Crear archivo con estructura inicial
            default_rules = {
                "local_rules": [],
                "stock_blocks": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            self.save_rules(default_rules)
            return default_rules
        
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading rules: {e}")
            return {
                "local_rules": [],
                "stock_blocks": [],
                "metadata": {"error": str(e)}
            }
    
    def save_rules(self, rules=None):
        """Guarda las reglas en el archivo JSON"""
        if rules is None:
            rules = self.rules
        
        try:
            rules["metadata"]["last_updated"] = datetime.now().isoformat()
            
            with open(self.rules_file, 'w', encoding='utf-8') as f:
                json.dump(rules, f, indent=4, ensure_ascii=False)
            
            print(f"✅ Rules saved successfully to {self.rules_file}")
            return True
        except Exception as e:
            print(f"❌ Error saving rules: {e}")
            return False
    
    # --- REGLAS DE LOCAL + SKU → PROVEEDOR ---
    
    def add_local_rule(self, local_code, sku, proveedor_code, descripcion=""):
        """
        Agrega una regla: LOCAL + SKU específico solo usa PROVEEDOR específico
        
        Args:
            local_code: Código del local (ej: "12345")
            sku: Código del SKU/producto (ej: "A12345")
            proveedor_code: Código del proveedor forzado (ej: "77300")
            descripcion: Descripción opcional de la regla
        """
        # Validar que no exista ya
        for rule in self.rules["local_rules"]:
            if rule["local"] == str(local_code) and rule["sku"] == str(sku).upper():
                print(f"⚠️ Rule already exists for LOCAL {local_code} + SKU {sku}")
                return False
        
        new_rule = {
            "local": str(local_code),
            "sku": str(sku).upper(),
            "proveedor": str(proveedor_code),
            "descripcion": descripcion,
            "created": datetime.now().isoformat(),
            "active": True
        }
        
        self.rules["local_rules"].append(new_rule)
        self.save_rules()
        print(f"✅ LOCAL rule added: LOCAL {local_code} + SKU {sku} → Proveedor {proveedor_code}")
        return True
    
    def remove_local_rule(self, local_code, sku):
        """Elimina una regla de LOCAL + SKU"""
        initial_count = len(self.rules["local_rules"])
        self.rules["local_rules"] = [
            r for r in self.rules["local_rules"] 
            if not (r["local"] == str(local_code) and r["sku"] == str(sku).upper())
        ]
        
        if len(self.rules["local_rules"]) < initial_count:
            self.save_rules()
            print(f"✅ LOCAL rule removed: LOCAL {local_code} + SKU {sku}")
            return True
        
        print(f"⚠️ LOCAL rule not found: LOCAL {local_code} + SKU {sku}")
        return False
    
    def get_local_rules(self):
        """Obtiene todas las reglas de LOCAL"""
        return self.rules.get("local_rules", [])
    
    def get_proveedor_for_local_sku(self, local_code, sku):
        """
        Obtiene el proveedor forzado para un LOCAL + SKU específico
        
        Args:
            local_code: Código del local
            sku: Código del SKU
            
        Returns:
            str: Código de proveedor si existe regla, None si no
        """
        for rule in self.rules.get("local_rules", []):
            if (rule.get("active", True) and 
                rule["local"] == str(local_code) and 
                rule["sku"] == str(sku).upper()):
                return rule["proveedor"]
        return None
    
    # --- REGLAS DE BLOQUEO POR QUIEBRE DE STOCK ---
    
    def add_stock_block(self, sku, proveedor_code, motivo="Quiebre de stock"):
        """
        Agrega un bloqueo: SKU + Proveedor no debe generar orden
        
        Args:
            sku: Código del material (ej: "A12345")
            proveedor_code: Código del proveedor bloqueado (ej: "77300")
            motivo: Motivo del bloqueo
        """
        # Validar que no exista ya
        for block in self.rules["stock_blocks"]:
            if block["sku"] == str(sku).upper() and block["proveedor"] == str(proveedor_code):
                print(f"⚠️ Block already exists for SKU {sku} + Proveedor {proveedor_code}")
                return False
        
        new_block = {
            "sku": str(sku).upper(),
            "proveedor": str(proveedor_code),
            "motivo": motivo,
            "created": datetime.now().isoformat(),
            "active": True
        }
        
        self.rules["stock_blocks"].append(new_block)
        self.save_rules()
        print(f"✅ Stock block added: SKU {sku} + Proveedor {proveedor_code}")
        return True
    
    def remove_stock_block(self, sku, proveedor_code):
        """Elimina un bloqueo de stock"""
        initial_count = len(self.rules["stock_blocks"])
        self.rules["stock_blocks"] = [
            b for b in self.rules["stock_blocks"] 
            if not (b["sku"] == str(sku).upper() and b["proveedor"] == str(proveedor_code))
        ]
        
        if len(self.rules["stock_blocks"]) < initial_count:
            self.save_rules()
            print(f"✅ Stock block removed: SKU {sku} + Proveedor {proveedor_code}")
            return True
        
        print(f"⚠️ Stock block not found: SKU {sku} + Proveedor {proveedor_code}")
        return False
    
    def get_stock_blocks(self):
        """Obtiene todos los bloqueos de stock"""
        return self.rules.get("stock_blocks", [])
    
    def is_blocked(self, sku, proveedor_code):
        """
        Verifica si una combinación SKU + Proveedor está bloqueada
        
        Returns:
            bool: True si está bloqueado, False si no
        """
        for block in self.rules.get("stock_blocks", []):
            if (block.get("active", True) and 
                block["sku"] == str(sku).upper() and 
                block["proveedor"] == str(proveedor_code)):
                return True
        return False
    
    def get_blocked_proveedores_for_sku(self, sku):
        """
        Obtiene lista de proveedores bloqueados para un SKU
        
        Returns:
            list: Lista de códigos de proveedor bloqueados
        """
        blocked = []
        for block in self.rules.get("stock_blocks", []):
            if block.get("active", True) and block["sku"] == str(sku).upper():
                blocked.append(block["proveedor"])
        return blocked
    
    # --- UTILIDADES ---
    
    def get_stats(self):
        """Obtiene estadísticas de las reglas"""
        local_rules = self.get_local_rules()
        stock_blocks = self.get_stock_blocks()
        
        return {
            "total_local_rules": len(local_rules),
            "active_local_rules": len([r for r in local_rules if r.get("active", True)]),
            "total_stock_blocks": len(stock_blocks),
            "active_stock_blocks": len([b for b in stock_blocks if b.get("active", True)])
        }
    
    def clear_all_rules(self):
        """Limpia todas las reglas (con confirmación)"""
        self.rules["local_rules"] = []
        self.rules["stock_blocks"] = []
        self.save_rules()
        print("✅ All rules cleared")
    
    def export_rules(self, filename):
        """Exporta las reglas a un archivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.rules, f, indent=4, ensure_ascii=False)
            print(f"✅ Rules exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error exporting rules: {e}")
            return False
    
    def import_rules(self, filename):
        """Importa reglas desde un archivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_rules = json.load(f)
            
            # Validar estructura
            if "local_rules" in imported_rules and "stock_blocks" in imported_rules:
                self.rules = imported_rules
                self.save_rules()
                print(f"✅ Rules imported from {filename}")
                return True
            else:
                print("❌ Invalid rules file format")
                return False
        except Exception as e:
            print(f"❌ Error importing rules: {e}")
            return False
    
    def export_to_excel(self, filename):
        """Exporta las reglas a un archivo Excel para edición masiva"""
        try:
            import pandas as pd
            
            # Crear DataFrames
            df_local = pd.DataFrame(self.rules.get("local_rules", []))
            df_stock = pd.DataFrame(self.rules.get("stock_blocks", []))
            
            # Si están vacíos, crear con columnas
            if df_local.empty:
                df_local = pd.DataFrame(columns=["local", "sku", "proveedor", "descripcion", "active"])
            if df_stock.empty:
                df_stock = pd.DataFrame(columns=["sku", "proveedor", "motivo", "active"])
            
            # Guardar en Excel con dos hojas
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df_local.to_excel(writer, sheet_name='LOCAL_SKU_Rules', index=False)
                df_stock.to_excel(writer, sheet_name='Stock_Blocks', index=False)
                
                # Agregar hoja de instrucciones
                instrucciones = pd.DataFrame({
                    'INSTRUCCIONES': [
                        '=== REGLAS LOCAL + SKU ===',
                        'Editar en hoja "LOCAL_SKU_Rules"',
                        'Columnas requeridas:',
                        '  - local: Código del local (ej: 12345)',
                        '  - sku: Código del producto (ej: A12345)',
                        '  - proveedor: Código del proveedor forzado (ej: 77300)',
                        '  - descripcion: Descripción opcional',
                        '  - active: true/false (dejar vacío = true)',
                        '',
                        '=== BLOQUEOS DE STOCK ===',
                        'Editar en hoja "Stock_Blocks"',
                        'Columnas requeridas:',
                        '  - sku: Código del producto (ej: A12345)',
                        '  - proveedor: Código del proveedor a bloquear (ej: 77300)',
                        '  - motivo: Razón del bloqueo',
                        '  - active: true/false (dejar vacío = true)',
                        '',
                        '=== IMPORTANTE ===',
                        '1. NO modificar las columnas "created"',
                        '2. Después de editar, guardar y usar "Importar desde Excel"',
                        '3. Las reglas duplicadas serán ignoradas'
                    ]
                })
                instrucciones.to_excel(writer, sheet_name='INSTRUCCIONES', index=False)
            
            print(f"✅ Rules exported to Excel: {filename}")
            return True
        except ImportError:
            print("❌ pandas no está instalado. Se necesita para exportar a Excel.")
            return False
        except Exception as e:
            print(f"❌ Error exporting to Excel: {e}")
            return False
    
    def import_from_excel(self, filename, merge=True):
        """
        Importa reglas desde un archivo Excel
        
        Args:
            filename: Ruta del archivo Excel
            merge: Si True, fusiona con reglas existentes. Si False, reemplaza.
        
        Returns:
            dict: Estadísticas de importación
        """
        try:
            import pandas as pd
            
            stats = {
                "local_rules_added": 0,
                "local_rules_skipped": 0,
                "stock_blocks_added": 0,
                "stock_blocks_skipped": 0,
                "errors": []
            }
            
            # Leer Excel
            try:
                df_local = pd.read_excel(filename, sheet_name='LOCAL_SKU_Rules')
            except:
                df_local = pd.DataFrame()
                stats["errors"].append("No se encontró hoja 'LOCAL_SKU_Rules'")
            
            try:
                df_stock = pd.read_excel(filename, sheet_name='Stock_Blocks')
            except:
                df_stock = pd.DataFrame()
                stats["errors"].append("No se encontró hoja 'Stock_Blocks'")
            
            # Si no es merge, limpiar reglas existentes
            if not merge:
                self.rules["local_rules"] = []
                self.rules["stock_blocks"] = []
            
            # Importar reglas LOCAL + SKU
            if not df_local.empty and 'local' in df_local.columns and 'sku' in df_local.columns:
                for _, row in df_local.iterrows():
                    try:
                        local = str(row['local']).strip()
                        sku = str(row['sku']).strip().upper()
                        proveedor = str(row['proveedor']).strip()
                        descripcion = str(row.get('descripcion', '')).strip()
                        active = row.get('active', True)
                        
                        # Convertir 'true'/'false' strings a boolean
                        if isinstance(active, str):
                            active = active.lower() in ['true', '1', 'yes', 'sí', 'si']
                        
                        # Verificar si ya existe
                        exists = False
                        for rule in self.rules["local_rules"]:
                            if rule["local"] == local and rule["sku"] == sku:
                                exists = True
                                stats["local_rules_skipped"] += 1
                                break
                        
                        if not exists:
                            new_rule = {
                                "local": local,
                                "sku": sku,
                                "proveedor": proveedor,
                                "descripcion": descripcion,
                                "created": datetime.now().isoformat(),
                                "active": active
                            }
                            self.rules["local_rules"].append(new_rule)
                            stats["local_rules_added"] += 1
                    except Exception as e:
                        stats["errors"].append(f"Error en LOCAL rule fila {_}: {e}")
            
            # Importar bloqueos de stock
            if not df_stock.empty and 'sku' in df_stock.columns and 'proveedor' in df_stock.columns:
                for _, row in df_stock.iterrows():
                    try:
                        sku = str(row['sku']).strip().upper()
                        proveedor = str(row['proveedor']).strip()
                        motivo = str(row.get('motivo', '')).strip()
                        active = row.get('active', True)
                        
                        # Convertir 'true'/'false' strings a boolean
                        if isinstance(active, str):
                            active = active.lower() in ['true', '1', 'yes', 'sí', 'si']
                        
                        # Verificar si ya existe
                        exists = False
                        for block in self.rules["stock_blocks"]:
                            if block["sku"] == sku and block["proveedor"] == proveedor:
                                exists = True
                                stats["stock_blocks_skipped"] += 1
                                break
                        
                        if not exists:
                            new_block = {
                                "sku": sku,
                                "proveedor": proveedor,
                                "motivo": motivo,
                                "created": datetime.now().isoformat(),
                                "active": active
                            }
                            self.rules["stock_blocks"].append(new_block)
                            stats["stock_blocks_added"] += 1
                    except Exception as e:
                        stats["errors"].append(f"Error en Stock Block fila {_}: {e}")
            
            # Guardar cambios
            self.save_rules()
            
            print(f"✅ Import completed:")
            print(f"   • LOCAL rules added: {stats['local_rules_added']}")
            print(f"   • LOCAL rules skipped: {stats['local_rules_skipped']}")
            print(f"   • Stock blocks added: {stats['stock_blocks_added']}")
            print(f"   • Stock blocks skipped: {stats['stock_blocks_skipped']}")
            if stats['errors']:
                print(f"   ⚠️ Errors: {len(stats['errors'])}")
            
            return stats
            
        except ImportError:
            print("❌ pandas y openpyxl no están instalados.")
            return {"error": "pandas/openpyxl not installed"}
        except Exception as e:
            print(f"❌ Error importing from Excel: {e}")
            return {"error": str(e)}


# Función de prueba
if __name__ == "__main__":
    print("🔧 Testing Rules Manager...")
    
    rm = RulesManager("test_rules.json")
    
    # Probar reglas de LOCAL + SKU
    print("\n--- Testing LOCAL + SKU Rules ---")
    rm.add_local_rule("12345", "A12345", "77300", "Centro Distribución Principal - Producto A12345")
    rm.add_local_rule("67890", "A67890", "55500", "Bodega Secundaria - Producto A67890")
    
    print(f"Proveedor for LOCAL 12345 + SKU A12345: {rm.get_proveedor_for_local_sku('12345', 'A12345')}")
    print(f"Proveedor for LOCAL 12345 + SKU A99999: {rm.get_proveedor_for_local_sku('12345', 'A99999')}")
    print(f"Proveedor for LOCAL 99999 + SKU A12345: {rm.get_proveedor_for_local_sku('99999', 'A12345')}")
    
    # Probar bloqueos de stock
    print("\n--- Testing Stock Blocks ---")
    rm.add_stock_block("A12345", "77300", "Sin stock hasta enero 2026")
    rm.add_stock_block("A67890", "55500", "Producto descontinuado")
    
    print(f"Is A12345 + 77300 blocked? {rm.is_blocked('A12345', '77300')}")
    print(f"Is A12345 + 99999 blocked? {rm.is_blocked('A12345', '99999')}")
    
    # Estadísticas
    print("\n--- Stats ---")
    stats = rm.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n✅ Test completed!")
