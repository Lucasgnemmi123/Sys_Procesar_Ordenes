"""
Gestor de Lista Maestra de Productos
Creado por Lucas Gnemmi
Versión: 1.0

Maneja la lista maestra de productos (SKU + DESCRIPCION) en formato JSON.
Reemplaza la dependencia del archivo Items.xlsx
"""

import json
import os
from datetime import datetime


class ProductsManager:
    """Gestiona la lista maestra de productos (SKU + DESCRIPCION)"""
    
    def __init__(self, products_file="products.json"):
        """
        Inicializa el gestor de productos
        
        Args:
            products_file: Nombre del archivo JSON que almacena los productos
        """
        self.products_file = products_file
        self.products = self.load_products()
    
    def load_products(self):
        """Carga los productos desde el archivo JSON"""
        if not os.path.exists(self.products_file):
            # Crear archivo por defecto vacío
            default_products = {
                "products": [],
                "metadata": {
                    "total_count": 0,
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            self.save_products(default_products)
            return default_products
        
        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading products: {e}")
            return {
                "products": [],
                "metadata": {
                    "total_count": 0,
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
    
    def save_products(self, products_data=None):
        """Guarda los productos en el archivo JSON"""
        if products_data is None:
            products_data = self.products
        
        # Actualizar metadata
        products_data["metadata"]["total_count"] = len(products_data["products"])
        products_data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.products_file, 'w', encoding='utf-8') as f:
                json.dump(products_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving products: {e}")
            return False
    
    def add_product(self, sku, descripcion):
        """
        Agrega un nuevo producto
        
        Args:
            sku: Código SKU del producto
            descripcion: Descripción del producto
            
        Returns:
            bool: True si se agregó correctamente, False si ya existe
        """
        sku = str(sku).strip().upper()
        descripcion = str(descripcion).strip()
        
        if not sku or not descripcion:
            return False
        
        # Verificar si ya existe
        if self.product_exists(sku):
            return False
        
        # Agregar producto
        product = {
            "sku": sku,
            "descripcion": descripcion,
            "created": datetime.now().isoformat()
        }
        
        self.products["products"].append(product)
        self.save_products()
        return True
    
    def update_product(self, sku, nueva_descripcion):
        """
        Actualiza la descripción de un producto existente
        
        Args:
            sku: Código SKU del producto
            nueva_descripcion: Nueva descripción
            
        Returns:
            bool: True si se actualizó correctamente
        """
        sku = str(sku).strip().upper()
        
        for product in self.products["products"]:
            if product["sku"] == sku:
                product["descripcion"] = nueva_descripcion.strip()
                product["updated"] = datetime.now().isoformat()
                self.save_products()
                return True
        
        return False
    
    def remove_product(self, sku):
        """
        Elimina un producto
        
        Args:
            sku: Código SKU del producto a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
        """
        sku = str(sku).strip().upper()
        
        initial_count = len(self.products["products"])
        self.products["products"] = [
            p for p in self.products["products"] 
            if p["sku"] != sku
        ]
        
        if len(self.products["products"]) < initial_count:
            self.save_products()
            return True
        
        return False
    
    def product_exists(self, sku):
        """
        Verifica si un SKU existe en la lista
        
        Args:
            sku: Código SKU a verificar
            
        Returns:
            bool: True si existe
        """
        sku = str(sku).strip().upper()
        return any(p["sku"] == sku for p in self.products["products"])
    
    def get_product(self, sku):
        """
        Obtiene un producto por su SKU
        
        Args:
            sku: Código SKU
            
        Returns:
            dict: Datos del producto o None si no existe
        """
        sku = str(sku).strip().upper()
        
        for product in self.products["products"]:
            if product["sku"] == sku:
                return product
        
        return None
    
    def get_all_products(self):
        """
        Obtiene todos los productos
        
        Returns:
            list: Lista de todos los productos ordenados por SKU
        """
        return sorted(self.products["products"], key=lambda x: x["sku"])
    
    def get_all_skus(self):
        """
        Obtiene todos los SKUs como un set
        
        Returns:
            set: Set de todos los SKUs
        """
        return {p["sku"] for p in self.products["products"]}
    
    def search_products(self, query):
        """
        Busca productos por SKU o descripción
        
        Args:
            query: Texto a buscar
            
        Returns:
            list: Lista de productos que coinciden
        """
        query = query.strip().upper()
        
        results = []
        for product in self.products["products"]:
            if query in product["sku"] or query in product["descripcion"].upper():
                results.append(product)
        
        return sorted(results, key=lambda x: x["sku"])
    
    def bulk_import(self, products_list):
        """
        Importación masiva de productos
        
        Args:
            products_list: Lista de tuplas (sku, descripcion)
            
        Returns:
            dict: Estadísticas de la importación
        """
        stats = {
            "total": len(products_list),
            "added": 0,
            "updated": 0,
            "skipped": 0,
            "errors": []
        }
        
        for sku, descripcion in products_list:
            try:
                sku = str(sku).strip().upper()
                descripcion = str(descripcion).strip()
                
                if not sku or not descripcion or sku == "NAN" or descripcion == "NAN":
                    stats["skipped"] += 1
                    continue
                
                if self.product_exists(sku):
                    # Actualizar existente
                    self.update_product(sku, descripcion)
                    stats["updated"] += 1
                else:
                    # Agregar nuevo
                    if self.add_product(sku, descripcion):
                        stats["added"] += 1
                    else:
                        stats["skipped"] += 1
                        
            except Exception as e:
                stats["errors"].append(f"Error with SKU {sku}: {str(e)}")
        
        return stats
    
    def export_to_excel(self, output_path):
        """
        Exporta la lista de productos a Excel
        
        Args:
            output_path: Ruta del archivo Excel de salida
            
        Returns:
            bool: True si se exportó correctamente
        """
        try:
            import pandas as pd
            
            df = pd.DataFrame(self.products["products"])
            df = df[["sku", "descripcion"]]  # Solo columnas relevantes
            df.columns = ["SKU", "DESCRIPCION"]
            
            df.to_excel(output_path, index=False, engine='openpyxl')
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
    
    def import_from_excel(self, excel_path):
        """
        Importa productos desde un archivo Excel
        
        Args:
            excel_path: Ruta del archivo Excel
            
        Returns:
            dict: Estadísticas de la importación
        """
        try:
            import pandas as pd
            
            # Leer Excel
            df = pd.read_excel(excel_path, dtype=str)
            df.columns = df.columns.str.strip().str.upper()
            
            # Buscar columnas SKU y DESCRIPCION
            sku_col = None
            desc_col = None
            
            for col in df.columns:
                if col in ['SKU', 'CODIGO', 'CODE']:
                    sku_col = col
                if col in ['DESCRIPCION', 'DESCRIPTION', 'DESC', 'NOMBRE', 'NAME']:
                    desc_col = col
            
            if not sku_col or not desc_col:
                return {
                    "total": 0,
                    "added": 0,
                    "updated": 0,
                    "skipped": 0,
                    "errors": [f"Required columns not found. Available: {list(df.columns)}"]
                }
            
            # Preparar lista de productos
            products_list = list(zip(df[sku_col], df[desc_col]))
            
            # Importar masivamente
            return self.bulk_import(products_list)
            
        except Exception as e:
            return {
                "total": 0,
                "added": 0,
                "updated": 0,
                "skipped": 0,
                "errors": [f"Error importing from Excel: {str(e)}"]
            }
    
    def clear_all(self):
        """Elimina todos los productos (con confirmación)"""
        self.products["products"] = []
        self.save_products()
        return True
    
    def get_stats(self):
        """
        Obtiene estadísticas de la lista de productos
        
        Returns:
            dict: Estadísticas
        """
        return {
            "total_products": len(self.products["products"]),
            "last_updated": self.products["metadata"].get("last_updated", "N/A"),
            "version": self.products["metadata"].get("version", "1.0")
        }
