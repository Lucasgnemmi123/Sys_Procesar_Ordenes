"""
Interfaz Gráfica para Gestión de Reglas Especiales
Created by Lucas Gnemmi
Version: 1.0

Permite crear, editar y eliminar reglas especiales:
1. Reglas de LOCAL → Proveedor forzado
2. Reglas de Bloqueo por Quiebre de Stock
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from rules_manager import RulesManager

class RulesDialog:
    """Ventana de diálogo para gestionar reglas especiales"""
    
    def __init__(self, parent):
        """Inicializa la ventana de reglas"""
        self.parent = parent
        self.rules_manager = RulesManager()
        
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
        self.window.title("⚙️ Gestión de Reglas Especiales")
        
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
        
        # Inicializar estilos de tablas
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.configure_table_styles()
        
        self.setup_ui()
        self.refresh_all()
    
    def configure_table_styles(self):
        """Configura los estilos para las tablas y pestañas del diálogo con tema moderno"""
        # ============ ESTILOS DE PESTAÑAS (NOTEBOOK) ============
        # Configurar estilo personalizado para el Notebook
        self.style.configure('Rules.TNotebook',
            background=self.BG_DARK,      # Fondo oscuro
            borderwidth=0,
            tabmargins=[5, 5, 5, 0]
        )
        
        # Estilo para las pestañas (tabs)
        self.style.configure('Rules.TNotebook.Tab',
            background=self.BG_SURFACE,   # Fondo superficie cuando no está seleccionada
            foreground=self.WHITE,        # Texto blanco
            padding=[15, 8],              # Espacio interno moderado
            font=('Segoe UI', 11, 'bold'),# Fuente más grande
            borderwidth=1,
            relief='flat'                 # Sin relieve
        )
        
        # Estilo cuando el mouse pasa sobre la pestaña
        self.style.map('Rules.TNotebook.Tab',
            background=[
                ('selected', self.PRIMARY),    # Color primario cuando está seleccionada
                ('active', self.SECONDARY)     # Color secundario cuando el mouse está encima
            ],
            foreground=[
                ('selected', '#000000'),       # Texto negro cuando está seleccionada (mejor contraste)
                ('active', self.WHITE)         # Texto blanco cuando el mouse está encima
            ],
            relief=[
                ('selected', 'flat'),  # Sin relieve cuando está seleccionada
                ('!selected', 'raised')  # Con relieve cuando no está seleccionada
            ],
            borderwidth=[
                ('selected', 3),  # Borde más grueso cuando está seleccionada
                ('!selected', 2)
            ]
        )
        
        # ============ ESTILOS DE TABLAS ============
        # Estilo para tabla de reglas LOCAL
        self.style.configure('LocalRules.Treeview',
            background=self.WHITE,        # Fondo blanco para legibilidad
            foreground='#2c3e50',         # Texto azul oscuro
            fieldbackground=self.WHITE,   # Campo blanco
            bordercolor='#bdc3c7',        # Borde gris claro
            borderwidth=2,                # Borde más grueso
            rowheight=35,                 # Filas más altas
            font=('Segoe UI', 12)         # Fuente más grande
        )
        self.style.configure('LocalRules.Treeview.Heading',
            background=self.SUCCESS,      # Header verde para reglas
            foreground=self.WHITE,        # Texto blanco
            borderwidth=2,                # Borde más grueso
            font=('Segoe UI', 13, 'bold'), # Header más grande
            relief='flat'                 # Sin relieve
        )
        self.style.map('LocalRules.Treeview',
            background=[('selected', self.SUCCESS)], # Selección con verde
            foreground=[('selected', self.WHITE)]   # Texto blanco al seleccionar
        )
        
        # Estilo para tabla de bloqueos de stock
        self.style.configure('StockBlocks.Treeview',
            background=self.WHITE,        # Fondo blanco para legibilidad
            foreground='#2c3e50',         # Texto azul oscuro
            fieldbackground=self.WHITE,   # Campo blanco
            bordercolor='#bdc3c7',        # Borde gris claro
            borderwidth=2,                # Borde más grueso
            rowheight=35,                 # Filas más altas
            font=('Segoe UI', 12)         # Fuente más grande
        )
        self.style.configure('StockBlocks.Treeview.Heading',
            background=self.ERROR,        # Header rojo para bloqueos
            foreground=self.WHITE,        # Texto blanco
            borderwidth=2,                # Borde más grueso
            font=('Segoe UI', 13, 'bold'), # Header más grande
            relief='flat'                 # Sin relieve
        )
        self.style.map('StockBlocks.Treeview',
            background=[('selected', self.ERROR)], # Selección con rojo
            foreground=[('selected', self.WHITE)]  # Texto blanco al seleccionar
        )
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Header con tema moderno y botón cerrar
        header = tk.Frame(self.window, bg=self.BG_CARD, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Frame para organizar título y botón cerrar
        header_content = tk.Frame(header, bg=self.BG_CARD)
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(
            header_content, 
            text="⚙️ REGLAS ESPECIALES", 
            font=("Segoe UI", 18, "bold"),  # Fuente más grande
            fg=self.PRIMARY,                # Color primario para el texto
            bg=self.BG_CARD                 # Fondo del card
        ).pack(side="left")
        
        # Botón cerrar
        close_btn = tk.Button(
            header_content,
            text="✕ Cerrar",
            command=self.window.destroy,
            bg=self.ERROR,              # Fondo rojo
            fg=self.WHITE,              # Texto blanco
            font=("Segoe UI", 12, "bold"),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=5
        )
        close_btn.pack(side="right")
        
        # Notebook para tabs con estilo personalizado
        self.notebook = ttk.Notebook(self.window, style='Rules.TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Reglas de LOCAL + SKU
        self.tab_local = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(self.tab_local, text="📍 Reglas de LOCAL + SKU → Proveedor")
        
        # Tab 2: Bloqueos de Stock
        self.tab_stock = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(self.tab_stock, text="🚫 Bloqueos por Quiebre de Stock")
        
        # Tab 3: Gestión de reglas
        self.tab_stats = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(self.tab_stats, text="⚙️ Gestión de reglas")
        
        # Configurar cada tab
        self.setup_local_tab()
        self.setup_stock_tab()
        self.setup_stats_tab()
        
    # --- TAB 1: REGLAS DE LOCAL ---
    
    def setup_local_tab(self):
        """Configura el tab de reglas de LOCAL"""
        # Panel de entrada con tema oscuro
        input_frame = tk.LabelFrame(
            self.tab_local, 
            text="➕ Agregar Nueva Regla: LOCAL + SKU → Proveedor", 
            font=("Segoe UI", 12, "bold"),  # Fuente moderna
            bg=self.BG_CARD,                # Fondo oscuro
            fg=self.WHITE,                  # Texto blanco
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Campos - Fila 1: LOCAL y SKU
        row1 = tk.Frame(input_frame, bg=self.BG_CARD)
        row1.pack(fill="x", pady=5)
        
        tk.Label(
            row1, 
            text="Código LOCAL:", 
            font=("Segoe UI", 11), 
            bg=self.BG_CARD,      # Fondo del card
            fg=self.WHITE,        # Texto blanco
            width=18,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.local_entry = tk.Entry(row1, font=("Segoe UI", 11), width=12, relief='solid', bd=1, 
                                    bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.local_entry.pack(side="left", padx=5)
        
        tk.Label(
            row1, 
            text="+", 
            font=("Segoe UI", 14, "bold"), 
            bg=self.BG_CARD,      # Fondo del card
            fg=self.WHITE         # Texto blanco
        ).pack(side="left", padx=10)
        
        tk.Label(
            row1, 
            text="Código SKU:", 
            font=("Segoe UI", 11), 
            bg=self.BG_CARD,
            fg=self.WHITE,
            width=15,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.local_sku_entry = tk.Entry(row1, font=("Segoe UI", 11), width=12, relief='solid', bd=1, 
                                        bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.local_sku_entry.pack(side="left", padx=5)
        
        # Fila 2: Proveedor
        row1b = tk.Frame(input_frame, bg=self.BG_CARD)
        row1b.pack(fill="x", pady=5)
        
        tk.Label(
            row1b, 
            text="→", 
            font=("Segoe UI", 14, "bold"), 
            bg=self.BG_CARD,
            fg=self.PRIMARY
        ).pack(side="left", padx=5)
        
        tk.Label(
            row1b, 
            text="Código Proveedor:", 
            font=("Segoe UI", 11), 
            bg=self.BG_CARD,
            fg=self.WHITE,
            width=18,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.local_prov_entry = tk.Entry(row1b, font=("Segoe UI", 11), width=15, relief='solid', bd=1, 
                                         bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.local_prov_entry.pack(side="left", padx=5)
        
        # Descripción
        row2 = tk.Frame(input_frame, bg=self.BG_CARD)
        row2.pack(fill="x", pady=5)
        
        tk.Label(
            row2, 
            text="Descripción (opcional):", 
            font=("Segoe UI", 11), 
            bg=self.BG_CARD,
            fg=self.WHITE,
            width=20,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.local_desc_entry = tk.Entry(row2, font=("Segoe UI", 11), width=50, relief='solid', bd=1, 
                                         bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.local_desc_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botón agregar
        tk.Button(
            input_frame,
            text="➕ Agregar Regla",
            font=("Segoe UI", 9, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.add_local_rule,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            activebackground=self.PRIMARY
        ).pack(pady=10)
        
        # Lista de reglas existentes
        list_frame = tk.LabelFrame(
            self.tab_local, 
            text="📋 Reglas Activas", 
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_CARD,
            fg=self.WHITE,
            padx=10,
            pady=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("LOCAL", "SKU", "Proveedor", "Descripción", "Fecha Creación")
        self.local_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            height=12,
            style='LocalRules.Treeview'
        )
        
        # Configurar columnas
        self.local_tree.heading("LOCAL", text="Código LOCAL")
        self.local_tree.heading("SKU", text="Código SKU")
        self.local_tree.heading("Proveedor", text="Código Proveedor")
        self.local_tree.heading("Descripción", text="Descripción")
        self.local_tree.heading("Fecha Creación", text="Fecha Creación")
        
        self.local_tree.column("LOCAL", width=120, anchor="center")
        self.local_tree.column("SKU", width=120, anchor="center")
        self.local_tree.column("Proveedor", width=140, anchor="center")
        self.local_tree.column("Descripción", width=280, anchor="w")
        self.local_tree.column("Fecha Creación", width=140, anchor="center")
        
        # Configurar tags de filas alternadas
        self.local_tree.tag_configure('oddrow', background='#F5F5F5')
        self.local_tree.tag_configure('evenrow', background='white')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.local_tree.yview)
        self.local_tree.configure(yscrollcommand=scrollbar.set)
        
        self.local_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón eliminar
        tk.Button(
            list_frame,
            text="🗑️ Eliminar Regla Seleccionada",
            font=("Segoe UI", 9, "bold"),
            bg=self.ERROR,
            fg=self.WHITE,
            command=self.remove_local_rule,
            cursor="hand2",
            padx=12,
            pady=6
        ).pack(pady=5)
        
    def add_local_rule(self):
        """Agrega una nueva regla de LOCAL + SKU"""
        local = self.local_entry.get().strip()
        sku = self.local_sku_entry.get().strip().upper()
        proveedor = self.local_prov_entry.get().strip()
        descripcion = self.local_desc_entry.get().strip()
        
        if not local or not sku or not proveedor:
            messagebox.showwarning(
                "⚠️ Campos Incompletos",
                "Por favor ingrese el código LOCAL, SKU y código de Proveedor."
            , parent=self.window)
            return
        
        if self.rules_manager.add_local_rule(local, sku, proveedor, descripcion):
            messagebox.showinfo(
                "✅ Éxito",
                f"Regla agregada:\nLOCAL {local} + SKU {sku} → Proveedor {proveedor}"
            , parent=self.window)
            
            # Limpiar campos
            self.local_entry.delete(0, tk.END)
            self.local_sku_entry.delete(0, tk.END)
            self.local_prov_entry.delete(0, tk.END)
            self.local_desc_entry.delete(0, tk.END)
            
            self.refresh_local_rules()
            self.refresh_stats()
        else:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo agregar la regla.\nPosiblemente ya existe una regla para LOCAL {local} + SKU {sku}."
            , parent=self.window)
    
    def remove_local_rule(self):
        """Elimina la regla de LOCAL + SKU seleccionada"""
        selection = self.local_tree.selection()
        if not selection:
            messagebox.showwarning(
                "⚠️ Sin Selección",
                "Por favor seleccione una regla para eliminar."
            , parent=self.window)
            return
        
        item = self.local_tree.item(selection[0])
        local = item["values"][0]
        sku = item["values"][1]
        
        if messagebox.askyesno(
            "🗑️ Confirmar Eliminación",
            f"¿Está seguro que desea eliminar la regla?\n\nLOCAL {local} + SKU {sku}"
        , parent=self.window):
            if self.rules_manager.remove_local_rule(local, sku):
                messagebox.showinfo("✅ Éxito", f"Regla eliminada: LOCAL {local} + SKU {sku}", parent=self.window)
                self.refresh_local_rules()
                self.refresh_stats()
            else:
                messagebox.showerror("❌ Error", "No se pudo eliminar la regla.", parent=self.window)
    
    def refresh_local_rules(self):
        """Actualiza la lista de reglas de LOCAL"""
        # Limpiar
        for item in self.local_tree.get_children():
            self.local_tree.delete(item)
        
        # Cargar reglas
        rules = self.rules_manager.get_local_rules()
        for rule in rules:
            fecha = rule.get("created", "N/A")
            if "T" in fecha:
                fecha = fecha.split("T")[0]  # Solo fecha, sin hora
            
            # Determinar tag de fila alternada
            num_items = len(self.local_tree.get_children())
            tag_fila = 'evenrow' if num_items % 2 == 0 else 'oddrow'
            
            self.local_tree.insert(
                "", 
                "end", 
                values=(
                    rule["local"],
                    rule.get("sku", "N/A"),  # Agregar SKU
                    rule["proveedor"],
                    rule.get("descripcion", ""),
                    fecha
                ),
                tags=(tag_fila,)
            )
    
    # --- TAB 2: BLOQUEOS DE STOCK ---
    
    def setup_stock_tab(self):
        """Configura el tab de bloqueos de stock"""
        # Panel de entrada con tema oscuro
        input_frame = tk.LabelFrame(
            self.tab_stock, 
            text="➕ Agregar Nuevo Bloqueo por Quiebre de Stock", 
            font=("Segoe UI", 12, "bold"),  # Fuente moderna
            bg=self.BG_CARD,                # Fondo oscuro
            fg=self.WHITE,                  # Texto blanco
            padx=15,
            pady=15
        )
        input_frame.pack(fill="x", padx=10, pady=10)
        
        # Explicación
        tk.Label(
            input_frame,
            text="⚠️ Un SKU bloqueado con un proveedor específico:\n"
                 "• Si solo tiene 1 proveedor → NO genera orden de compra\n"
                 "• Si tiene múltiples proveedores → Ignora el bloqueado y usa los demás",
            font=("Segoe UI", 10),          # Fuente moderna
            bg=self.BG_CARD,                # Fondo oscuro
            fg=self.WARNING,                # Texto amarillo para advertencia
            justify="left"
        ).pack(anchor="w", pady=5)
        
        # Campos
        row1 = tk.Frame(input_frame, bg=self.BG_CARD)
        row1.pack(fill="x", pady=5)
        
        tk.Label(
            row1, 
            text="Código SKU:", 
            font=("Segoe UI", 11),          # Fuente moderna
            bg=self.BG_CARD,                # Fondo oscuro
            fg=self.WHITE,                  # Texto blanco
            width=20,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.stock_sku_entry = tk.Entry(row1, font=("Segoe UI", 10), width=15, relief='solid', bd=1, 
                                         bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.stock_sku_entry.pack(side="left", padx=5)
        
        tk.Label(
            row1, 
            text="🚫", 
            font=("Segoe UI", 14, "bold"), 
            bg=self.BG_CARD,
            fg=self.ERROR
        ).pack(side="left", padx=10)
        
        tk.Label(
            row1, 
            text="Código Proveedor:", 
            font=("Segoe UI", 11), 
            bg=self.BG_CARD,
            fg=self.WHITE,
            width=20,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.stock_prov_entry = tk.Entry(row1, font=("Segoe UI", 10), width=15, relief='solid', bd=1, 
                                         bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.stock_prov_entry.pack(side="left", padx=5)
        
        # Motivo
        row2 = tk.Frame(input_frame, bg=self.BG_CARD)
        row2.pack(fill="x", pady=5)
        
        tk.Label(
            row2, 
            text="Motivo del bloqueo:", 
            font=("Segoe UI", 11), 
            bg=self.BG_CARD,
            fg=self.WHITE,
            width=20,
            anchor="w"
        ).pack(side="left", padx=5)
        
        self.stock_motivo_entry = tk.Entry(row2, font=("Segoe UI", 10), width=50, relief='solid', bd=1, 
                                           bg=self.BG_DARK, fg=self.WHITE, insertbackground=self.WHITE)
        self.stock_motivo_entry.insert(0, "Quiebre de stock")
        self.stock_motivo_entry.pack(side="left", padx=5, fill="x", expand=True)
        
        # Botón agregar
        tk.Button(
            input_frame,
            text="🚫 Bloquear Combinación",
            font=("Segoe UI", 9, "bold"),
            bg=self.ERROR,
            fg=self.WHITE,
            command=self.add_stock_block,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            activebackground=self.WARNING
        ).pack(pady=10)
        
        # Lista de bloqueos existentes
        list_frame = tk.LabelFrame(
            self.tab_stock, 
            text="📋 Bloqueos Activos", 
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_CARD,
            fg=self.WHITE,
            padx=10,
            pady=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview
        columns = ("SKU", "Proveedor", "Motivo", "Fecha Creación")
        self.stock_tree = ttk.Treeview(
            list_frame, 
            columns=columns, 
            show="headings",
            height=12,
            style='StockBlocks.Treeview'
        )
        
        # Configurar columnas
        self.stock_tree.heading("SKU", text="Código SKU")
        self.stock_tree.heading("Proveedor", text="Código Proveedor Bloqueado")
        self.stock_tree.heading("Motivo", text="Motivo del Bloqueo")
        self.stock_tree.heading("Fecha Creación", text="Fecha Creación")
        
        self.stock_tree.column("SKU", width=140, anchor="center")
        self.stock_tree.column("Proveedor", width=180, anchor="center")
        self.stock_tree.column("Motivo", width=280, anchor="w")
        self.stock_tree.column("Fecha Creación", width=150, anchor="center")
        
        # Configurar tags de filas alternadas
        self.stock_tree.tag_configure('oddrow', background='#F5F5F5')
        self.stock_tree.tag_configure('evenrow', background='white')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stock_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón eliminar
        tk.Button(
            list_frame,
            text="✅ Desbloquear Seleccionado",
            font=("Segoe UI", 9, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.remove_stock_block,
            cursor="hand2",
            padx=12,
            pady=6
        ).pack(pady=5)
    
    def add_stock_block(self):
        """Agrega un nuevo bloqueo de stock"""
        sku = self.stock_sku_entry.get().strip().upper()
        proveedor = self.stock_prov_entry.get().strip()
        motivo = self.stock_motivo_entry.get().strip()
        
        if not sku or not proveedor:
            messagebox.showwarning(
                "⚠️ Campos Incompletos",
                "Por favor ingrese el código SKU y el código de Proveedor."
            , parent=self.window)
            return
        
        if self.rules_manager.add_stock_block(sku, proveedor, motivo):
            messagebox.showinfo(
                "✅ Éxito",
                f"Bloqueo agregado:\nSKU {sku} + Proveedor {proveedor}\n\n"
                f"Este proveedor no generará órdenes para este SKU."
            , parent=self.window)
            
            # Limpiar campos
            self.stock_sku_entry.delete(0, tk.END)
            self.stock_prov_entry.delete(0, tk.END)
            self.stock_motivo_entry.delete(0, tk.END)
            self.stock_motivo_entry.insert(0, "Quiebre de stock")
            
            self.refresh_stock_blocks()
            self.refresh_stats()
        else:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo agregar el bloqueo.\n"
                f"Posiblemente ya existe un bloqueo para SKU {sku} + Proveedor {proveedor}."
            , parent=self.window)
    
    def remove_stock_block(self):
        """Elimina el bloqueo de stock seleccionado"""
        selection = self.stock_tree.selection()
        if not selection:
            messagebox.showwarning(
                "⚠️ Sin Selección",
                "Por favor seleccione un bloqueo para eliminar."
            , parent=self.window)
            return
        
        item = self.stock_tree.item(selection[0])
        sku = item["values"][0]
        proveedor = item["values"][1]
        
        if messagebox.askyesno(
            "✅ Confirmar Desbloqueo",
            f"¿Está seguro que desea desbloquear?\n\nSKU: {sku}\nProveedor: {proveedor}"
        , parent=self.window):
            if self.rules_manager.remove_stock_block(sku, proveedor):
                messagebox.showinfo(
                    "✅ Éxito", 
                    f"Bloqueo eliminado:\nSKU {sku} + Proveedor {proveedor}"
                , parent=self.window)
                self.refresh_stock_blocks()
                self.refresh_stats()
            else:
                messagebox.showerror("❌ Error", "No se pudo eliminar el bloqueo.", parent=self.window)
    
    def refresh_stock_blocks(self):
        """Actualiza la lista de bloqueos de stock"""
        # Limpiar
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # Cargar bloqueos
        blocks = self.rules_manager.get_stock_blocks()
        for block in blocks:
            fecha = block.get("created", "N/A")
            if "T" in fecha:
                fecha = fecha.split("T")[0]  # Solo fecha, sin hora
            
            # Determinar tag de fila alternada
            num_items = len(self.stock_tree.get_children())
            tag_fila = 'evenrow' if num_items % 2 == 0 else 'oddrow'
            
            self.stock_tree.insert(
                "", 
                "end", 
                values=(
                    block["sku"],
                    block["proveedor"],
                    block.get("motivo", ""),
                    fecha
                ),
                tags=(tag_fila,)
            )
    
    # --- TAB 3: ESTADÍSTICAS ---
    
    def setup_stats_tab(self):
        """Configura el tab de estadísticas"""
        # Frame principal
        main_frame = tk.Frame(self.tab_stats, bg=self.BG_CARD)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        tk.Label(
            main_frame,
            text="📊 Estadísticas del Sistema de Reglas",
            font=("Segoe UI", 14, "bold"),
            bg=self.BG_CARD,
            fg=self.PRIMARY
        ).pack(pady=10)
        
        # Stats display
        self.stats_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            font=("Consolas", 10),
            bg=self.BG_DARK,
            fg=self.WHITE,
            insertbackground=self.WHITE,
            relief="solid",
            bd=1
        )
        self.stats_text.pack(fill="both", expand=True, pady=10)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.BG_CARD)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="📊 Exportar a Excel",
            font=("Segoe UI", 9, "bold"),
            bg=self.SUCCESS,
            fg=self.WHITE,
            command=self.export_to_excel,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            activebackground=self.PRIMARY
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📄 Importar Template",
            font=("Segoe UI", 9, "bold"),
            bg=self.WARNING,
            fg=self.WHITE,
            command=self.import_from_excel,
            cursor="hand2",
            padx=12,
            pady=6,
            relief="flat",
            activebackground=self.PRIMARY
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="📄 Descargar Template",
            font=("Segoe UI", 9, "bold"),
            bg="#ef6c00",
            fg=self.WHITE,
            command=self.descargar_template,
            cursor="hand2",
            padx=12,
            pady=6
        ).pack(side="left", padx=5)
        
        # Separador visual
        tk.Frame(btn_frame, width=20, bg=self.WHITE).pack(side="left")
        
        tk.Button(
            btn_frame,
            text="🗑️ Limpiar Todas las Reglas",
            font=("Segoe UI", 9, "bold"),
            bg=self.ERROR,
            fg=self.WHITE,
            command=self.clear_all_rules,
            cursor="hand2",
            padx=12,
            pady=6
        ).pack(side="left", padx=5)
    
    def refresh_stats(self):
        """Actualiza las estadísticas"""
        stats = self.rules_manager.get_stats()
        local_rules = self.rules_manager.get_local_rules()
        stock_blocks = self.rules_manager.get_stock_blocks()
        
        self.stats_text.config(state="normal")
        self.stats_text.delete(1.0, tk.END)
        
        output = "=" * 60 + "\n"
        output += "📊 ESTADÍSTICAS DEL SISTEMA DE REGLAS ESPECIALES\n"
        output += "=" * 60 + "\n\n"
        
        output += "📍 REGLAS DE LOCAL → PROVEEDOR:\n"
        output += f"   • Total de reglas: {stats['total_local_rules']}\n"
        output += f"   • Reglas activas: {stats['active_local_rules']}\n\n"
        
        if local_rules:
            output += "   Detalle de reglas:\n"
            for rule in local_rules:
                sku = rule.get('sku', 'N/A')
                output += f"   • LOCAL {rule['local']} + SKU {sku} → Proveedor {rule['proveedor']}\n"
                if rule.get('descripcion'):
                    output += f"     Descripción: {rule['descripcion']}\n"
        
        output += "\n" + "-" * 60 + "\n\n"
        
        output += "🚫 BLOQUEOS POR QUIEBRE DE STOCK:\n"
        output += f"   • Total de bloqueos: {stats['total_stock_blocks']}\n"
        output += f"   • Bloqueos activos: {stats['active_stock_blocks']}\n\n"
        
        if stock_blocks:
            output += "   Detalle de bloqueos:\n"
            for block in stock_blocks:
                output += f"   • SKU {block['sku']} + Proveedor {block['proveedor']}\n"
                if block.get('motivo'):
                    output += f"     Motivo: {block['motivo']}\n"
        
        output += "\n" + "=" * 60 + "\n"
        
        self.stats_text.insert(1.0, output)
        self.stats_text.config(state="disabled")
    
    def export_rules(self):
        """Exporta las reglas a un archivo"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="Exportar Reglas",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.rules_manager.export_rules(filename):
                messagebox.showinfo(
                    "✅ Éxito",
                    f"Reglas exportadas exitosamente a:\n{filename}"
                , parent=self.window)
            else:
                messagebox.showerror(
                    "❌ Error",
                    "No se pudieron exportar las reglas."
                , parent=self.window)
    
    def export_to_excel(self):
        """Exporta las reglas a Excel para edición masiva"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="Exportar Reglas a Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="reglas_especiales.xlsx"
        )
        
        if filename:
            if self.rules_manager.export_to_excel(filename):
                messagebox.showinfo(
                    "✅ Éxito",
                    f"Reglas exportadas a Excel exitosamente:\n{filename}\n\n"
                    f"El archivo contiene:\n"
                    f"• Hoja 'LOCAL_SKU_Rules': Reglas de LOCAL + SKU\n"
                    f"• Hoja 'Stock_Blocks': Bloqueos de stock\n"
                    f"• Hoja 'INSTRUCCIONES': Guía de edición\n\n"
                    f"Después de editar, use 'Importar Template' para cargar los cambios."
                , parent=self.window)
            else:
                messagebox.showerror(
                    "❌ Error",
                    "No se pudieron exportar las reglas a Excel.\n\n"
                    "Asegúrese de que pandas y openpyxl están instalados."
                , parent=self.window)
    
    def import_from_excel(self):
        """Importa reglas desde un archivo Excel"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Importar Reglas desde Excel",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if filename:
            # Preguntar si quiere fusionar o reemplazar
            merge = messagebox.askyesno(
                "📥 Modo de Importación",
                "¿Desea FUSIONAR las reglas del Excel con las existentes?\n\n"
                "• SÍ: Agregar nuevas reglas sin eliminar las actuales\n"
                "• NO: REEMPLAZAR todas las reglas (se perderán las actuales, parent=self.window)\n\n"
                "¿Fusionar reglas?"
            )
            
            # Confirmación adicional si va a reemplazar
            if not merge:
                if not messagebox.askyesno(
                    "⚠️ Confirmar Reemplazo",
                    "ATENCIÓN: Se eliminarán TODAS las reglas actuales.\n\n"
                    "¿Está completamente seguro?"
                , parent=self.window):
                    return
            
            stats = self.rules_manager.import_from_excel(filename, merge=merge)
            
            if "error" in stats:
                messagebox.showerror(
                    "❌ Error",
                    f"No se pudieron importar las reglas:\n\n{stats['error']}\n\n"
                    "Asegúrese de que pandas y openpyxl están instalados."
                , parent=self.window)
            else:
                # Mostrar resumen
                msg = "✅ Importación completada:\n\n"
                msg += f"📍 Reglas LOCAL + SKU:\n"
                msg += f"   • Agregadas: {stats['local_rules_added']}\n"
                msg += f"   • Omitidas (duplicadas): {stats['local_rules_skipped']}\n\n"
                msg += f"🚫 Bloqueos de Stock:\n"
                msg += f"   • Agregados: {stats['stock_blocks_added']}\n"
                msg += f"   • Omitidos (duplicados): {stats['stock_blocks_skipped']}\n"
                
                if stats['errors']:
                    msg += f"\n⚠️ Errores encontrados: {len(stats['errors'])}\n"
                    msg += "Revise la consola para más detalles."
                
                messagebox.showinfo("✅ Importación Completada", msg, parent=self.window)
                
                # Actualizar todas las vistas
                self.refresh_all()
    
    def descargar_template(self):
        """Descarga un template de Excel con la estructura esperada para las reglas"""
        from tkinter import filedialog
        import pandas as pd
        
        # Pedir ubicación de guardado
        filename = filedialog.asksaveasfilename(
            title="Guardar Template",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="Reglas_Template.xlsx"
        )
        
        if not filename:
            return
        
        try:
            # Crear datos de ejemplo para LOCAL_SKU_Rules
            local_rules_ejemplo = pd.DataFrame({
                'local': ['12345', '67890', '11111'],
                'sku': ['A12345', 'B67890', 'C11111'],
                'proveedor': ['77300', '77301', '77302'],
                'descripcion': ['Regla ejemplo 1', 'Regla ejemplo 2', 'Regla ejemplo 3'],
                'active': [True, True, True]
            })
            
            # Crear datos de ejemplo para Stock_Blocks
            stock_blocks_ejemplo = pd.DataFrame({
                'sku': ['A12345', 'B67890', 'C11111'],
                'proveedor': ['77300', '77301', '77302'],
                'motivo': ['Quiebre de stock temporal', 'Calidad deficiente', 'Descontinuado por proveedor'],
                'active': [True, True, True]
            })
            
            # Crear hoja de instrucciones
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
                    '1. Después de llenar, usar "Importar Template"',
                    '2. Las reglas duplicadas serán ignoradas',
                    '3. Eliminar las filas de ejemplo antes de importar'
                ]
            })
            
            # Guardar en Excel con tres hojas
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                local_rules_ejemplo.to_excel(writer, sheet_name='LOCAL_SKU_Rules', index=False)
                stock_blocks_ejemplo.to_excel(writer, sheet_name='Stock_Blocks', index=False)
                instrucciones.to_excel(writer, sheet_name='INSTRUCCIONES', index=False)
            
            messagebox.showinfo(
                "✅ Template Descargado",
                f"Template guardado en:\n{filename}\n\n"
                "El template contiene:\n"
                "• Hoja 'LOCAL_SKU_Rules': Para reglas LOCAL + SKU\n"
                "• Hoja 'Stock_Blocks': Para bloqueos por quiebre\n"
                "• Hoja 'INSTRUCCIONES': Guía de uso\n\n"
                "Edite las hojas y luego use 'Importar desde Excel'",
                parent=self.window
            )
        except Exception as e:
            messagebox.showerror(
                "❌ Error",
                f"No se pudo crear el template:\n{str(e)}",
                parent=self.window
            )
    
    def clear_all_rules(self):
        """Limpia todas las reglas del sistema con doble confirmación"""
        # Primera confirmación
        if not messagebox.askyesno(
            "⚠️ Limpiar Todas las Reglas",
            "¿Está seguro que desea eliminar TODAS las reglas?\n\n"
            "Esto incluye:\n"
            "• Todas las reglas de LOCAL + SKU → Proveedor\n"
            "• Todos los bloqueos por quiebre de stock\n\n"
            "Esta acción NO se puede deshacer."
        , parent=self.window):
            return
        
        # Segunda confirmación más fuerte
        if not messagebox.askyesno(
            "🚨 CONFIRMACIÓN FINAL",
            "ÚLTIMA ADVERTENCIA:\n\n"
            "Se eliminarán TODAS las reglas del sistema.\n"
            "Se perderán TODOS los datos de reglas.\n\n"
            "¿Está COMPLETAMENTE seguro?\n\n"
            "TIP: Use 'Exportar a Excel' o 'Exportar JSON'\n"
            "antes de limpiar para tener un respaldo."
        , parent=self.window):
            return
        
        # Obtener estadísticas antes de limpiar
        stats = self.rules_manager.get_stats()
        total_rules = stats['total_local_rules'] + stats['total_stock_blocks']
        
        # Limpiar todas las reglas
        self.rules_manager.clear_all_rules()
        
        # Actualizar todas las vistas
        self.refresh_all()
        
        messagebox.showinfo(
            "✅ Reglas Eliminadas",
            f"Se eliminaron exitosamente todas las reglas:\n\n"
            f"• {stats['total_local_rules']} reglas de LOCAL + SKU\n"
            f"• {stats['total_stock_blocks']} bloqueos de stock\n"
            f"• Total: {total_rules} reglas eliminadas\n\n"
            f"El sistema está ahora limpio."
        , parent=self.window)
    
    def refresh_all(self):
        """Actualiza todas las vistas"""
        self.refresh_local_rules()
        self.refresh_stock_blocks()
        self.refresh_stats()


# Función de prueba
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    dialog = RulesDialog(root)
    root.mainloop()

