"""
Sistema de Procesamiento de Pedidos - Interfaz Moderna
Creado por Lucas Gnemmi
Versión: 2.0

Sistema profesional para el procesamiento de pedidos con interfaz gráfica moderna.
Incluye validación de SKUs, mapeo de proveedores y generación de archivos Excel formateados.
"""

import os
import shutil
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
import pandas as pd
import subprocess
import webbrowser
from datetime import datetime
from procesamiento_v2 import (
    procesar_pdfs,
    validar_skus_items,
    mapear_proveedor_por_sku,
    rellenar_fecha_entrega_y_observacion,
    asignar_id_final,
    formatear_excel_salida,
    obtener_nombre_archivo_salida
)
from agenda_manager import AgendaManager
from rules_dialog import RulesDialog
from agenda_dialog import AgendaDialog

# Configuración de colores del tema elegante
class ModernTheme:
    """Clase para definir el tema visual elegante y profesional"""
    # Colores principales elegantes - Inspirado en tema oscuro/elegante
    PRIMARY = "#1a237e"      # Azul índigo profundo
    SECONDARY = "#3949ab"    # Azul índigo medio
    DARK = "#0d1421"         # Azul muy oscuro
    LIGHT_GRAY = "#f5f7fa"   # Gris muy claro
    MEDIUM_GRAY = "#e8eaf6"  # Gris con tinte azul
    WHITE = "#ffffff"        # Blanco puro
    
    # Colores funcionales
    SUCCESS = "#2e7d32"      # Verde oscuro elegante
    WARNING = "#ef6c00"      # Naranja elegante
    ERROR = "#c62828"        # Rojo elegante
    INFO = "#1976d2"         # Azul información
    
    # Colores de texto
    TEXT_PRIMARY = "#263238"
    TEXT_SECONDARY = "#546e7a"
    TEXT_WHITE = "#ffffff"
    
    # Colores adicionales para progreso
    PROGRESS_BG = "#e8eaf6"
    PROGRESS_FILL = "#3949ab"
    
    # Gradiente para efectos
    GRADIENT_START = "#1a237e"
    GRADIENT_END = "#3949ab"

