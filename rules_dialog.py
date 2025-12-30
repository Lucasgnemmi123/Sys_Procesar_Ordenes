"""
Interfaz Simple para Gestión de Reglas Especiales
Version simplificada con diseño moderno que garantiza el refresh correcto
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from rules_manager import RulesManager
import pandas as pd

class RulesDialog:
    """Ventana simple para gestionar reglas especiales"""
    
    def __init__(self, parent=None):
        """Inicializa la ventana de reglas"""
        self.parent = parent
        self.rules_manager = RulesManager()
        
        # Crear root oculto si no existe (igual que AgendaDialog)
        try:
            root = tk._default_root
            if root is None:
                root = tk.Tk()
                root.withdraw()
        except:
            root = tk.Tk()
            root.withdraw()
        
        # Crear Toplevel independiente (compatible con customtkinter parent)
        self.window = tk.Toplevel()
        self.window.title("Gestión de Reglas Especiales - Sistema DHL")
        
        # IMPORTANTE: Forzar theme 'default' para SOBREESCRIBIR el 'clam' de gui_moderna_v2
        # Esto debe hacerse INMEDIATAMENTE después de crear la ventana
        self.style = ttk.Style(self.window)
        self.style.theme_use('default')
        
        # Obtener dimensiones de pantalla
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Ventana optimizada - MENOS ANCHA
        window_width = min(1200, screen_width - 100)
        window_height = min(950, screen_height - 100)  # Altura fija optimizada
        
        # Centrar
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Colores del tema moderno (consistente con gui_moderna_v2.py)
        self.BG_DARK = "#1a1d29"
        self.BG_SURFACE = "#242837"
        self.BG_CARD = "#2d3142"
        self.PRIMARY = "#00d4ff"
        self.PRIMARY_DARK = "#00b8d9"
        self.SUCCESS = "#34d399"
        self.WARNING = "#fbbf24"
        self.ERROR = "#f87171"
        self.TEXT_PRIMARY = "#ffffff"
        self.TEXT_SECONDARY = "#e5e7eb"
        self.TEXT_MUTED = "#9ca3af"
        self.BORDER = "#3f4555"
        
        # Configurar ventana
        self.window.configure(bg=self.BG_DARK)
        
        # Configurar estilos de tabla
        self.configure_table_style()
        
        self.setup_ui()
        
        # CRÍTICO: Esperar a que la ventana esté completamente renderizada
        # antes de hacer el primer refresh
        self.window.update()
        self.window.after(200, self.refresh_all)
    
    def _show_message(self, msg_type, title, message):
        """Helper para mostrar messageboxes que SIEMPRE aparezcan al frente"""
        self.window.lift()
        self.window.attributes('-topmost', True)
        self.window.update()
        
        if msg_type == "info":
            result = messagebox.showinfo(title, message, parent=self.window)
        elif msg_type == "error":
            result = messagebox.showerror(title, message, parent=self.window)
        elif msg_type == "warning":
            result = messagebox.showwarning(title, message, parent=self.window)
        elif msg_type == "yesno":
            result = messagebox.askyesno(title, message, parent=self.window)
        
        self.window.attributes('-topmost', False)
        return result
    
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
        
        # Estilo moderno para el Notebook
        self.style.configure('Modern.TNotebook',
            background=self.BG_DARK,
            borderwidth=0,
            tabmargins=[2, 5, 2, 0]
        )
        
        self.style.configure('Modern.TNotebook.Tab',
            background=self.BG_SURFACE,
            foreground=self.TEXT_MUTED,
            padding=[25, 12],
            font=('Segoe UI', 11, 'bold'),
            borderwidth=0,
            focuscolor='none'
        )
        
        self.style.map('Modern.TNotebook.Tab',
            background=[
                ('selected', self.BG_CARD),
                ('active', self.BG_SURFACE)  # hover
            ],
            foreground=[
                ('selected', self.PRIMARY),
                ('active', self.TEXT_SECONDARY)
            ],
            expand=[('selected', [1, 1, 1, 0])]
        )
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Header oscuro moderno
        header = tk.Frame(self.window, bg=self.BG_SURFACE, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Título con icono
        title_frame = tk.Frame(header, bg=self.BG_SURFACE)
        title_frame.pack(side="left", padx=25, pady=15)
        
        tk.Label(
            title_frame, 
            text="⚙", 
            font=("Segoe UI Emoji", 24),
            bg=self.BG_SURFACE,
            fg=self.PRIMARY
        ).pack(side="left", padx=(0, 10))
        
        tk.Label(
            title_frame, 
            text="REGLAS ESPECIALES", 
            font=("Segoe UI", 18, "bold"),
            bg=self.BG_SURFACE,
            fg=self.PRIMARY
        ).pack(side="left")
        
        # Botón cerrar con texto
        close_btn = tk.Button(
            header,
            text="✕ Cerrar",
            command=self.window.destroy,
            bg=self.ERROR,
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#dc2626",
            activeforeground=self.TEXT_PRIMARY
        )
        close_btn.pack(side="right", padx=15, pady=15)
        
        # Barra de herramientas con botones de gestión
        self.setup_management_buttons(self.window)
        
        # ESTRUCTURA CON NOTEBOOK - 2 PESTAÑAS SEPARADAS
        # Contenedor principal
        main_container = tk.Frame(self.window, bg=self.BG_DARK)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Crear Notebook para pestañas con estilo moderno
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.pack(fill="both", expand=True)
        
        # Pestaña 1: Reglas LOCAL + SKU
        tab_local = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(tab_local, text="  📍 Reglas LOCAL + SKU  ")
        self.setup_local_section(tab_local)
        
        # Pestaña 2: Bloqueos de Stock
        tab_stock = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(tab_stock, text="  📦 Bloqueos de Stock  ")
        self.setup_stock_section(tab_stock)
    
    def setup_local_section(self, parent):
        """Configura la sección de reglas LOCAL"""
        # Card con fondo elevado que ocupa todo el espacio
        section = tk.Frame(parent, bg=self.BG_CARD, relief="flat", bd=0)
        section.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Formulario de entrada con estilo moderno
        form = tk.Frame(section, bg=self.BG_CARD)
        form.pack(fill="x", padx=20, pady=15)
        
        # Fila 1
        row1 = tk.Frame(form, bg=self.BG_CARD)
        row1.pack(fill="x", pady=5)
        
        self._create_input_group(row1, "LOCAL:", "local_entry", 15)
        self._create_input_group(row1, "SKU:", "local_sku_entry", 15)
        self._create_input_group(row1, "Proveedor:", "local_prov_entry", 15)
        
        # Fila 2
        row2 = tk.Frame(form, bg=self.BG_CARD)
        row2.pack(fill="x", pady=5)
        
        tk.Label(
            row2, 
            text="Descripción:", 
            bg=self.BG_CARD, 
            fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=5)
        
        self.local_desc_entry = tk.Entry(
            row2, 
            width=70,
            bg=self.BG_SURFACE,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.PRIMARY,
            relief="flat",
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=2,
            highlightbackground=self.BORDER,
            highlightcolor=self.PRIMARY
        )
        self.local_desc_entry.pack(side="left", padx=5, ipady=6)
        
        # Botones con estilo moderno
        btn_frame = tk.Frame(form, bg=self.BG_CARD)
        btn_frame.pack(fill="x", pady=10)
        
        self._create_action_button(
            btn_frame, 
            "✚ Agregar Regla", 
            self.add_local_rule, 
            self.SUCCESS
        ).pack(side="left", padx=5)
        
        self._create_action_button(
            btn_frame, 
            "✖ Eliminar Seleccionada", 
            self.remove_local_rule, 
            self.ERROR
        ).pack(side="left", padx=5)
        
        # Buscador
        search_frame = tk.Frame(section, bg=self.BG_CARD)
        search_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            bg=self.BG_CARD,
            fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=5)
        
        self.local_search_entry = tk.Entry(
            search_frame,
            width=40,
            bg=self.BG_SURFACE,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.PRIMARY,
            relief="flat",
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=2,
            highlightbackground=self.BORDER,
            highlightcolor=self.PRIMARY
        )
        self.local_search_entry.pack(side="left", padx=5, ipady=6)
        self.local_search_entry.insert(0, "Buscar por LOCAL, SKU o Proveedor...")
        self.local_search_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.local_search_entry, "Buscar por LOCAL, SKU o Proveedor..."))
        self.local_search_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(self.local_search_entry, "Buscar por LOCAL, SKU o Proveedor..."))
        self.local_search_entry.bind("<KeyRelease>", lambda e: self.filter_local_rules())
        
        tk.Button(
            search_frame,
            text="✖ Limpiar",
            command=lambda: self._clear_search(self.local_search_entry, "Buscar por LOCAL, SKU o Proveedor...", self.refresh_local_rules),
            bg=self.BG_SURFACE,
            fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 9),
            relief="flat",
            padx=10,
            pady=2,
            cursor="hand2",
            bd=0
        ).pack(side="left", padx=5)
        
        # Tabla con estilo moderno
        table_frame = tk.Frame(section, bg=self.BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        columns = ("LOCAL", "SKU", "Proveedor", "Descripcion", "Fecha")
        self.local_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            style="Bordered.Treeview"
        )
        
        self.local_tree.heading("LOCAL", text="LOCAL")
        self.local_tree.heading("SKU", text="SKU")
        self.local_tree.heading("Proveedor", text="Proveedor")
        self.local_tree.heading("Descripcion", text="Descripción")
        self.local_tree.heading("Fecha", text="Fecha Creación")
        
        self.local_tree.column("LOCAL", width=100, anchor="center")
        self.local_tree.column("SKU", width=120, anchor="center")
        self.local_tree.column("Proveedor", width=100, anchor="center")
        self.local_tree.column("Descripcion", width=400)
        self.local_tree.column("Fecha", width=120, anchor="center")
        
        # Configurar tags de filas alternadas (COPIADO DE products_dialog.py)
        self.local_tree.tag_configure('oddrow', background='#F5F5F5')
        self.local_tree.tag_configure('evenrow', background='white')
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.local_tree.yview)
        self.local_tree.configure(yscrollcommand=scrollbar.set)
        
        self.local_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_input_group(self, parent, label_text, entry_var_name, width):
        """Helper para crear un grupo de label + entry"""
        tk.Label(
            parent, 
            text=label_text, 
            bg=self.BG_CARD, 
            fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=5)
        
        entry = tk.Entry(
            parent, 
            width=width,
            bg=self.BG_SURFACE,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.PRIMARY,
            relief="flat",
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=2,
            highlightbackground=self.BORDER,
            highlightcolor=self.PRIMARY
        )
        entry.pack(side="left", padx=5, ipady=6)
        setattr(self, entry_var_name, entry)
    
    def _create_action_button(self, parent, text, command, bg_color):
        """Helper para crear botones de acción con estilo"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            activebackground=bg_color,
            activeforeground=self.TEXT_PRIMARY,
            bd=0,
            highlightthickness=0
        )
        # Aplicar esquinas redondeadas mediante estilo
        btn.configure(borderwidth=0)
        return btn
    
    def setup_stock_section(self, parent):
        """Configura la sección de bloqueos de stock"""
        # Card con fondo elevado que ocupa todo el espacio
        section = tk.Frame(parent, bg=self.BG_CARD, relief="flat", bd=0)
        section.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Formulario
        form = tk.Frame(section, bg=self.BG_CARD)
        form.pack(fill="x", padx=20, pady=15)
        
        row1 = tk.Frame(form, bg=self.BG_CARD)
        row1.pack(fill="x", pady=5)
        
        self._create_input_group(row1, "SKU:", "stock_sku_entry", 15)
        self._create_input_group(row1, "Proveedor:", "stock_prov_entry", 15)
        self._create_input_group(row1, "Motivo:", "stock_motivo_entry", 45)
        self.stock_motivo_entry.insert(0, "Quiebre de stock")
        
        btn_frame = tk.Frame(form, bg=self.BG_CARD)
        btn_frame.pack(fill="x", pady=10)
        
        self._create_action_button(
            btn_frame, 
            "✚ Agregar Bloqueo", 
            self.add_stock_block, 
            self.SUCCESS
        ).pack(side="left", padx=5)
        
        self._create_action_button(
            btn_frame, 
            "✖ Eliminar Seleccionado", 
            self.remove_stock_block, 
            self.ERROR
        ).pack(side="left", padx=5)
        
        # Buscador
        search_frame = tk.Frame(section, bg=self.BG_CARD)
        search_frame.pack(fill="x", padx=20, pady=(10, 5))
        
        tk.Label(
            search_frame,
            text="🔍 Buscar:",
            bg=self.BG_CARD,
            fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=5)
        
        self.stock_search_entry = tk.Entry(
            search_frame,
            width=40,
            bg=self.BG_SURFACE,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.PRIMARY,
            relief="flat",
            font=("Segoe UI", 10),
            bd=0,
            highlightthickness=2,
            highlightbackground=self.BORDER,
            highlightcolor=self.PRIMARY
        )
        self.stock_search_entry.pack(side="left", padx=5, ipady=6)
        self.stock_search_entry.insert(0, "Buscar por SKU o Proveedor...")
        self.stock_search_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(self.stock_search_entry, "Buscar por SKU o Proveedor..."))
        self.stock_search_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(self.stock_search_entry, "Buscar por SKU o Proveedor..."))
        self.stock_search_entry.bind("<KeyRelease>", lambda e: self.filter_stock_blocks())
        
        tk.Button(
            search_frame,
            text="✖ Limpiar",
            command=lambda: self._clear_search(self.stock_search_entry, "Buscar por SKU o Proveedor...", self.refresh_stock_blocks),
            bg=self.BG_SURFACE,
            fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 9),
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        # Tabla
        table_frame = tk.Frame(section, bg=self.BG_CARD)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        columns = ("SKU", "Proveedor", "Motivo", "Fecha")
        self.stock_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            style="Bordered.Treeview"
        )
        
        self.stock_tree.heading("SKU", text="SKU")
        self.stock_tree.heading("Proveedor", text="Proveedor")
        self.stock_tree.heading("Motivo", text="Motivo del Bloqueo")
        self.stock_tree.heading("Fecha", text="Fecha Creación")
        
        self.stock_tree.column("SKU", width=120, anchor="center")
        self.stock_tree.column("Proveedor", width=120, anchor="center")
        self.stock_tree.column("Motivo", width=450)
        self.stock_tree.column("Fecha", width=120, anchor="center")
        
        # Configurar tags de filas alternadas (COPIADO DE products_dialog.py)
        self.stock_tree.tag_configure('oddrow', background='#F5F5F5')
        self.stock_tree.tag_configure('evenrow', background='white')
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stock_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_management_buttons(self, parent):
        """Botones de gestión masiva en toolbar"""
        # Toolbar oscuro
        toolbar = tk.Frame(parent, bg=self.BG_SURFACE, height=60)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)
        
        # Frame interno para botones
        btn_frame = tk.Frame(toolbar, bg=self.BG_SURFACE)
        btn_frame.pack(fill="both", padx=15, pady=10)
        
        # Label de acciones
        tk.Label(
            btn_frame,
            text="ACCIONES:",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_SURFACE,
            fg=self.TEXT_MUTED
        ).pack(side="left", padx=(0, 15))
        
        # Botones de gestión
        self._create_toolbar_button(
            btn_frame, 
            "� Descargar Template", 
            self.descargar_template, 
            self.PRIMARY
        ).pack(side="left", padx=3)
        
        self._create_toolbar_button(
            btn_frame, 
            "📥 Importar Template", 
            self.import_from_excel, 
            self.PRIMARY
        ).pack(side="left", padx=3)
        
        self._create_toolbar_button(
            btn_frame, 
            "📤 Exportar a Excel", 
            self.export_to_excel, 
            self.PRIMARY
        ).pack(side="left", padx=3)
        
        # Botón de limpieza a la derecha
        self._create_toolbar_button(
            btn_frame, 
            "🗑 Limpiar Todo", 
            self.clear_all_rules, 
            self.ERROR
        ).pack(side="right", padx=3)
    
    def _create_toolbar_button(self, parent, text, command, bg_color):
        """Helper para crear botones de toolbar más compactos"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            activebackground=bg_color,
            activeforeground=self.TEXT_PRIMARY
        )
        return btn
    
    # Métodos de gestión
    def add_local_rule(self):
        local = self.local_entry.get().strip()
        sku = self.local_sku_entry.get().strip().upper()
        proveedor = self.local_prov_entry.get().strip()
        descripcion = self.local_desc_entry.get().strip()
        
        if not local or not sku or not proveedor:
            self._show_message("warning", "Campos Incompletos", "Complete LOCAL, SKU y Proveedor")
            return
        
        if self.rules_manager.add_local_rule(local, sku, proveedor, descripcion):
            self._show_message("info", "Exito", f"Regla agregada: LOCAL {local} + SKU {sku}")
            
            # Limpiar campos DESPUÉS del messagebox
            self.local_entry.delete(0, tk.END)
            self.local_sku_entry.delete(0, tk.END)
            self.local_prov_entry.delete(0, tk.END)
            self.local_desc_entry.delete(0, tk.END)
            
            # Diferir refresh para DESPUÉS del ciclo de eventos
            self.window.after(50, self.refresh_local_rules)
        else:
            self._show_message("error", "Error", "No se pudo agregar la regla")
    
    def remove_local_rule(self):
        selection = self.local_tree.selection()
        if not selection:
            self._show_message("warning", "Sin Seleccion", "Seleccione una regla")
            return
        
        item = self.local_tree.item(selection[0])
        local = item["values"][0]
        sku = item["values"][1]
        
        if self._show_message("yesno", "Confirmar", f"Eliminar regla LOCAL {local} + SKU {sku}?"):
            if self.rules_manager.remove_local_rule(local, sku):
                self._show_message("info", "Exito", "Regla eliminada")
                # Diferir refresh para DESPUÉS del ciclo de eventos
                self.window.after(50, self.refresh_local_rules)
    
    def add_stock_block(self):
        sku = self.stock_sku_entry.get().strip().upper()
        proveedor = self.stock_prov_entry.get().strip()
        motivo = self.stock_motivo_entry.get().strip()
        
        if not sku or not proveedor:
            self._show_message("warning", "Campos Incompletos", "Complete SKU y Proveedor")
            return
        
        if self.rules_manager.add_stock_block(sku, proveedor, motivo):
            self._show_message("info", "Exito", f"Bloqueo agregado: SKU {sku}")
            
            # Limpiar campos DESPUÉS del messagebox
            self.stock_sku_entry.delete(0, tk.END)
            self.stock_prov_entry.delete(0, tk.END)
            self.stock_motivo_entry.delete(0, tk.END)
            self.stock_motivo_entry.insert(0, "Quiebre de stock")
            
            # Diferir refresh para DESPUÉS del ciclo de eventos
            self.window.after(50, self.refresh_stock_blocks)
        else:
            self._show_message("error", "Error", "No se pudo agregar el bloqueo")
    
    def remove_stock_block(self):
        selection = self.stock_tree.selection()
        if not selection:
            self._show_message("warning", "Sin Seleccion", "Seleccione un bloqueo")
            return
        
        item = self.stock_tree.item(selection[0])
        sku = item["values"][0]
        proveedor = item["values"][1]
        
        if self._show_message("yesno", "Confirmar", f"Eliminar bloqueo SKU {sku}?"):
            if self.rules_manager.remove_stock_block(sku, proveedor):
                self._show_message("info", "Exito", "Bloqueo eliminado")
                self.refresh_stock_blocks()  # DESPUÉS del messagebox
    
    def _clear_placeholder(self, entry, placeholder):
        """Limpia el placeholder al hacer foco"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.TEXT_PRIMARY)
    
    def _restore_placeholder(self, entry, placeholder):
        """Restaura el placeholder si está vacío"""
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=self.TEXT_MUTED)
    
    def _clear_search(self, entry, placeholder, refresh_func):
        """Limpia el campo de búsqueda y refresca"""
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg=self.TEXT_MUTED)
        refresh_func()
    
    def filter_local_rules(self):
        """Filtra las reglas locales según el texto de búsqueda"""
        search_text = self.local_search_entry.get().lower()
        if search_text == "buscar por local, sku o proveedor...":
            search_text = ""
        
        for item in self.local_tree.get_children():
            self.local_tree.delete(item)
        
        rules = self.rules_manager.get_local_rules()
        for rule in rules:
            local = str(rule.get("local", "")).lower()
            sku = str(rule.get("sku", "N/A")).lower()
            proveedor = str(rule.get("proveedor", "")).lower()
            descripcion = str(rule.get("descripcion", "")).lower()
            
            if (not search_text or 
                search_text in local or 
                search_text in sku or 
                search_text in proveedor or
                search_text in descripcion):
                
                fecha = rule.get("created", "N/A")
                if "T" in fecha:
                    fecha = fecha.split("T")[0]
                
                self.local_tree.insert("", "end", values=(
                    rule["local"],
                    rule.get("sku", "N/A"),
                    rule["proveedor"],
                    rule.get("descripcion", ""),
                    fecha
                ))
    
    def filter_stock_blocks(self):
        """Filtra los bloqueos de stock según el texto de búsqueda"""
        search_text = self.stock_search_entry.get().lower()
        if search_text == "buscar por sku o proveedor...":
            search_text = ""
        
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        blocks = self.rules_manager.get_stock_blocks()
        for block in blocks:
            sku = str(block.get("sku", "")).lower()
            proveedor = str(block.get("proveedor", "")).lower()
            motivo = str(block.get("motivo", "")).lower()
            
            if (not search_text or 
                search_text in sku or 
                search_text in proveedor or
                search_text in motivo):
                
                fecha = block.get("created", "N/A")
                if "T" in fecha:
                    fecha = fecha.split("T")[0]
                
                self.stock_tree.insert("", "end", values=(
                    block["sku"],
                    block["proveedor"],
                    block.get("motivo", ""),
                    fecha
                ))
    
    def refresh_local_rules(self):
        """Refresca la tabla de reglas locales - SIMPLE COMO PRODUCTS_DIALOG"""
        # Limpiar tabla
        for item in self.local_tree.get_children():
            self.local_tree.delete(item)
        
        # Cargar reglas
        rules = self.rules_manager.get_local_rules()
        
        for idx, rule in enumerate(rules):
            fecha = rule.get("created", "N/A")
            if "T" in fecha:
                fecha = fecha.split("T")[0]
            
            tag_fila = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.local_tree.insert("", "end", values=(
                rule["local"],
                rule.get("sku", "N/A"),
                rule["proveedor"],
                rule.get("descripcion", ""),
                fecha
            ), tags=(tag_fila,))
    
    def refresh_stock_blocks(self):
        """Refresca la tabla de bloqueos de stock - SIMPLE COMO PRODUCTS_DIALOG"""
        # Limpiar tabla
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        # Cargar bloques
        blocks = self.rules_manager.get_stock_blocks()
        
        for idx, block in enumerate(blocks):
            fecha = block.get("created", "N/A")
            if "T" in fecha:
                fecha = fecha.split("T")[0]
            
            tag_fila = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.stock_tree.insert("", "end", values=(
                block["sku"],
                block["proveedor"],
                block.get("motivo", ""),
                fecha
            ), tags=(tag_fila,))    
    def refresh_all(self):
        """Refresca todas las vistas"""
        self.refresh_local_rules()
        self.refresh_stock_blocks()
    
    def import_from_excel(self):
        """Importa reglas desde un archivo Excel"""
        filename = filedialog.askopenfilename(
            title="Importar Reglas desde Excel",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            parent=self.window
        )
        
        if not filename:
            return
        
        # Preguntar si quiere fusionar o reemplazar
        merge = messagebox.askyesno(
            "📥 Modo de Importación",
            "¿Desea FUSIONAR las reglas del Excel con las existentes?\n\n"
            "• SÍ: Agregar nuevas reglas sin eliminar las actuales\n"
            "• NO: REEMPLAZAR todas las reglas (se perderán las actuales)\n\n"
            "¿Fusionar reglas?",
            parent=self.window
        )
        
        # Confirmación adicional si va a reemplazar
        if not merge:
            if not messagebox.askyesno(
                "⚠️ Confirmar Reemplazo",
                "ATENCIÓN: Se eliminarán TODAS las reglas actuales.\n\n"
                "¿Está completamente seguro?",
                parent=self.window
            ):
                return
        
        stats = self.rules_manager.import_from_excel(filename, merge=merge)
        
        if "error" in stats:
            messagebox.showerror(
                "❌ Error",
                f"No se pudieron importar las reglas:\n\n{stats['error']}\n\n"
                "Asegúrese de que pandas y openpyxl están instalados.",
                parent=self.window
            )
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
            self.refresh_all()  # DESPUÉS del messagebox
    
    def export_to_excel(self):
        """Exporta las reglas a Excel para edición masiva"""
        filename = filedialog.asksaveasfilename(
            title="Exportar Reglas a Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="reglas_especiales.xlsx",
            parent=self.window
        )
        
        if not filename:
            return
        
        if self.rules_manager.export_to_excel(filename):
            messagebox.showinfo(
                "✅ Éxito",
                f"Reglas exportadas a Excel exitosamente:\n{filename}\n\n"
                f"El archivo contiene:\n"
                f"• Hoja 'LOCAL_SKU_Rules': Reglas de LOCAL + SKU\n"
                f"• Hoja 'Stock_Blocks': Bloqueos de stock\n"
                f"• Hoja 'INSTRUCCIONES': Guía de edición\n\n"
                f"Después de editar, use 'Importar Template' para cargar los cambios.",
                parent=self.window
            )
        else:
            messagebox.showerror(
                "❌ Error",
                "No se pudieron exportar las reglas a Excel.\n\n"
                "Asegúrese de que pandas y openpyxl están instalados.",
                parent=self.window
            )
    
    def descargar_template(self):
        """Descarga un template de Excel con la estructura esperada para las reglas"""
        filename = filedialog.asksaveasfilename(
            title="Guardar Template",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="Reglas_Template.xlsx",
            parent=self.window
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
        if not messagebox.askyesno(
            "⚠️ Confirmar Eliminación", 
            "¿Eliminar TODAS las reglas especiales?\n\n"
            "Esta acción NO se puede deshacer.",
            parent=self.window
        ):
            return
        
        if messagebox.askyesno(
            "🔴 CONFIRMACIÓN FINAL", 
            "¿Está COMPLETAMENTE seguro?\n\n"
            "Se eliminarán:\n"
            "• Todas las reglas LOCAL + SKU\n"
            "• Todos los bloqueos de stock",
            parent=self.window
        ):
            self.rules_manager.clear_all_rules()
            messagebox.showinfo(
                "✅ Completado", 
                "Todas las reglas han sido eliminadas.",
                parent=self.window
            )
            self.refresh_all()  # DESPUÉS del messagebox

# Test
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    dialog = RulesDialog(root)
    root.mainloop()
