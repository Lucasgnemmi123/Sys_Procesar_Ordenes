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
        
        # Crear un root de tkinter oculto si no existe
        try:
            root = tk._default_root
            if root is None:
                root = tk.Tk()
                root.withdraw()
        except:
            root = tk.Tk()
            root.withdraw()
        
        # Crear ventana independiente (compatible con customtkinter parent)
        self.window = tk.Toplevel()
        self.window.title("📦 Maestra C.Calzada")
        
        # IMPORTANTE: Forzar theme 'default' para SOBREESCRIBIR el 'clam' de gui_moderna_v2
        self.style = ttk.Style(self.window)
        self.style.theme_use('default')
        
        # Adaptar altura a la pantalla del usuario
        screen_height = self.window.winfo_screenheight()
        window_height = int(screen_height * 0.85)  # 85% de la altura de pantalla
        window_width = 1200
        
        # Centrar ventana
        x_position = int((self.window.winfo_screenwidth() - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        
        self.window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.window.configure(bg="#1a1d29")  # BG_DARK
        
        # Colores tema moderno (consistente con GUI principal)
        self.PRIMARY = "#00d4ff"      # PRIMARY
        self.PRIMARY_DARK = "#00b8d9" # PRIMARY_DARK
        self.SECONDARY = "#a78bfa"    # SECONDARY
        self.SUCCESS = "#34d399"      # SUCCESS
        self.WARNING = "#fbbf24"      # WARNING
        self.ERROR = "#f87171"        # ERROR
        self.WHITE = "#ffffff"        # TEXT_PRIMARY
        self.BG_DARK = "#1a1d29"      # BG_DARK
        self.BG_CARD = "#2d3142"      # BG_CARD
        self.BG_SURFACE = "#242837"   # BG_SURFACE
        self.LIGHT_GRAY = "#e5e7eb"   # TEXT_SECONDARY
        
        # Configurar estilos de tabla
        self.configure_table_style()
        
        self.setup_ui()
        self.refresh_products()
    
    def configure_table_style(self):
        """Configura el estilo de la tabla EXACTO de agenda_dialog.py"""
        self.style.configure('Bordered.Treeview',
            background='white',
            foreground='black',
            fieldbackground='white',
            bordercolor='black',
            borderwidth=1,
            rowheight=28,
            font=('Segoe UI', 9)
        )
        self.style.configure('Bordered.Treeview.Heading',
            background='#E3F2FD',
            foreground='#1976D2',
            borderwidth=1,
            font=('Segoe UI', 9, 'bold'),
            relief='solid'
        )
        self.style.map('Bordered.Treeview',
            background=[('selected', '#BBDEFB')],
            foreground=[('selected', 'black')]
        )
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header con tema moderno
        header = tk.Frame(self.window, bg=self.BG_CARD, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Frame para el título y botón de cerrar
        header_content = tk.Frame(header, bg=self.BG_CARD)
        header_content.pack(fill="both", expand=True, padx=20)
        
        # Título centrado
        tk.Label(
            header_content, 
            text="📦 MAESTRA C.CALZADA - PRODUCTOS", 
            font=("Segoe UI", 18, "bold"),  # Fuente más grande
            fg=self.PRIMARY,                # Color primario para el texto
            bg=self.BG_CARD                 # Fondo del card
        ).pack(side="left", expand=True)
        
        # Botón de cerrar
        close_btn = tk.Button(
            header_content,
            text="✕ Cerrar",
            font=("Segoe UI", 11, "bold"),
            bg=self.ERROR,
            fg=self.WHITE,
            border=0,
            cursor="hand2",
            relief="flat",
            padx=15,
            pady=5,
            command=self.window.destroy
        )
        close_btn.pack(side="right", pady=20)
        
        # Main container con fondo oscuro
        main_frame = tk.Frame(self.window, bg=self.BG_DARK)
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
            font=("Segoe UI", 12, "bold"),  # Fuente moderna más grande
            bg=self.BG_CARD,                # Fondo del card
            fg=self.WHITE,                  # Texto blanco
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Row 1: SKU y Descripción
        row1 = tk.Frame(input_frame, bg=self.BG_CARD)
        row1.pack(fill="x", pady=5)
        
        tk.Label(
            row1, 
            text="Código SKU:", 
            font=("Segoe UI", 11, 'bold'),  # Fuente moderna
            bg=self.BG_CARD,                # Fondo del card
            fg=self.WHITE,                  # Texto blanco
            width=15,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.sku_entry = tk.Entry(row1, font=("Segoe UI", 11), width=20, relief='solid', bd=1, 
                                  bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.sku_entry.pack(side="left", padx=5)
        
        tk.Label(
            row1, 
            text="Descripción:", 
            font=("Segoe UI", 11, 'bold'),  # Fuente moderna
            bg=self.BG_CARD,                # Fondo del card
            fg=self.WHITE,                  # Texto blanco
            width=15,
            anchor="w"
        ).pack(side="left", padx=(30, 5))
        
        self.desc_entry = tk.Entry(row1, font=("Segoe UI", 11), width=60, relief='solid', bd=1, 
                                   bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.desc_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botones
        btn_frame = tk.Frame(input_frame, bg=self.BG_CARD)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Agregar Producto",
            font=("Segoe UI", 9, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.add_product,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground=self.PRIMARY
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🔍 Verificar si Existe",
            font=("Segoe UI", 9, "bold"),
            bg=self.WARNING,
            fg=self.WHITE,
            command=self.check_if_exists,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground=self.PRIMARY
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 9, "bold"),
            bg="#757575",
            fg=self.WHITE,
            command=self.clear_fields,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground=self.BG_SURFACE
        ).pack(side="left", padx=5)
    
    def create_bulk_panel(self, parent):
        """Crea el panel de carga masiva"""
        bulk_frame = tk.LabelFrame(
            parent, 
            text="📁 Carga Masiva desde Excel", 
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_CARD,
            fg=self.WHITE,
            padx=15,
            pady=15
        )
        bulk_frame.pack(fill="x", padx=10, pady=10)
        
        # Instrucciones
        tk.Label(
            bulk_frame,
            text="📋 El archivo Excel debe tener 2 columnas: SKU y DESCRIPCION (o CODIGO/CODE y DESC/NOMBRE/NAME)",
            font=("Segoe UI", 10),
            bg=self.BG_CARD,
            fg=self.WARNING,
            justify="left"
        ).pack(anchor="w", pady=5)
        
        # Botones
        btn_frame = tk.Frame(bulk_frame, bg=self.BG_CARD)
        btn_frame.pack(pady=5)
        
        tk.Button(
            btn_frame,
            text="� Importar Template",
            font=("Segoe UI", 9, "bold"),
            bg=self.SECONDARY,
            fg=self.WHITE,
            command=self.import_from_excel,
            cursor="hand2",
            padx=12,
            pady=4,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground=self.PRIMARY
        ).pack(side="left", padx=8)
        
        tk.Button(
            btn_frame,
            text="📤 Exportar a Excel",
            font=("Segoe UI", 9, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.export_to_excel,
            cursor="hand2",
            padx=12,
            pady=4,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground="#22c55e"
        ).pack(side="left", padx=8)        
        # Botón para eliminar toda la maestra
        tk.Button(
            btn_frame,
            text="🗑️ Eliminar Toda la Maestra",
            font=("Segoe UI", 9, "bold"),
            bg="#dc2626",  # Rojo para eliminar
            fg=self.WHITE,
            command=self.eliminar_toda_maestra,
            cursor="hand2",
            padx=12,
            pady=4,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground="#b91c1c"
        ).pack(side="left", padx=8)        
        tk.Button(
            btn_frame,
            text="📄 Descargar Template",
            font=("Segoe UI", 9, "bold"),
            bg=self.WARNING,
            fg=self.WHITE,
            command=self.download_template,
            cursor="hand2",
            padx=12,
            pady=4,
            relief="flat",
            bd=0,
            highlightthickness=0,
            activebackground=self.PRIMARY
        ).pack(side="left", padx=8)
    
    def create_list_panel(self, parent):
        """Crea el panel de lista de productos"""
        list_frame = tk.LabelFrame(
            parent, 
            text="📋 Productos Registrados", 
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_CARD,
            fg=self.WHITE,
            padx=10,
            pady=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de búsqueda
        search_frame = tk.Frame(list_frame, bg=self.BG_CARD)
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            font=("Segoe UI", 11, 'bold'),
            bg=self.BG_CARD,
            fg=self.WHITE
        ).pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_products())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 11),
            width=40,
            relief='solid',
            bd=1,
            bg=self.BG_DARK,
            fg=self.WHITE,
            insertbackground=self.WHITE
        )
        search_entry.pack(side="left", padx=5)
        
        # Label de resultados de búsqueda
        self.search_result_label = tk.Label(
            search_frame,
            text="",
            font=("Segoe UI", 10, 'italic'),
            bg=self.BG_CARD,
            fg=self.SECONDARY
        )
        self.search_result_label.pack(side="left", padx=10)
        
        # Treeview
        columns = ("SKU", "Descripción")
        self.products_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            height=15,
            style='Bordered.Treeview'
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
        
        # Botón de acción centrado
        btn_frame = tk.Frame(list_frame, bg=self.WHITE)
        btn_frame.pack(fill="x", pady=5)
        
        # Frame centrador
        center_frame = tk.Frame(btn_frame, bg=self.WHITE)
        center_frame.pack(expand=True)
        
        tk.Button(
            center_frame,
            text="🗑️ Eliminar Seleccionado",
            font=("Segoe UI", 10, "bold"),
            bg=self.ERROR,
            fg=self.WHITE,
            command=self.delete_selected,
            cursor="hand2",
            padx=20,
            pady=8
        ).pack()
    
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
    
    def update_product_from_fields(self):
        """Actualiza el producto usando los campos del formulario"""
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
    
    def check_if_exists(self):
        """Verifica si un SKU existe y muestra información detallada"""
        sku = self.sku_entry.get().strip().upper()
        
        if not sku:
            messagebox.showwarning(
                "⚠️ Campo Vacío",
                "Por favor ingrese un código SKU para verificar.",
                parent=self.window
            )
            return
        
        producto = self.products_manager.get_product(sku)
        
        if producto:
            # El producto existe - mostrar información
            messagebox.showinfo(
                "✅ Producto Encontrado",
                f"El SKU ya existe en el sistema:\n\n"
                f"SKU: {producto['sku']}\n"
                f"Descripción: {producto['descripcion']}\n"
                f"Creado: {producto.get('created', 'N/A')}\n"
                f"Última actualización: {producto.get('updated', 'N/A')}",
                parent=self.window
            )
            
            # Buscar y seleccionar el producto en la tabla
            for item in self.products_tree.get_children():
                values = self.products_tree.item(item)["values"]
                if values[0] == sku:
                    self.products_tree.selection_set(item)
                    self.products_tree.see(item)
                    break
        else:
            # El producto NO existe
            respuesta = messagebox.askyesno(
                "❌ Producto No Encontrado",
                f"El SKU '{sku}' NO existe en el sistema.\n\n"
                f"¿Desea agregarlo ahora?",
                parent=self.window
            )
            
            if respuesta:
                # Mantener el SKU en el campo y enfocar descripción
                self.desc_entry.focus_set()
    
    def clear_fields(self):
        """Limpia todos los campos del formulario"""
        self.sku_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.sku_entry.focus_set()
    
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
            self.search_result_label.config(text="")
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
        
        # Actualizar label de resultados
        if len(results) == 0:
            self.search_result_label.config(text="❌ No se encontraron resultados", fg=self.ERROR)
        elif len(results) == 1:
            self.search_result_label.config(text=f"✅ 1 producto encontrado", fg=self.SUCCESS)
        else:
            self.search_result_label.config(text=f"✅ {len(results)} productos encontrados", fg=self.SUCCESS)
        
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

    def eliminar_toda_maestra(self):
        """Elimina toda la maestra de productos"""
        if messagebox.askyesno(
            "🗑️ Confirmar Eliminación", 
            "\u00bfEstá seguro de que desea eliminar TODA la maestra de productos?\n\nEsta acción NO se puede deshacer.",
            parent=self.window
        ):
            try:
                # Limpiar la lista de productos pero mantener estructura
                self.products_manager.products["products"].clear()
                
                # Guardar cambios usando el método del manager
                if self.products_manager.save_products():
                    # Actualizar la lista
                    self.refresh_products()
                    messagebox.showinfo(
                        "✅ Maestra Eliminada", 
                        "Toda la maestra de productos ha sido eliminada correctamente.",
                        parent=self.window
                    )
                else:
                    messagebox.showerror(
                        "Error", 
                        "No se pudieron guardar los cambios.", 
                        parent=self.window
                    )
            except Exception as e:
                messagebox.showerror(
                    "Error", 
                    f"No se pudo eliminar la maestra: {str(e)}", 
                    parent=self.window
                )