class ModernGUI:
    """
    Interfaz gráfica moderna para el sistema de procesamiento de órdenes DHL
    Created by Lucas Gnemmi
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.theme = ModernTheme()
        
        # Variables para ventanas únicas
        self.ventana_agenda = None
        self.ventana_reglas = None
        
        # Variables de progreso
        self.progress_steps = [
            "Inicializando sistema...",
            "Leyendo archivos Excel...",
            "Validando SKUs...",
            "Mapeando proveedores...",
            "Procesando fechas...",
            "Asignando IDs finales...",
            "Formateando archivo Excel...",
            "Guardando resultados...",
            "¡Procesamiento completado!"
        ]
        self.current_step = 0
        self.total_steps = len(self.progress_steps)
        
        self.setup_main_window()
        self.setup_paths()
        self.setup_widgets()
        self.refrescar_archivos()
        
    def setup_main_window(self):
        """Configuración de la ventana principal responsiva"""
        self.root.title("🚚 Sistema de Procesamiento de Pedidos")
        self.root.configure(bg=self.theme.LIGHT_GRAY)
        self.root.minsize(1200, 750)
        
        # Maximizar ventana
        self.root.state('zoomed')
        
        # Hacer la ventana responsiva
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Configurar estilo TTK moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados
        self._configure_styles()
        
    def _configure_styles(self):
        """Configurar estilos personalizados para widgets TTK"""
        # Estilo para botones principales
        self.style.configure(
            "Modern.TButton",
            background=self.theme.PRIMARY,
            foreground=self.theme.WHITE,
            font=("Arial", 10, "bold"),
            padding=(10, 5),
            relief="flat"
        )
        
        # Estilo hover para botones
        self.style.map(
            "Modern.TButton",
            background=[('active', self.theme.SECONDARY)],
            relief=[('pressed', 'flat'), ('!pressed', 'flat')]
        )
        
        # Estilo para frames
        self.style.configure(
            "Modern.TLabelFrame",
            background=self.theme.LIGHT_GRAY,
            relief="solid",
            borderwidth=1
        )
        
        # Estilo para labels
        self.style.configure(
            "Modern.TLabel",
            background=self.theme.LIGHT_GRAY,
            foreground=self.theme.TEXT_PRIMARY,
            font=("Arial", 9)
        )
        
        # Estilo para barra de progreso - Color que resalta
        self.style.configure(
            "Modern.Horizontal.TProgressbar",
            background="#FF6B35",  # Naranja vibrante que resalta
            troughcolor=self.theme.MEDIUM_GRAY,
            borderwidth=1,
            lightcolor="#FF6B35",
            darkcolor="#E55A2B",
            relief="flat"
        )
        
    def setup_paths(self):
        """Configuración de rutas del sistema"""
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ORDENES_DIR = os.path.join(self.BASE_DIR, "Ordenes")
        self.AGENDA_XLSM = os.path.join(self.BASE_DIR, "Full-Agenda", "Agenda.xlsm")
        self.FULL_XLSX = os.path.join(self.BASE_DIR, "Full-Agenda", "Full.xlsx")
        self.ITEMS_XLSX = os.path.join(self.BASE_DIR, "Full-Agenda", "Items.xlsx")
        
        # Crear directorios si no existen
        os.makedirs(self.ORDENES_DIR, exist_ok=True)
        os.makedirs(os.path.join(self.BASE_DIR, "Salidas"), exist_ok=True)
        
    def get_nombre_archivo_salida(self):
        """Obtiene el nombre dinámico del archivo de salida basado en la fecha de M1"""
        try:
            return obtener_nombre_archivo_salida(self.AGENDA_XLSM, self.BASE_DIR)
        except Exception as e:
            # Fallback a nombre con timestamp si hay error
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return os.path.join(self.BASE_DIR, "Salidas", f"PEDIDOS_CD_OVIEDO_{timestamp}.xlsx")
        
    def setup_widgets(self):
        """Configuración de todos los widgets de la interfaz"""
        self._create_header()
        self._create_main_layout()
        self._create_footer()
        
    def _create_header(self):
        """Crear encabezado simple y visible"""
        # Header principal
        header_main = tk.Frame(self.root, bg=self.theme.PRIMARY, height=80)
        header_main.pack(fill="x", side="top")
        header_main.pack_propagate(False)
        
        # Título centrado directamente
        title_label = tk.Label(
            header_main, 
            text="🚚  SISTEMA DE PROCESAMIENTO DE PEDIDOS", 
            font=("Segoe UI", 20, "bold"),
            fg=self.theme.WHITE, 
            bg=self.theme.PRIMARY
        )
        title_label.pack(expand=True)
        
        # Línea decorativa inferior
        line_frame = tk.Frame(self.root, bg=self.theme.SECONDARY, height=3)
        line_frame.pack(fill="x")

        
    def _create_main_layout(self):
        """Crear layout principal simple y funcional"""
        # Contenedor principal
        main_container = tk.Frame(self.root, bg=self.theme.WHITE, relief="solid", bd=1)
        main_container.pack(fill="both", expand=True, side="top", padx=10, pady=(5, 10))
        
        # Frame de contenido
        content_frame = tk.Frame(main_container, bg=self.theme.WHITE)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Panel izquierdo - tamaño fijo
        left_frame = tk.Frame(content_frame, bg=self.theme.WHITE)
        left_frame.pack(side="left", fill="y", padx=(0, 15))
        
        # Panel derecho - expansible
        right_frame = tk.Frame(content_frame, bg=self.theme.WHITE)
        right_frame.pack(side="left", fill="both", expand=True)
        
        # Crear paneles
        self._create_left_panel(left_frame)
        self._create_center_panel(right_frame)
        
    def _create_styled_labelframe(self, parent, text, icon="", pack_options=None):
        """Crear LabelFrame con estilo personalizado y efectos visuales"""
        # Frame contenedor con efectos de sombra
        container = tk.Frame(parent, bg=self.theme.LIGHT_GRAY)
        if pack_options:
            container.pack(**pack_options)
        
        # Sombra del frame
        shadow = tk.Frame(container, bg=self.theme.MEDIUM_GRAY, height=2)
        shadow.pack(fill="x", side="bottom")
        
        # Frame principal con gradiente simulado
        main_frame = tk.Frame(container, bg=self.theme.WHITE, relief="flat", bd=0)
        main_frame.pack(fill="both", expand=True)
        
        # Header decorativo del panel
        header_frame = tk.Frame(main_frame, bg=self.theme.PRIMARY, height=35)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Título del panel con icono
        title_label = tk.Label(
            header_frame, 
            text=f"{icon} {text}", 
            font=("Segoe UI", 12, "bold"),
            fg=self.theme.WHITE,
            bg=self.theme.PRIMARY
        )
        title_label.pack(anchor="w", padx=15, pady=8)
        
        # Área de contenido
        content_frame = tk.Frame(main_frame, bg=self.theme.WHITE)
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        return content_frame

    def _create_left_panel(self, parent):
        """Crear panel izquierdo con controles estilizados"""
        left_panel = self._create_styled_labelframe(
            parent, 
            "Panel de Control", 
            "📁",
            {"fill": "both", "expand": True}
        )
        
        # Sección de archivos PDF
        self._create_excel_section_simple(left_panel)
        
        # Sección de pasos de procesamiento
        self._create_processing_section(left_panel)
        
        # Sección de accesos rápidos
        self._create_quick_access_section(left_panel)
        
    def _create_pdf_section(self, parent):
        """Crear sección de gestión de archivos Excel"""
        pdf_section = tk.LabelFrame(
            parent, 
            text="� Gestión de Archivos Excel", 
            font=("Arial", 12, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            relief="groove",
            bd=1
        )
        pdf_section.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Lista de Excel con diseño mejorado
        list_container = tk.Frame(pdf_section, bg=self.theme.WHITE)
        list_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(
            list_container, 
            text="📂 Archivos en carpeta Órdenes:", 
            font=("Arial", 10, "bold"), 
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 5))
        
        # Frame para listbox con scrollbar
        list_frame = tk.Frame(list_container, bg=self.theme.WHITE)
        list_frame.pack(fill="both", expand=True)
        
        self.listbox_archivos = tk.Listbox(
            list_frame, 
            height=8, 
            selectmode=tk.SINGLE, 
            font=("Consolas", 9),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            selectbackground=self.theme.PRIMARY,
            selectforeground=self.theme.WHITE,
            relief="solid",
            bd=1
        )
        self.listbox_archivos.pack(side="left", fill="both", expand=True)
        
        scrollbar_archivos = tk.Scrollbar(
            list_frame, 
            orient="vertical", 
            command=self.listbox_archivos.yview
        )
        scrollbar_archivos.pack(side="right", fill="y")
        self.listbox_archivos.config(yscrollcommand=scrollbar_archivos.set)
        
        # Botones de gestión con diseño mejorado
        btn_container = tk.Frame(pdf_section, bg=self.theme.WHITE)
        btn_container.pack(fill="x", padx=10, pady=(0, 10))
        
        buttons = [
            ("➕ Agregar Excel", self.agregar_archivo, self.theme.SUCCESS),
            ("🗑️ Limpiar Todo", self.eliminar_archivo, self.theme.ERROR),
            ("🔄 Actualizar", self.refrescar_archivos, self.theme.INFO)
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                btn_container, 
                text=text, 
                command=command,
                bg=color, 
                fg=self.theme.WHITE, 
                font=("Arial", 9, "bold"),
                relief="flat",
                padx=12,
                pady=4,
                cursor="hand2"
            )
            btn.pack(side="left", padx=3, pady=2)
            
            # Efectos hover
            self._add_hover_effect(btn, color)
            
    def _create_processing_section(self, parent):
        """Crear sección de pasos de procesamiento"""
        processing_section = tk.LabelFrame(
            parent, 
            text="⚙️ Pasos del Procesamiento", 
            font=("Arial", 12, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            relief="groove",
            bd=1
        )
        processing_section.pack(fill="x", padx=5, pady=5)
        
        steps_container = tk.Frame(processing_section, bg=self.theme.WHITE)
        steps_container.pack(fill="x", padx=10, pady=10)
        
        # Paso 1: Abrir Full
        self._create_step_button(
            steps_container, "1", "📋 Abrir Full.xlsx", 
            self.abrir_full_xlsx, "#9B59B6"
        )
        
        # Paso 2: Gestión de Agenda
        self._create_step_button(
            steps_container, "2", "📅 Gestión de Agenda", 
            self.abrir_gestion_agenda, "#3498DB"
        )
        
        # Paso 3: Configurar región
        region_frame = tk.Frame(steps_container, bg=self.theme.WHITE)
        region_frame.pack(fill="x", pady=2)
        
        tk.Label(
            region_frame, 
            text="3.", 
            font=("Arial", 10, "bold"), 
            bg=self.theme.WHITE, 
            fg=self.theme.ERROR, 
            width=3
        ).pack(side="left")
        
        region_config = tk.Frame(region_frame, bg=self.theme.WHITE)
        region_config.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            region_config, 
            text="Región:", 
            font=("Arial", 9, "bold"), 
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 5))
        
        self.region_var = tk.StringVar(value="119")
        self.region_entry = tk.Entry(
            region_config,
            textvariable=self.region_var,
            font=("Arial", 10),
            width=8,
            justify="center",
            relief="solid",
            bd=1
        )
        self.region_entry.pack(side="left")
        
        tk.Label(
            region_config, 
            text=" (por defecto: 119)", 
            font=("Arial", 8), 
            bg=self.theme.WHITE, 
            fg=self.theme.TEXT_SECONDARY
        ).pack(side="left", padx=5)
        
        # Paso 4: Procesar
        process_frame = tk.Frame(steps_container, bg=self.theme.WHITE)
        process_frame.pack(fill="x", pady=8)
        
        tk.Label(
            process_frame, 
            text="4.", 
            font=("Arial", 10, "bold"), 
            bg=self.theme.WHITE, 
            fg=self.theme.ERROR, 
            width=3
        ).pack(side="left")
        
        self.btn_procesar = tk.Button(
            process_frame, 
            text="🚀 PROCESAR PEDIDOS", 
            command=self.ejecutar_procesamiento_async,
            bg=self.theme.PRIMARY, 
            fg=self.theme.WHITE, 
            font=("Arial", 12, "bold"),
            relief="flat",
            pady=8,
            cursor="hand2"
        )
        self.btn_procesar.pack(side="left", fill="x", expand=True)
        
        # Efecto hover para botón principal
        self._add_hover_effect(self.btn_procesar, self.theme.PRIMARY)
        
    def _create_step_button(self, parent, step_num, text, command, color):
        """Crear un botón de paso numerado"""
        step_frame = tk.Frame(parent, bg=self.theme.WHITE)
        step_frame.pack(fill="x", pady=2)
        
        tk.Label(
            step_frame, 
            text=f"{step_num}.", 
            font=("Arial", 10, "bold"), 
            bg=self.theme.WHITE, 
            fg=self.theme.ERROR, 
            width=3
        ).pack(side="left")
        
        btn = tk.Button(
            step_frame, 
            text=text, 
            command=command,
            bg=color, 
            fg=self.theme.WHITE, 
            font=("Arial", 9, "bold"),
            relief="flat",
            pady=3,
            cursor="hand2"
        )
        btn.pack(side="left", fill="x", expand=True)
        
        # Efecto hover
        self._add_hover_effect(btn, color)
        
    def _create_quick_access_section(self, parent):
        """Crear sección de accesos rápidos"""
        quick_section = tk.LabelFrame(
            parent, 
            text="🔗 Acceso Rápido", 
            font=("Arial", 12, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            relief="groove",
            bd=1
        )
        quick_section.pack(fill="x", padx=5, pady=5)
        
        quick_container = tk.Frame(quick_section, bg=self.theme.WHITE)
        quick_container.pack(fill="x", padx=10, pady=10)
        
        quick_buttons = [
            ("⚙️ Reglas Especiales", self.abrir_reglas_especiales, "#8E44AD"),
            ("�📁 Abrir Carpeta Salidas", self.abrir_carpeta_salidas, "#16A085"),
            ("📊 Abrir Items C.Calzada", self.abrir_items_xlsx, "#F39C12")
        ]
        
        for text, command, color in quick_buttons:
            btn = tk.Button(
                quick_container, 
                text=text, 
                command=command,
                bg=color, 
                fg=self.theme.WHITE, 
                font=("Arial", 9, "bold"),
                relief="flat",
                pady=3,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=2)
            
            # Efecto hover
            self._add_hover_effect(btn, color)
            
    def _create_center_panel(self, parent):
        """Crear panel central con logs y resultados"""
        # Panel de logs
        self._create_log_panel(parent)
        
        # Panel de progreso
        self._create_progress_panel(parent)
        
        # Panel de vista previa
        self._create_preview_panel(parent)
    

        
    def _create_log_panel(self, parent):
        """Crear panel de logs de actividades estilizado"""
        log_frame = self._create_styled_labelframe(
            parent, 
            "Registro de Actividad", 
            "📜",
            {"fill": "both", "expand": True, "pady": (0, 8)}
        )
        
        # Terminal estilizado con efectos
        terminal_container = tk.Frame(log_frame, bg=self.theme.DARK, relief="sunken", bd=2)
        terminal_container.pack(fill="both", expand=True)
        
        # Barra superior del terminal
        terminal_header = tk.Frame(terminal_container, bg="#2d2d2d", height=25)
        terminal_header.pack(fill="x")
        terminal_header.pack_propagate(False)
        
        # Botones decorativos del terminal
        buttons_frame = tk.Frame(terminal_header, bg="#2d2d2d")
        buttons_frame.pack(anchor="w", padx=8, pady=6)
        
        for color in ["#ff5f56", "#ffbd2e", "#27ca3f"]:
            btn = tk.Frame(buttons_frame, bg=color, width=12, height=12)
            btn.pack(side="left", padx=2)
        
        # Área de texto del terminal
        self.txt_log = scrolledtext.ScrolledText(
            terminal_container, 
            height=12, 
            state="disabled", 
            font=("Consolas", 9),
            bg=self.theme.DARK,
            fg="#00FF00",  # Verde terminal
            insertbackground="#00FF00",
            wrap=tk.WORD,
            relief="flat",
            bd=0
        )
        self.txt_log.pack(fill="both", expand=True, padx=5, pady=5)
        
    def _create_progress_panel(self, parent):
        """Crear panel de barra de progreso estilizado"""
        progress_frame = self._create_styled_labelframe(
            parent, 
            "Progreso del Procesamiento", 
            "⚡",
            {"fill": "x", "pady": 8}
        )
        
        # Texto del progreso con estilo mejorado
        self.progress_text = tk.StringVar(value="Listo para procesar...")
        progress_label = tk.Label(
            progress_frame,
            textvariable=self.progress_text,
            font=("Segoe UI", 10, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY
        )
        progress_label.pack(anchor="w", pady=(0, 10))
        
        # Contenedor de la barra con efectos de bisel
        progress_bg = tk.Frame(progress_frame, bg="#e0e0e0", relief="sunken", bd=2)
        progress_bg.pack(fill="x", pady=5)
        
        # Barra de progreso personalizada
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_bg,
            variable=self.progress_var,
            maximum=100,
            style="Modern.Horizontal.TProgressbar",
            length=400
        )
        self.progress_bar.pack(fill="x", padx=3, pady=3)
        
        # Porcentaje con estilo mejorado
        self.progress_percent = tk.StringVar(value="0%")
        percent_label = tk.Label(
            progress_frame,
            textvariable=self.progress_percent,
            font=("Arial", 10, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.SECONDARY
        )
        percent_label.pack(anchor="e", pady=(5, 0))
        
    def _create_preview_panel(self, parent):
        """Crear panel de vista previa de resultados estilizado"""
        preview_frame = self._create_styled_labelframe(
            parent, 
            "Vista Previa de Resultados", 
            "📊",
            {"fill": "both", "expand": True, "pady": (8, 0)}
        )
        
        # Contenedor estilizado para la vista previa
        preview_container = tk.Frame(preview_frame, bg="#f8f9fa", relief="groove", bd=2)
        preview_container.pack(fill="both", expand=True)
        
        # Barra de herramientas de la vista previa
        toolbar = tk.Frame(preview_container, bg="#e9ecef", height=30)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)
        
        # Etiqueta informativa
        info_label = tk.Label(
            toolbar,
            text="📄 Datos procesados",
            font=("Segoe UI", 9, "bold"),
            bg="#e9ecef",
            fg=self.theme.TEXT_PRIMARY
        )
        info_label.pack(anchor="w", padx=10, pady=6)
        
        # Área de texto con estilo de documento
        self.txt_salida = scrolledtext.ScrolledText(
            preview_container, 
            height=12, 
            state="disabled", 
            font=("Consolas", 9),
            bg="#ffffff",
            fg=self.theme.TEXT_PRIMARY,
            wrap=tk.NONE,
            relief="flat",
            bd=0,
            selectbackground=self.theme.SECONDARY,
            selectforeground=self.theme.WHITE
        )
        self.txt_salida.pack(fill="both", expand=True, padx=8, pady=8)
        
    def _create_footer(self):
        """Crear barra de estado estilizada en el pie"""
        # Contenedor del footer con gradiente
        footer_container = tk.Frame(self.root, bg=self.theme.DARK, height=35)
        footer_container.pack(side="bottom", fill="x")
        footer_container.pack_propagate(False)
        
        # Línea decorativa superior
        top_line = tk.Frame(footer_container, bg=self.theme.SECONDARY, height=2)
        top_line.pack(fill="x")
        
        # Barra de estado principal
        status_frame = tk.Frame(footer_container, bg=self.theme.DARK)
        status_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Estado del sistema (izquierda)
        self.status_bar = tk.Label(
            status_frame, 
            text="✅ Sistema listo para procesar", 
            anchor=tk.W,
            bg=self.theme.DARK,
            fg="#00FF00",  # Verde terminal como los logs
            font=("Segoe UI", 9, "bold")
        )
        self.status_bar.pack(side=tk.LEFT)
        
        # Separador
        separator = tk.Label(
            status_frame,
            text="•",
            bg=self.theme.DARK,
            fg="#00FF00",  # Verde terminal
            font=("Arial", 12)
        )
        separator.pack(side=tk.LEFT, padx=10)
        
        # Información del autor (derecha)
        author_label = tk.Label(
            status_frame,
            text="Creado por Lucas Gnemmi",
            anchor=tk.E,
            bg=self.theme.DARK,
            fg="#00FF00",  # Verde terminal como los logs
            font=("Segoe UI", 11, "bold")
        )
        author_label.pack(side=tk.RIGHT)
        
    def _add_hover_effect(self, button, original_color):
        """Agregar efecto hover a los botones"""
        def on_enter(e):
            # Crear un color más claro para el hover
            button.configure(bg=self._lighten_color(original_color))
            
        def on_leave(e):
            button.configure(bg=original_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def _add_enhanced_hover_effect(self, button, original_color):
        """Agregar efecto hover mejorado con animaciones"""
        def on_enter(e):
            button.configure(
                bg=self._lighten_color(original_color),
                relief="raised",
                bd=3
            )
        
        def on_leave(e):
            button.configure(
                bg=original_color,
                relief="raised", 
                bd=2
            )
        
        def on_click(e):
            button.configure(relief="sunken", bd=1)
            button.after(100, lambda: button.configure(relief="raised", bd=3))
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_click)
        
    def _lighten_color(self, color):
        """Crear una versión más clara del color para efectos hover"""
        # Simplificado: agregar opacidad visual
        if color == self.theme.PRIMARY:
            return "#E5354A"
        elif color == self.theme.SUCCESS:
            return "#2ECC71"
        elif color == self.theme.ERROR:
            return "#EC7063"
        elif color == self.theme.INFO:
            return "#5DADE2"
        elif color == "#9B59B6":
            return "#BB7ACF"
        elif color == "#E67E22":
            return "#F1975A"
        elif color == "#16A085":
            return "#48C9B0"
        elif color == "#F39C12":
            return "#F8C471"
        elif color == "#2E8B57":
            return "#3CB371"  # Verde más claro para hover
        else:
            return color
        
    def _create_excel_section_simple(self, parent):
        """Crear sección simplificada de archivo Excel"""
        excel_section = tk.LabelFrame(
            parent, 
            text="📊 Archivo de Pedidos", 
            font=("Arial", 12, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            relief="groove",
            bd=1
        )
        excel_section.pack(fill="x", padx=5, pady=5)
        
        # Contenedor principal con padding elegante
        main_container = tk.Frame(excel_section, bg=self.theme.WHITE)
        main_container.pack(fill="x", padx=15, pady=15)
        
        # Icono y título descriptivo
        header_frame = tk.Frame(main_container, bg=self.theme.WHITE)
        header_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            header_frame, 
            text="📄 Archivo Excel de Pedidos", 
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY
        ).pack(anchor="w")
        
        tk.Label(
            header_frame, 
            text="Debe estar ubicado en la carpeta 'Ordenes'", 
            font=("Arial", 9),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(2, 0))
        
        # Botón principal elegante para abrir Excel
        btn_container = tk.Frame(main_container, bg=self.theme.WHITE)
        btn_container.pack(fill="x", pady=(5, 0))
        
        self.btn_abrir_excel = tk.Button(
            btn_container, 
            text="📂 Abrir Archivo de Pedidos", 
            command=self.abrir_archivo_pedidos,
            bg="#2E8B57",  # Verde elegante
            fg=self.theme.WHITE, 
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            width=25
        )
        self.btn_abrir_excel.pack(anchor="w")
        
        # Efecto hover para el botón
        self._add_hover_effect(self.btn_abrir_excel, "#2E8B57")
        
        # Información de estado del archivo
        self.excel_status_frame = tk.Frame(main_container, bg=self.theme.WHITE)
        self.excel_status_frame.pack(fill="x", pady=(10, 0))
        
        self.excel_status_label = tk.Label(
            self.excel_status_frame,
            text="📋 Listo para procesar archivo Excel",
            font=("Arial", 9),
            bg=self.theme.WHITE,
            fg=self.theme.SUCCESS
        )
        self.excel_status_label.pack(anchor="w")
        
    def log(self, msg, color="#00FF00"):
        """Añadir mensaje al log con timestamp y color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {msg}"
        
        self.txt_log.configure(state="normal")
        self.txt_log.insert(tk.END, f"{formatted_msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.configure(state="disabled")
        self.root.update_idletasks()
        
    def actualizar_progreso(self, porcentaje, texto=""):
        """Actualizar la barra de progreso"""
        if hasattr(self, 'progress_var'):
            self.progress_var.set(porcentaje)
            self.progress_percent.set(f"{porcentaje:.0f}%")
            if texto:
                self.progress_text.set(texto)
            self.root.update_idletasks()
    
    def siguiente_paso(self):
        """Avanzar al siguiente paso del procesamiento"""
        if self.current_step < len(self.progress_steps):
            step_text = self.progress_steps[self.current_step]
            porcentaje = (self.current_step / (self.total_steps - 1)) * 100
            self.actualizar_progreso(porcentaje, step_text)
            self.current_step += 1
    
    def progreso_paso(self, paso, total_pasos, descripcion):
        """Actualizar progreso basado en pasos completados"""
        porcentaje = (paso / total_pasos) * 100
        self.actualizar_progreso(porcentaje, f"Paso {paso}/{total_pasos}: {descripcion}")
        
    def mostrar_salida(self, df):
        """Mostrar vista previa de la salida con formato mejorado"""
        self.txt_salida.configure(state="normal")
        self.txt_salida.delete("1.0", tk.END)
        
        if df.empty:
            self.txt_salida.insert(tk.END, "📭 No records in output.\n")
        else:
            # Mostrar columnas principales en el orden correcto
            cols_principales = ['ID PEDIDO', 'LOCAL', 'PROVEEDOR', 'FECHA_ENTREGA', 'SKU', 'CANTIDAD', 'OBSERVACION']
            cols_disponibles = [col for col in cols_principales if col in df.columns]
            
            if cols_disponibles:
                df_preview = df[cols_disponibles]
                header = f"📊 Total records: {len(df)}\n"
                header += f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                header += "=" * 80 + "\n\n"
                
                self.txt_salida.insert(tk.END, header)
                self.txt_salida.insert(tk.END, df_preview.head(20).to_string(index=False))
                
                if len(df) > 20:
                    self.txt_salida.insert(tk.END, f"\n\n... and {len(df)-20} more rows ...")
            else:
                self.txt_salida.insert(tk.END, df.head(20).to_string(index=False))
                
        self.txt_salida.configure(state="disabled")
        
    def refrescar_archivos(self):
        """Actualizar el estado del archivo Excel para la nueva interfaz"""
        os.makedirs(self.ORDENES_DIR, exist_ok=True)
        
        excel_files = [f for f in sorted(os.listdir(self.ORDENES_DIR)) if f.lower().endswith(('.xlsx', '.xls'))]
        
        # Actualizar el label de estado si existe
        if hasattr(self, 'excel_status_label'):
            if excel_files:
                archivo_principal = excel_files[0]
                file_path = os.path.join(self.ORDENES_DIR, archivo_principal)
                size = os.path.getsize(file_path) / 1024  # KB
                
                status_text = f"📂 Archivo: {archivo_principal} ({size:.1f} KB)"
                if len(excel_files) > 1:
                    status_text += f" (+{len(excel_files)-1} más)"
                
                self.excel_status_label.config(
                    text=status_text,
                    fg=self.theme.SUCCESS
                )
            else:
                self.excel_status_label.config(
                    text="⚠️ No se encontró archivo Excel en Ordenes",
                    fg=self.theme.WARNING
                )
        
        # Actualizar barra de estado
        self.status_bar.config(text=f"📄 {len(excel_files)} Excel files found • Ready for processing")
        self.log(f"🔄 File status updated: {len(excel_files)} Excel files found")
        
    def eliminar_archivo(self):
        """Eliminar todos los archivos Excel con confirmación mejorada"""
        excel_files = [f for f in os.listdir(self.ORDENES_DIR) if f.lower().endswith(('.xlsx', '.xls'))]
        
        if not excel_files:
            messagebox.showinfo("ℹ️ Información", "No hay archivos Excel para eliminar.")
            return
            
        # Diálogo de confirmación más detallado
        total_size = sum(os.path.getsize(os.path.join(self.ORDENES_DIR, excel_file)) 
                        for excel_file in excel_files) / 1024 / 1024  # MB
        
        confirm_msg = (
            f"🗑️ Delete all Excel files?\n\n"
            f"Files to delete: {len(excel_files)}\n"
            f"Total size: {total_size:.2f} MB\n\n"
            f"This action cannot be undone."
        )
        
        if messagebox.askyesno("🗑️ Confirmar Eliminación", confirm_msg):
            try:
                for excel_file in excel_files:
                    os.remove(os.path.join(self.ORDENES_DIR, excel_file))
                    
                self.log(f"🗑️ Deleted {len(excel_files)} Excel files ({total_size:.2f} MB)")
                self.refrescar_archivos()
                messagebox.showinfo("✅ Éxito", f"Se eliminaron exitosamente {len(excel_files)} archivos Excel.")
                
            except Exception as e:
                self.log(f"❌ Error deleting files: {e}")
                messagebox.showerror("❌ Error", f"Error eliminando archivos: {e}")
                
    def agregar_archivo(self):
        """Agregar archivos Excel con validación mejorada"""
        archivos = filedialog.askopenfilenames(
            title="Select Excel files",
            filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")],
            initialdir=os.path.expanduser("~/Desktop")
        )
        
        if archivos:
            try:
                copiados = 0
                total_size = 0
                
                for archivo in archivos:
                    nombre = os.path.basename(archivo)
                    destino = os.path.join(self.ORDENES_DIR, nombre)
                    
                    # Verificar si el archivo ya existe
                    if os.path.exists(destino):
                        if not messagebox.askyesno(
                            "📄 File Exists", 
                            f"File '{nombre}' already exists.\nOverwrite?"
                        ):
                            continue
                    
                    shutil.copy2(archivo, destino)
                    file_size = os.path.getsize(destino) / 1024  # KB
                    total_size += file_size
                    
                    self.log(f"📄 Copied: {nombre} ({file_size:.1f} KB)")
                    copiados += 1
                    
                self.refrescar_archivos()
                
                if copiados > 0:
                    messagebox.showinfo(
                        "✅ Éxito", 
                        f"Se agregaron exitosamente {copiados} archivos Excel.\n"
                        f"Tamaño total: {total_size:.1f} KB"
                    )
                    
            except Exception as e:
                self.log(f"❌ Error copiando archivos: {e}")
                messagebox.showerror("❌ Error", f"Error copiando archivos: {e}")
                
    def abrir_archivo_pedidos(self):
        """Abrir el archivo Excel de pedidos en la carpeta Ordenes"""
        try:
            # Buscar archivos Excel en la carpeta Ordenes
            excel_files = [f for f in os.listdir(self.ORDENES_DIR) if f.lower().endswith(('.xlsx', '.xls'))]
            
            if not excel_files:
                messagebox.showwarning(
                    "⚠️ Archivo No Encontrado", 
                    "No se encontró ningún archivo Excel en la carpeta 'Ordenes'.\n\n"
                    "Por favor, coloca el archivo de pedidos en la carpeta 'Ordenes' y vuelve a intentar."
                )
                self.excel_status_label.config(
                    text="⚠️ No se encontró archivo Excel en Ordenes",
                    fg=self.theme.WARNING
                )
                return
            
            # Si hay múltiples archivos, usar el primero
            archivo_excel = excel_files[0]
            archivo_path = os.path.join(self.ORDENES_DIR, archivo_excel)
            
            # Abrir el archivo
            os.startfile(archivo_path)
            self.log(f"📂 Opening Excel file: {archivo_excel}")
            
            # Actualizar status
            self.excel_status_label.config(
                text=f"📂 Archivo: {archivo_excel} ({len(excel_files)} archivos encontrados)",
                fg=self.theme.SUCCESS
            )
            
        except Exception as e:
            self.log(f"❌ Error opening Excel file: {e}")
            messagebox.showerror("❌ Error", f"No se puede abrir el archivo Excel: {e}")
            self.excel_status_label.config(
                text="❌ Error abriendo archivo Excel",
                fg=self.theme.ERROR
            )
    
    def abrir_full_xlsx(self):
        """Abrir archivo Full.xlsx con validación"""
        if os.path.exists(self.FULL_XLSX):
            try:
                os.startfile(self.FULL_XLSX)
                self.log("📋 Opening Full.xlsx")
            except Exception as e:
                self.log(f"❌ Error opening Full.xlsx: {e}")
                messagebox.showerror("❌ Error", f"No se puede abrir Full.xlsx: {e}")
        else:
            messagebox.showwarning("⚠️ Archivo No Encontrado", "Full.xlsx no existe en la carpeta Full-Agenda.")
            
    def abrir_agenda_xlsm(self):
        """Abrir archivo Agenda.xlsm con validación"""
        if os.path.exists(self.AGENDA_XLSM):
            try:
                os.startfile(self.AGENDA_XLSM)
                self.log("📅 Opening Agenda.xlsm")
            except Exception as e:
                self.log(f"❌ Error opening Agenda.xlsm: {e}")
                messagebox.showerror("❌ Error", f"No se puede abrir Agenda.xlsm: {e}")
        else:
            messagebox.showwarning("⚠️ File Not Found", "Agenda.xlsm does not exist in Full-Agenda folder.")
            
    def abrir_salida_xlsx(self):
        """Abrir archivo de salida con validación"""
        archivo_salida = self.get_nombre_archivo_salida()
        if os.path.exists(archivo_salida):
            try:
                os.startfile(archivo_salida)
                nombre_archivo = os.path.basename(archivo_salida)
                self.log(f"📤 Opening {nombre_archivo}")
            except Exception as e:
                self.log(f"❌ Error opening output file: {e}")
                messagebox.showerror("❌ Error", f"Cannot open output file: {e}")
        else:
            messagebox.showwarning(
                "⚠️ File Not Found", 
                "Output file does not exist.\nPlease run the processing first."
            )
            
    def abrir_carpeta_salidas(self):
        """Abrir carpeta Salidas donde se guardan los archivos procesados"""
        try:
            salidas_dir = os.path.join(self.BASE_DIR, "Salidas")
            if not os.path.exists(salidas_dir):
                os.makedirs(salidas_dir, exist_ok=True)
            os.startfile(salidas_dir)
            self.log("📁 Opening Salidas folder")
        except Exception as e:
            self.log(f"❌ Error opening Salidas folder: {e}")
            messagebox.showerror("❌ Error", f"Cannot open Salidas folder: {e}")
            
    def abrir_items_xlsx(self):
        """Abrir archivo Items C.Calzada con validación"""
        if os.path.exists(self.ITEMS_XLSX):
            try:
                os.startfile(self.ITEMS_XLSX)
                self.log("📊 Opening Items C.Calzada")
            except Exception as e:
                self.log(f"❌ Error opening Items.xlsx: {e}")
                messagebox.showerror("❌ Error", f"Cannot open Items.xlsx: {e}")
        else:
            messagebox.showwarning(
                "⚠️ File Not Found", 
                "Items.xlsx does not exist in Full-Agenda folder."
            )
            
    def abrir_reglas_especiales(self):
        """Abrir ventana de gestión de reglas especiales"""
        # Si ya está abierta, traerla al frente
        if self.ventana_reglas and self.ventana_reglas.winfo_exists():
            self.ventana_reglas.lift()
            self.ventana_reglas.focus_force()
            return
        
        try:
            self.log("⚙️ Opening Special Rules Manager...")
            dialog = RulesDialog(self.root)
            self.ventana_reglas = dialog.window
            self.log("✅ Rules Manager opened successfully")
        except Exception as e:
            self.log(f"❌ Error opening Rules Manager: {e}")
            messagebox.showerror(
                "❌ Error", 
                f"Cannot open Rules Manager:\n\n{str(e)}",
                parent=self.root
            )
    
    def abrir_gestion_agenda(self):
        """Abrir ventana de gestión de agenda de proveedores"""
        # Si ya está abierta, traerla al frente
        if self.ventana_agenda and self.ventana_agenda.winfo_exists():
            self.ventana_agenda.lift()
            self.ventana_agenda.focus_force()
            return
        
        try:
            self.log("📅 Opening Supplier Delivery Schedule Manager...")
            theme_colors = {
                'bg_main': self.theme.LIGHT_GRAY,
                'bg_card': self.theme.WHITE,
                'fg_text': self.theme.TEXT_PRIMARY,
                'accent': self.theme.SECONDARY,
                'button_bg': self.theme.PRIMARY,
                'button_hover': '#2980b9',
                'success': self.theme.SUCCESS,
                'warning': self.theme.WARNING
            }
            dialog = AgendaDialog(self.root, theme_colors)
            self.ventana_agenda = dialog.dialog
            self.log("✅ Agenda Manager opened successfully")
        except Exception as e:
            self.log(f"❌ Error opening Agenda Manager: {e}")
            messagebox.showerror(
                "❌ Error", 
                f"Cannot open Agenda Manager:\n\n{str(e)}",
                parent=self.root
            )
            
    def ejecutar_procesamiento(self):
        """Ejecutar el procesamiento completo con logging mejorado"""
        self.btn_procesar.config(state="disabled", text="🔄 PROCESANDO...")
        self.status_bar.config(text="🔄 Procesando pedidos, por favor espere...")
        
        # Reiniciar progreso
        self.current_step = 0
        
        try:
            # Paso 0: Inicializar
            self.siguiente_paso()
            self.log("=" * 80)
            self.log("🚀 INICIANDO PROCESAMIENTO DE PEDIDOS")
            self.log("=" * 80)
            self.log(f"📂 Directorio base: {self.BASE_DIR}")
            self.log(f"📅 Iniciado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Paso 1: Leer Excel
            self.siguiente_paso()
            self.log("📖 Paso 1: Leyendo archivos Excel...")
            df_pdfs = procesar_pdfs(self.ORDENES_DIR)
            excel_count = len([f for f in os.listdir(self.ORDENES_DIR) if f.lower().endswith(('.xlsx', '.xls'))])
            self.log(f"✅ Procesados {len(df_pdfs)} registros de {excel_count} archivos Excel")
            
            if df_pdfs.empty:
                self.log("⚠️ No records found in Excel files.")
                self.status_bar.config(text="⚠️ No data to process")
                return
                
            # Paso 2: Validar SKUs
            self.siguiente_paso()
            self.log("🔍 Paso 2: Validando Items C.Calzada...")
            df_items_valid, df_err_items, warnings_items = validar_skus_items(df_pdfs, self.ITEMS_XLSX)
            
            for warning in warnings_items:
                self.log(warning)
                
            self.log(f"✅ Registros válidos en items: {len(df_items_valid)}")
            if len(df_err_items) > 0:
                self.log(f"⚠️ Registros no encontrados en items: {len(df_err_items)}")
            
            # Paso 3: Mapear proveedores
            self.siguiente_paso()
            self.log("�️ Paso 3: Mapeando proveedores desde Full.xlsx...")
            region_seleccionada = self.region_var.get().strip() or "119"
            self.log(f"📍 Usando región: {region_seleccionada}")
            df_map, df_err_prov, warnings = mapear_proveedor_por_sku(df_items_valid, self.FULL_XLSX, region_seleccionada)
            
            for warning in warnings:
                self.log(warning)
                
            self.log(f"✅ Valid records with supplier: {len(df_map)}")
            if len(df_err_prov) > 0:
                self.log(f"⚠️ Records with price errors: {len(df_err_prov)}")
                
            # Paso 4: Fechas y observaciones
            self.siguiente_paso()
            self.log("📅 Paso 4: Procesando fechas y observaciones con AgendaManager...")
            df_final_valid, df_err_fecha = rellenar_fecha_entrega_y_observacion(df_map)
            
            # Asegurar índices únicos después del procesamiento
            df_final_valid = df_final_valid.reset_index(drop=True)
            df_err_fecha = df_err_fecha.reset_index(drop=True)
            
            self.log(f"✅ Registros con fecha asignada: {len(df_final_valid)}")
            if len(df_err_fecha) > 0:
                self.log(f"⚠️ Registros con errores de agenda: {len(df_err_fecha)}")
                
            # Asegurar índices únicos en todos los DataFrames de errores antes del concat
            df_err_items = df_err_items.reset_index(drop=True)
            df_err_prov = df_err_prov.reset_index(drop=True)
            
            # Eliminar columnas duplicadas si existen
            if len(df_err_items.columns) != len(set(df_err_items.columns)):
                self.log("⚠️ Columnas duplicadas en df_err_items, eliminando...")
                df_err_items = df_err_items.loc[:, ~df_err_items.columns.duplicated()]
            
            if len(df_err_prov.columns) != len(set(df_err_prov.columns)):
                self.log("⚠️ Columnas duplicadas en df_err_prov, eliminando...")
                df_err_prov = df_err_prov.loc[:, ~df_err_prov.columns.duplicated()]
            
            if len(df_err_fecha.columns) != len(set(df_err_fecha.columns)):
                self.log("⚠️ Columnas duplicadas en df_err_fecha, eliminando...")
                df_err_fecha = df_err_fecha.loc[:, ~df_err_fecha.columns.duplicated()]
            
            # Combinar todos los errores
            df_errores = pd.concat([df_err_items, df_err_prov, df_err_fecha], ignore_index=True)
            
            # Paso 5: Asignar IDs finales
            self.siguiente_paso()
            self.log("🏷️ Paso 5: Asignando IDs finales...")
            df_final = asignar_id_final(df_final_valid)
            
            # Paso 6: Guardando resultados
            self.siguiente_paso()
            self.log("💾 Paso 6: Guardando resultados en Excel...")
            # Obtener nombre dinámico del archivo
            archivo_salida = self.get_nombre_archivo_salida()
            nombre_archivo = os.path.basename(archivo_salida)
            
            with pd.ExcelWriter(archivo_salida, engine="openpyxl") as writer:
                df_final.to_excel(writer, sheet_name="PEDIDOS_CD", index=False)
                if not df_errores.empty:
                    df_errores.to_excel(writer, sheet_name="Errors", index=False)
                    
            self.log(f"✅ Archivo guardado: {nombre_archivo}")
            
            # Paso 7: Formato profesional
            self.siguiente_paso()
            self.log("🎨 Paso 7: Aplicando formato profesional...")
            formatear_excel_salida(archivo_salida)
            
            # Paso 8: Completado
            self.siguiente_paso()
            
            # Mostrar resumen
            self.log("=" * 80)
            self.log("📊 RESUMEN DEL PROCESAMIENTO:")
            self.log(f"   • Total de registros procesados: {len(df_final)}")
            self.log(f"   • Total de errores: {len(df_errores)}")
            self.log(f"   • Archivo de salida: {nombre_archivo}")
            self.log(f"   • Completado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.log("🎉 PROCESAMIENTO COMPLETADO EXITOSAMENTE")
            self.log("=" * 80)
            
            # Mostrar vista previa
            self.mostrar_salida(df_final)
            
            # Actualizar barra de estado
            self.status_bar.config(
                text=f"✅ Procesamiento completado: {len(df_final)} registros, {len(df_errores)} errores • Creado por Lucas Gnemmi"
            )
            
            # Mostrar mensaje de éxito
            result_msg = (
                f"🎉 ¡Procesamiento completado exitosamente!\n\n"
                f"📊 Registros procesados: {len(df_final)}\n"
                f"❌ Errores encontrados: {len(df_errores)}\n"
                f"📁 Archivo guardado: {nombre_archivo}\n\n"
                f"¿Desea abrir el archivo de resultados?"
            )
            
            if messagebox.askyesno("🎉 Procesamiento Completado", result_msg):
                self.abrir_salida_xlsx()
                
        except Exception as e:
            import traceback
            error_msg = f"❌ ERROR CRÍTICO: {str(e)}"
            self.log(error_msg)
            self.log("📋 Traceback completo:")
            for line in traceback.format_exc().split('\n'):
                if line.strip():
                    self.log(line)
            self.status_bar.config(text="❌ Error en procesamiento")
            messagebox.showerror(
                "❌ Error Crítico", 
                f"Error durante el procesamiento:\n\n{str(e)}\n\nRevise el registro de actividad para más detalles."
            )
            
        finally:
            self.btn_procesar.config(state="normal", text="🚀 PROCESAR PEDIDOS")
            
    def ejecutar_procesamiento_async(self):
        """Ejecutar procesamiento en hilo separado para mantener UI responsiva"""
        threading.Thread(target=self.ejecutar_procesamiento, daemon=True).start()
        
    def run(self):
        """Iniciar la aplicación con mensaje de bienvenida"""
        self.log("🚀 Sistema de Procesamiento de Pedidos v2.0 iniciado")
        self.log(f"💻 Created by Lucas Gnemmi")
        self.log(f"📂 Working directory: {self.BASE_DIR}")
        self.log("🔧 System ready for processing")
        self.root.mainloop()

def main():
    """Función principal de la aplicación"""
    try:
        app = ModernGUI()
        app.run()
    except Exception as e:
        messagebox.showerror(
            "❌ Startup Error", 
            f"Error starting application:\n\n{str(e)}"
        )

if __name__ == "__main__":
    main()
