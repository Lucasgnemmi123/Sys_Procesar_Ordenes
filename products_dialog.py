"""
Interfaz Gráfica para Gestión de Lista Maestra de Productos
Creado por Lucas Gnemmi
Versión: 1.0

Permite crear, editar y eliminar productos (SKU + DESCRIPCION)
Incluye carga masiva desde Excel con template
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from products_manager import ProductsManager
import os


class ProductsDialog:
    """Ventana de diálogo para gestionar lista maestra de productos"""
    
    def __init__(self, parent):
        """Inicializa la ventana de productos"""
        self.parent = parent
        self.products_manager = ProductsManager()
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title("📦 Gestión de Lista Maestra de Productos")
        self.window.geometry("1200x750")
        self.window.configure(bg="#f5f7fa")
        
        # Colores tema
        self.PRIMARY = "#1a237e"
        self.SECONDARY = "#3949ab"
        self.SUCCESS = "#2e7d32"
        self.WARNING = "#ef6c00"
        self.ERROR = "#c62828"
        self.WHITE = "#ffffff"
        self.LIGHT_GRAY = "#f5f7fa"
        
        # Inicializar estilos
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.configure_table_style()
        
        self.setup_ui()
        self.refresh_products()
    
    def configure_table_style(self):
        """Configura el estilo de la tabla"""
        self.style.configure('Products.Treeview',
            background='white',
            foreground='black',
            fieldbackground='white',
            bordercolor='black',
            borderwidth=1,
            rowheight=30,
            font=('Segoe UI', 9)
        )
        self.style.configure('Products.Treeview.Heading',
            background='#E1F5FE',
            foreground='#01579B',
            borderwidth=1,
            font=('Segoe UI', 10, 'bold'),
            relief='solid'
        )
        self.style.map('Products.Treeview',
            background=[('selected', '#B3E5FC')],
            foreground=[('selected', 'black')]
        )
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header
        header = tk.Frame(self.window, bg=self.PRIMARY, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header, 
            text="📦 LISTA MAESTRA DE PRODUCTOS", 
            font=("Segoe UI", 16, "bold"),
            fg=self.WHITE, 
            bg=self.PRIMARY
        ).pack(expand=True)
        
        # Main container
        main_frame = tk.Frame(self.window, bg=self.WHITE)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel de entrada manual
        self.create_input_panel(main_frame)
        
        # Panel de carga masiva
        self.create_bulk_panel(main_frame)
        
        # Panel de lista de productos
        self.create_list_panel(main_frame)
        
        # Panel de estadísticas
        self.create_stats_panel(main_frame)
    
    def create_input_panel(self, parent):
        """Crea el panel de entrada manual"""
        input_frame = tk.LabelFrame(
            parent, 
            text="➕ Agregar/Editar Producto Individual", 
            font=("Arial", 11, "bold"),
            bg=self.WHITE,
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Row 1: SKU y Descripción
        row1 = tk.Frame(input_frame, bg=self.WHITE)
        row1.pack(fill="x", pady=5)
        
        tk.Label(
            row1, 
            text="Código SKU:", 
            font=("Arial", 10, 'bold'), 
            bg=self.WHITE,
            width=15,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.sku_entry = tk.Entry(row1, font=("Arial", 10), width=20, relief='solid', bd=1, bg='#FAFAFA')
        self.sku_entry.pack(side="left", padx=5)
        
        tk.Label(
            row1, 
            text="Descripción:", 
            font=("Arial", 10, 'bold'), 
            bg=self.WHITE,
            width=15,
            anchor="w"
        ).pack(side="left", padx=(30, 5))
        
        self.desc_entry = tk.Entry(row1, font=("Arial", 10), width=60, relief='solid', bd=1, bg='#FAFAFA')
        self.desc_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botones
        btn_frame = tk.Frame(input_frame, bg=self.WHITE)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Agregar Producto",
            font=("Arial", 10, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.add_product,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="✏️ Actualizar Seleccionado",
            font=("Arial", 10, "bold"),
            bg=self.SECONDARY,
            fg=self.WHITE,
            command=self.update_selected,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)
    
    def create_bulk_panel(self, parent):
        """Crea el panel de carga masiva"""
        bulk_frame = tk.LabelFrame(
            parent, 
            text="📁 Carga Masiva desde Excel", 
            font=("Arial", 11, "bold"),
            bg=self.WHITE,
            padx=15,
            pady=15
        )
        bulk_frame.pack(fill="x", padx=10, pady=10)
        
        # Instrucciones
        tk.Label(
            bulk_frame,
            text="📋 El archivo Excel debe tener 2 columnas: SKU y DESCRIPCION (o CODIGO/CODE y DESC/NOMBRE/NAME)",
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.WARNING,
            justify="left"
        ).pack(anchor="w", pady=5)
        
        # Botones
        btn_frame = tk.Frame(bulk_frame, bg=self.WHITE)
        btn_frame.pack(pady=5)
        
        tk.Button(
            btn_frame,
            text="📥 Importar desde Excel",
            font=("Arial", 10, "bold"),
            bg=self.SECONDARY,
            fg=self.WHITE,
            command=self.import_from_excel,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📤 Exportar a Excel",
            font=("Arial", 10, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.export_to_excel,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📄 Descargar Template",
            font=("Arial", 10, "bold"),
            bg=self.WARNING,
            fg=self.WHITE,
            command=self.download_template,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(side="left", padx=5)
    
    def create_list_panel(self, parent):
        """Crea el panel de lista de productos"""
        list_frame = tk.LabelFrame(
            parent, 
            text="📋 Productos Registrados", 
            font=("Arial", 11, "bold"),
            bg=self.WHITE,
            padx=10,
            pady=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de búsqueda
        search_frame = tk.Frame(list_frame, bg=self.WHITE)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            font=("Arial", 10, 'bold'),
            bg=self.WHITE
        ).pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_products())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 10),
            width=40,
            relief='solid',
            bd=1,
            bg='#FAFAFA'
        )
        search_entry.pack(side="left", padx=5)
        
        # Treeview
        columns = ("SKU", "Descripción")
        self.products_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            height=15,
            style='Products.Treeview'
        )
        
        # Configurar columnas
        self.products_tree.heading("SKU", text="Código SKU")
        self.products_tree.heading("Descripción", text="Descripción del Producto")
        
        self.products_tree.column("SKU", width=150, anchor="center")
        self.products_tree.column("Descripción", width=600, anchor="w")
        
        # Configurar tags de filas alternadas
        self.products_tree.tag_configure('oddrow', background='#F5F5F5')
        self.products_tree.tag_configure('evenrow', background='white')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind doble click para cargar en campos de edición
        self.products_tree.bind('<Double-Button-1>', self.load_selected_to_edit)
        
        # Botones de acción
        btn_frame = tk.Frame(list_frame, bg=self.WHITE)
        btn_frame.pack(fill="x", pady=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Eliminar Seleccionado",
            font=("Arial", 10, "bold"),
            bg=self.ERROR,
            fg=self.WHITE,
            command=self.delete_selected,
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🔄 Recargar Lista",
            font=("Arial", 10, "bold"),
            bg=self.SECONDARY,
            fg=self.WHITE,
            command=self.refresh_products,
            cursor="hand2"
        ).pack(side="left", padx=5)
    
    def create_stats_panel(self, parent):
        """Crea el panel de estadísticas"""
        stats_frame = tk.Frame(parent, bg=self.WHITE)
        stats_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=("Arial", 9),
            bg=self.WHITE,
            fg=self.SECONDARY,
            anchor="w"
        )
        self.stats_label.pack(fill="x", padx=5)
    
    def add_product(self):
        """Agrega un nuevo producto"""
        sku = self.sku_entry.get().strip().upper()
        descripcion = self.desc_entry.get().strip()
        
        if not sku or not descripcion:
            messagebox.showwarning(
                "⚠️ Campos Incompletos",
                "Por favor ingrese el código SKU y la descripción.",
                parent=self.window
            )
            return
        
        if self.products_manager.add_product(sku, descripcion):
            messagebox.showinfo(
                "✅ Éxito",
                f"Producto agregado:\nSKU: {sku}\nDescripción: {descripcion}",
                parent=self.window
            )
            
            # Limpiar campos
            self.sku_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
            self.refresh_products()
        else:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo agregar el producto.\nEl SKU {sku} ya existe.",
                parent=self.window
            )
    
    def update_selected(self):
        """Actualiza el producto seleccionado"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning(
                "⚠️ Sin Selección",
                "Por favor seleccione un producto para actualizar.",
                parent=self.window
            )
            return
        
        sku = self.sku_entry.get().strip().upper()
        nueva_descripcion = self.desc_entry.get().strip()
        
        if not sku or not nueva_descripcion:
            messagebox.showwarning(
                "⚠️ Campos Incompletos",
                "Por favor ingrese el código SKU y la nueva descripción.",
                parent=self.window
            )
            return
        
        if self.products_manager.update_product(sku, nueva_descripcion):
            messagebox.showinfo(
                "✅ Éxito",
                f"Producto actualizado:\nSKU: {sku}",
                parent=self.window
            )
            
            # Limpiar campos
            self.sku_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
            self.refresh_products()
        else:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo actualizar el producto.\nEl SKU {sku} no existe.",
                parent=self.window
            )
    
    def delete_selected(self):
        """Elimina el producto seleccionado"""
        selection = self.products_tree.selection()
        if not selection:
            messagebox.showwarning(
                "⚠️ Sin Selección",
                "Por favor seleccione un producto para eliminar.",
                parent=self.window
            )
            return
        
        item = self.products_tree.item(selection[0])
        sku = item["values"][0]
        
        if messagebox.askyesno(
            "🗑️ Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el producto?\n\nSKU: {sku}",
            parent=self.window
        ):
            if self.products_manager.remove_product(sku):
                messagebox.showinfo("✅ Éxito", f"Producto eliminado: {sku}", parent=self.window)
                self.refresh_products()
            else:
                messagebox.showerror("❌ Error", "No se pudo eliminar el producto.", parent=self.window)
    
    def load_selected_to_edit(self, event=None):
        """Carga el producto seleccionado en los campos de edición"""
        selection = self.products_tree.selection()
        if not selection:
            return
        
        item = self.products_tree.item(selection[0])
        sku = item["values"][0]
        descripcion = item["values"][1]
        
        self.sku_entry.delete(0, tk.END)
        self.sku_entry.insert(0, sku)
        
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, descripcion)
    
    def search_products(self):
        """Busca productos según el texto de búsqueda"""
        query = self.search_var.get().strip()
        
        if not query:
            self.refresh_products()
            return
        
        # Limpiar tabla
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Buscar productos
        results = self.products_manager.search_products(query)
        
        for idx, product in enumerate(results):
            tag_fila = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.products_tree.insert(
                "", 
                "end", 
                values=(product["sku"], product["descripcion"]),
                tags=(tag_fila,)
            )
        
        # Actualizar stats
        self.update_stats(len(results))
    
    def refresh_products(self):
        """Actualiza la lista de productos"""
        # Limpiar tabla
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Cargar productos
        products = self.products_manager.get_all_products()
        
        for idx, product in enumerate(products):
            tag_fila = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.products_tree.insert(
                "", 
                "end", 
                values=(product["sku"], product["descripcion"]),
                tags=(tag_fila,)
            )
        
        # Actualizar stats
        self.update_stats(len(products))
    
    def update_stats(self, count=None):
        """Actualiza las estadísticas"""
        if count is None:
            stats = self.products_manager.get_stats()
            count = stats["total_products"]
        
        self.stats_label.config(text=f"📊 Total de Productos: {count}")
    
    def import_from_excel(self):
        """Importa productos desde un archivo Excel"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
            parent=self.window
        )
        
        if not file_path:
            return
        
        # Importar
        stats = self.products_manager.import_from_excel(file_path)
        
        # Mostrar resultados
        message = (
            f"📊 Importación Completada\n\n"
            f"✅ Total procesados: {stats['total']}\n"
            f"➕ Agregados: {stats['added']}\n"
            f"✏️ Actualizados: {stats['updated']}\n"
            f"⏭️ Omitidos: {stats['skipped']}\n"
        )
        
        if stats['errors']:
            message += f"\n❌ Errores:\n" + "\n".join(stats['errors'][:5])
        
        messagebox.showinfo("📥 Importación", message, parent=self.window)
        
        self.refresh_products()
    
    def export_to_excel(self):
        """Exporta productos a un archivo Excel"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar archivo Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="productos_exportados.xlsx",
            parent=self.window
        )
        
        if not file_path:
            return
        
        if self.products_manager.export_to_excel(file_path):
            messagebox.showinfo(
                "✅ Éxito",
                f"Productos exportados exitosamente:\n{file_path}",
                parent=self.window
            )
        else:
            messagebox.showerror(
                "❌ Error",
                "No se pudo exportar los productos.",
                parent=self.window
            )
    
    def download_template(self):
        """Descarga un template de Excel para carga masiva"""
        try:
            import pandas as pd
            
            file_path = filedialog.asksaveasfilename(
                title="Guardar template",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile="template_productos.xlsx",
                parent=self.window
            )
            
            if not file_path:
                return
            
            # Crear template con ejemplos
            df = pd.DataFrame({
                "SKU": ["EJEMPLO001", "EJEMPLO002", "EJEMPLO003"],
                "DESCRIPCION": [
                    "Producto de ejemplo 1",
                    "Producto de ejemplo 2",
                    "Producto de ejemplo 3"
                ]
            })
            
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            messagebox.showinfo(
                "✅ Éxito",
                f"Template descargado:\n{file_path}\n\n"
                f"📝 Elimina los ejemplos y agrega tus productos.\n"
                f"Las columnas requeridas son: SKU y DESCRIPCION",
                parent=self.window
            )
        except Exception as e:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo crear el template:\n{str(e)}",
                parent=self.window
            )
