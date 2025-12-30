"""
Sistema de Procesamiento de Pedidos - Interfaz Moderna CustomTkinter
Creado por Lucas Gnemmi
Versión: 3.0 - Modernización UI

Sistema profesional para el procesamiento de pedidos con interfaz gráfica moderna.
Incluye validación de SKUs, mapeo de proveedores y generación de archivos Excel formateados.
Migrado a CustomTkinter para una experiencia visual moderna.
"""

import os
import sys

# Agregar directorio del script al path (para imports locales)
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Agregar carpeta libs al path para importar librerías empaquetadas
libs_path = os.path.join(script_dir, 'libs')
if os.path.exists(libs_path) and libs_path not in sys.path:
    sys.path.insert(0, libs_path)

import shutil
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
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
from products_dialog import ProductsDialog

# Configurar apariencia de CustomTkinter - DARK MODE MODERNO 🌙
ctk.set_appearance_mode("dark")  # DARK MODE por defecto
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Configuración de colores del tema MODERNO 2024
class ModernTheme:
    """Tema moderno con paleta equilibrada y elegante"""
    
    # FONDOS - Tonos oscuros suaves
    BG_DARK = "#1a1d29"          # Azul oscuro profundo
    BG_SURFACE = "#242837"       # Superficie elevada
    BG_CARD = "#2d3142"          # Cards con buen contraste
    
    # COLORES PRINCIPALES - Vibrantes pero elegantes
    PRIMARY = "#00d4ff"          # Cyan brillante (acento principal)
    PRIMARY_DARK = "#00b8d9"     # Cyan oscuro para hover
    SECONDARY = "#a78bfa"        # Lavanda suave
    ACCENT = "#fb7185"           # Rosa coral
    
    # COLORES FUNCIONALES - Saturados y visibles
    SUCCESS = "#34d399"          # Verde menta
    WARNING = "#fbbf24"          # Amarillo dorado
    ERROR = "#f87171"            # Rojo coral
    INFO = "#60a5fa"             # Azul cielo
    
    # TEXTO - Máximo contraste
    TEXT_PRIMARY = "#ffffff"     # Blanco puro
    TEXT_SECONDARY = "#e5e7eb"   # Gris muy claro
    TEXT_MUTED = "#9ca3af"       # Gris medio
    
    # EFECTOS
    BORDER = "#3f4555"           # Bordes visibles
    HOVER_BG = "#2d3142"         # Hover sutil
    
    # LEGACY
    WHITE = "#ffffff"
    DARK = "#1a1d29"
    LIGHT_GRAY = "#9ca3af"
    MEDIUM_GRAY = "#2d3142"
    PROGRESS_BG = "#242837"
    PROGRESS_FILL = "#00d4ff"
    
    # ESTILOS
    CORNER_RADIUS = 12
    CARD_PADDING = 24
    BUTTON_HEIGHT = 48
    SPACING = 20
    
    # TIPOGRAFÍA - Más grande
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_TITLE = 26
    FONT_SIZE_SUBTITLE = 18
    FONT_SIZE_BODY = 14
    FONT_SIZE_SMALL = 12

class ModernGUI:
    """
    Interfaz gráfica moderna para el sistema de procesamiento de órdenes DHL
    Created by Lucas Gnemmi
    Migrado a CustomTkinter v3.0
    """
    
    def __init__(self):
        self.root = ctk.CTk()
        self.theme = ModernTheme()
        
        # Variables para ventanas únicas
        self.ventana_agenda = None
        self.ventana_reglas = None
        self.ventana_productos = None
        
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
        
        # Maximizar después de crear todos los widgets para evitar redimensionamiento
        self.root.after(10, lambda: self.root.state('zoomed'))
        
    def setup_main_window(self):
        """Configuración de la ventana principal moderna con dark mode"""
        self.root.title("Sistema de Procesamiento de Pedidos by Lucas Gnemmi - v3.0")
        
        # Configurar icono de la ventana
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dhl_icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            pass  # print(f"No se pudo cargar el icono: {e}")
        
        # Dimensiones mínimas (no maximizar aquí, se hace al final)
        self.root.minsize(1300, 900)
        
        # Hacer la ventana responsiva
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Configurar estilo TTK moderno (para Treeview) - ATADO A self.root
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self._configure_styles()
        
    def _configure_styles(self):
        """Configurar estilos modernos para dark mode"""
        # Estilo para Treeview - Dark Mode
        self.style.configure(
            "Treeview",
            background=self.theme.BG_CARD,
            foreground=self.theme.TEXT_PRIMARY,
            fieldbackground=self.theme.BG_CARD,
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY),
            rowheight=40,
            borderwidth=0
        )
        
        self.style.map('Treeview',
            background=[('selected', self.theme.PRIMARY)],
            foreground=[('selected', self.theme.TEXT_PRIMARY)]
        )
        
        # Estilo para headers del Treeview
        self.style.configure(
            "Treeview.Heading",
            background=self.theme.BG_SURFACE,
            foreground=self.theme.TEXT_PRIMARY,
            relief="flat",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY, "bold")
        )
        
        self.style.map("Treeview.Heading",
            background=[('active', self.theme.PRIMARY)]
        )
        
    def setup_paths(self):
        """Configuración de rutas del sistema"""
        # Detectar si estamos ejecutando desde un ejecutable de PyInstaller
        if getattr(sys, 'frozen', False):
            # Si es ejecutable, usar el directorio del ejecutable
            self.BASE_DIR = os.path.dirname(sys.executable)
        else:
            # Si es script Python normal, usar el directorio del script
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
        """Crear header moderno estilo web"""
        # Header con gradiente visual
        header = ctk.CTkFrame(self.root, fg_color=self.theme.BG_CARD, height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Barra superior con acento
        accent_bar = ctk.CTkFrame(header, fg_color=self.theme.PRIMARY, height=4)
        accent_bar.pack(fill="x")
        
        # Contenedor interno
        content = ctk.CTkFrame(header, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=28, pady=16)
        
        # Título con icono
        title = ctk.CTkLabel(
            content,
            text="Sistema - Procesamiento de Pedidos",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_TITLE, "bold"),
            text_color=self.theme.PRIMARY
        )
        title.pack(side="left")
        
        # Contenedor derecho para versión y botón de actualización
        right_container = ctk.CTkFrame(content, fg_color="transparent")
        right_container.pack(side="right")
        
        # Badge de versión con acento
        version_frame = ctk.CTkFrame(right_container, fg_color=self.theme.PRIMARY, 
                                     corner_radius=20, height=36)
        version_frame.pack(side="left", padx=(0, 10))
        
        version = ctk.CTkLabel(
            version_frame,
            text="v3.0 Modern",
            font=(self.theme.FONT_FAMILY, 12, "bold"),
            text_color="#2c3e50"  # Azul oscuro en lugar de negro
        )
        version.pack(padx=18, pady=6)
        
        # Botón de actualización con logo de GitHub
        update_btn = ctk.CTkButton(
            right_container,
            text="⬇ Actualizar",
            command=self.verificar_actualizaciones,
            fg_color=self.theme.SECONDARY,
            text_color=self.theme.TEXT_PRIMARY,
            font=(self.theme.FONT_FAMILY, 12, "bold"),
            corner_radius=20,
            height=36,
            width=130,
            hover_color=self._darken_color(self.theme.SECONDARY),
            border_width=0
        )
        update_btn.pack(side="left")

        
    def _create_main_layout(self):
        """Crear layout moderno con cards y espaciado amplio"""
        # Contenedor principal con fondo oscuro
        main_container = ctk.CTkFrame(self.root, fg_color=self.theme.BG_DARK, corner_radius=0)
        main_container.pack(fill="both", expand=True, side="top")
        
        # Configurar grid para layout responsive
        main_container.grid_columnconfigure(0, weight=0, minsize=420)  # Panel izquierdo con ancho mínimo
        main_container.grid_columnconfigure(1, weight=1)  # Panel derecho expansible
        main_container.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo con scrollbar
        left_frame = ctk.CTkScrollableFrame(
            main_container,
            fg_color="transparent",
            width=420,
            scrollbar_button_color=self.theme.PRIMARY,
            scrollbar_button_hover_color=self.theme.PRIMARY_DARK
        )
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(self.theme.SPACING, self.theme.SPACING//2), pady=self.theme.SPACING)
        
        # Panel derecho - expansible
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(self.theme.SPACING//2, self.theme.SPACING), pady=self.theme.SPACING)
        
        # Crear paneles
        self._create_left_panel(left_frame)
        self._create_center_panel(right_frame)
        
    def _create_styled_labelframe(self, parent, text, icon="", pack_options=None):
        """Crear card moderno con estilo dark mode premium"""
        # Card container con bordes redondeados
        card = ctk.CTkFrame(
            parent,
            fg_color=self.theme.BG_CARD,
            corner_radius=self.theme.CORNER_RADIUS,
            border_width=1,
            border_color=self.theme.BORDER
        )
        if pack_options:
            card.pack(**pack_options)
        
        # Header del card con gradiente
        header_frame = ctk.CTkFrame(
            card,
            fg_color=self.theme.BG_SURFACE,
            corner_radius=self.theme.CORNER_RADIUS,
            height=50
        )
        header_frame.pack(fill="x", padx=2, pady=(2, 0))
        header_frame.pack_propagate(False)
        
        # Título del card con icono más grande
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {text}",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SUBTITLE, "bold"),
            text_color=self.theme.TEXT_PRIMARY
        )
        title_label.pack(anchor="w", padx=self.theme.CARD_PADDING, pady=12)
        
        # Área de contenido con padding
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=self.theme.CARD_PADDING, pady=self.theme.CARD_PADDING)
        
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
        """Crear sección de gestión de archivos Excel (LEGACY - NO USADA)"""
        pass  # Esta función no se usa, mantenida por compatibilidad
            
    def _create_processing_section(self, parent):
        """Crear sección de pasos de procesamiento"""
        processing_section = self._create_styled_labelframe(
            parent,
            "Pasos del Procesamiento",
            "⚙️",
            {"fill": "x", "padx": 5, "pady": 3}
        )
        
        steps_container = ctk.CTkFrame(processing_section, fg_color="transparent")
        steps_container.pack(fill="x", padx=10, pady=3)
        
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
        region_frame = ctk.CTkFrame(steps_container, fg_color="transparent")
        region_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            region_frame, 
            text="3.", 
            font=(self.theme.FONT_FAMILY, 16, "bold"), 
            text_color=self.theme.ACCENT, 
            width=30
        ).pack(side="left", padx=(0, 10))
        
        region_config = ctk.CTkFrame(region_frame, fg_color="transparent")
        region_config.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            region_config, 
            text="Región:", 
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY, "bold"), 
            text_color=self.theme.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 10))
        
        self.region_var = tk.StringVar(value="119")
        self.region_entry = ctk.CTkEntry(
            region_config,
            textvariable=self.region_var,
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY, "bold"),
            width=100,
            height=40,
            justify="center",
            corner_radius=8,
            border_width=2,
            border_color=self.theme.PRIMARY,
            fg_color=self.theme.BG_SURFACE,
            text_color=self.theme.TEXT_PRIMARY
        )
        self.region_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            region_config, 
            text="(por defecto: 119)", 
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL), 
            text_color=self.theme.TEXT_SECONDARY
        ).pack(side="left")
        
        # Paso 4: Procesar
        process_frame = ctk.CTkFrame(steps_container, fg_color="transparent")
        process_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            process_frame, 
            text="4.", 
            font=(self.theme.FONT_FAMILY, 16, "bold"), 
            text_color=self.theme.ACCENT, 
            width=30
        ).pack(side="left", padx=(0, 10))
        
        self.btn_procesar = ctk.CTkButton(
            process_frame, 
            text="🚀 PROCESAR PEDIDOS", 
            command=self.ejecutar_procesamiento_async,
            fg_color="#2c3e50",  # Azul oscuro
            text_color="#ffffff",  # Blanco puro
            font=(self.theme.FONT_FAMILY, 15, "bold"),
            corner_radius=self.theme.CORNER_RADIUS,
            height=45,
            hover_color="#34495e",  # Más oscuro
            border_width=0
        )
        self.btn_procesar.pack(side="left", fill="x", expand=True)
        
    def _create_step_button(self, parent, step_num, text, command, color):
        """Crear un botón de paso numerado"""
        step_frame = ctk.CTkFrame(parent, fg_color="transparent")
        step_frame.pack(fill="x", pady=2)
        
        ctk.CTkLabel(
            step_frame, 
            text=f"{step_num}.", 
            font=(self.theme.FONT_FAMILY, 16, "bold"), 
            text_color=self.theme.ACCENT, 
            width=30
        ).pack(side="left", padx=(0, 10))
        
        btn = ctk.CTkButton(
            step_frame, 
            text=text, 
            command=command,
            fg_color=color,
            text_color=self.theme.TEXT_PRIMARY, 
            font=(self.theme.FONT_FAMILY, 13, "bold"),
            corner_radius=self.theme.CORNER_RADIUS,
            height=38,
            hover_color=self._darken_color(color),
            border_width=0
        )
        btn.pack(side="left", fill="x", expand=True)
        
    def _create_quick_access_section(self, parent):
        """Crear sección de accesos rápidos"""
        quick_section = self._create_styled_labelframe(
            parent,
            "Acceso Rápido",
            "🔗",
            {"fill": "x", "padx": 5, "pady": 3}
        )
        
        quick_container = ctk.CTkFrame(quick_section, fg_color="transparent")
        quick_container.pack(fill="x", padx=10, pady=3)
        
        quick_buttons = [
            ("⚙️ Reglas Especiales", self.abrir_reglas_especiales, self.theme.SECONDARY),
            ("📦 Maestra C.Calzada", self.abrir_gestion_productos, self.theme.WARNING),
            ("📁 Abrir Carpeta Salidas", self.abrir_carpeta_salidas, self.theme.SUCCESS),
        ]
        for text, command, color in quick_buttons:
            btn = ctk.CTkButton(
                quick_container, 
                text=text, 
                command=command,
                fg_color=color,
                text_color=self.theme.TEXT_PRIMARY, 
                font=(self.theme.FONT_FAMILY, 13, "bold"),
                corner_radius=self.theme.CORNER_RADIUS,
                height=40,
                hover_color=self._darken_color(color),
                border_width=0
            )
            btn.pack(fill="x", pady=2)
            
    def _create_center_panel(self, parent):
        """Crear panel central con logs y resultados"""
        # Panel de logs
        self._create_log_panel(parent)
        
        # Panel de progreso
        self._create_progress_panel(parent)
        
        # Panel de vista previa
        self._create_preview_panel(parent)
    

        
    def _create_log_panel(self, parent):
        """Crear panel de logs con estilo terminal moderno dark"""
        log_frame = self._create_styled_labelframe(
            parent, 
            "Registro de Actividad", 
            "📜",
            {"fill": "both", "expand": True, "pady": (0, self.theme.SPACING)}
        )
        
        # Área de texto del terminal moderno
        self.txt_log = ctk.CTkTextbox(
            log_frame,
            height=280,
            font=("Cascadia Code", 13),
            fg_color=self.theme.BG_SURFACE,
            text_color=self.theme.TEXT_PRIMARY,
            wrap="word",
            corner_radius=8,
            border_width=1,
            border_color=self.theme.BORDER
        )
        self.txt_log.pack(fill="both", expand=True)
        
    def _create_progress_panel(self, parent):
        """Crear panel de barra de progreso moderna"""
        progress_frame = self._create_styled_labelframe(
            parent, 
            "Progreso del Procesamiento", 
            "⚡",
            {"fill": "x", "pady": self.theme.SPACING}
        )
        
        # Texto del progreso
        self.progress_text = ctk.CTkLabel(
            progress_frame,
            text="Listo para procesar...",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY, "bold"),
            text_color=self.theme.TEXT_PRIMARY
        )
        self.progress_text.pack(anchor="w", pady=(0, 10))
        
        # Barra de progreso moderna
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            width=400,
            height=24,
            corner_radius=12,
            progress_color=self.theme.PRIMARY,
            fg_color=self.theme.BG_SURFACE,
            border_width=1,
            border_color=self.theme.BORDER
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=5)
        
        # Porcentaje
        self.progress_percent_label = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY, "bold"),
            text_color=self.theme.ACCENT
        )
        self.progress_percent_label.pack(anchor="e", pady=(5, 0))
        
    def _create_preview_panel(self, parent):
        """Crear panel de vista previa moderno"""
        preview_frame = self._create_styled_labelframe(
            parent, 
            "Vista Previa de Resultados", 
            "📊",
            {"fill": "both", "expand": True, "pady": (self.theme.SPACING, 0)}
        )
        
        # Área de texto moderna
        self.txt_salida = ctk.CTkTextbox(
            preview_frame,
            height=300,
            font=("Cascadia Code", 13),
            fg_color=self.theme.BG_SURFACE,
            text_color=self.theme.TEXT_PRIMARY,
            wrap="none",
            corner_radius=8,
            border_width=1,
            border_color=self.theme.BORDER
        )
        self.txt_salida.pack(fill="both", expand=True)
        
    def _create_footer(self):
        """Crear footer moderno con barra de estado"""
        # Footer con estilo moderno
        footer_container = ctk.CTkFrame(self.root, fg_color=self.theme.BG_SURFACE, height=40, corner_radius=0)
        footer_container.pack(side="bottom", fill="x")
        footer_container.pack_propagate(False)
        
        # Línea accent superior
        accent_line = ctk.CTkFrame(footer_container, fg_color=self.theme.ACCENT, height=3, corner_radius=0)
        accent_line.pack(fill="x")
        
        # Contenido del footer
        status_frame = ctk.CTkFrame(footer_container, fg_color="transparent")
        status_frame.pack(fill="both", expand=True, padx=20, pady=8)
        
        # Estado del sistema
        self.status_bar = ctk.CTkLabel(
            status_frame, 
            text="✅ Sistema listo para procesar", 
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            text_color=self.theme.SUCCESS
        )
        self.status_bar.pack(side="left")
        
        # Info del creador
        creator_label = ctk.CTkLabel(
            status_frame,
            text="💻 Creado por Lucas Gnemmi | DHL System v3.0",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            text_color=self.theme.TEXT_SECONDARY
        )
        creator_label.pack(side="right")
        
        # Footer ya está creado con CustomTkinter en _create_footer()
        
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
        elif color == "#8E44AD":
            return "#A569BD"
        else:
            return color
    
    def _darken_color(self, color):
        """Crear una versión más oscura del color para efectos de hover más visibles"""
        if color == self.theme.PRIMARY:
            return "#0066cc"  # Más claro para mejor contraste
        elif color == self.theme.SECONDARY:  # Purple
            return "#7c3aed"  # Más vibrante
        elif color == self.theme.SUCCESS:
            return "#059669"  # Verde más intenso
        elif color == self.theme.ERROR:
            return "#dc2626"  # Rojo más claro
        elif color == self.theme.WARNING:
            return "#d97706"  # Naranja más intenso
        elif color == self.theme.INFO:
            return "#0ea5e9"  # Azul más claro
        elif color == "#9B59B6":  # Step buttons purple
            return "#8b5cf6"  # Más vibrante
        elif color == "#3498DB":  # Step buttons blue
            return "#2563eb"  # Más intenso
        elif color == "#E67E22":
            return "#ea580c"  # Más claro
        elif color == "#16A085":
            return "#0d9488"  # Verde azulado más claro
        elif color == "#F39C12":
            return "#f59e0b"  # Amarillo más intenso
        elif color == "#2E8B57":
            return "#059669"  # Verde más vibrante
        elif color == "#8E44AD":
            return "#7c3aed"  # Púrpura más claro
        else:
            # Para colores desconocidos, intentar oscurecer automáticamente
            if color.startswith('#'):
                try:
                    # Convertir hex a RGB
                    hex_color = color.lstrip('#')
                    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    # Oscurecer reduciendo cada componente en 30
                    darker_rgb = tuple(max(0, c - 30) for c in rgb)
                    return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"
                except:
                    pass
            return color
        
    def _create_excel_section_simple(self, parent):
        """Crear sección simplificada de archivo Excel"""
        excel_section = self._create_styled_labelframe(
            parent,
            "Archivo de Pedidos",
            "📊",
            {"fill": "x", "padx": 5, "pady": 3}
        )
        
        # Contenedor principal
        main_container = ctk.CTkFrame(excel_section, fg_color="transparent")
        main_container.pack(fill="x", padx=10, pady=3)
        
        # Descripción
        ctk.CTkLabel(
            main_container, 
            text="📄 Archivo Excel de Pedidos", 
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_BODY, "bold"),
            text_color=self.theme.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 5))
        
        ctk.CTkLabel(
            main_container, 
            text="Debe estar ubicado en la carpeta 'Ordenes'", 
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            text_color=self.theme.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 15))
        
        # Botón principal para abrir Excel
        self.btn_abrir_excel = ctk.CTkButton(
            main_container, 
            text="📂 Abrir Archivo de Pedidos", 
            command=self.abrir_archivo_pedidos,
            fg_color="#27ae60",  # Verde oscuro
            text_color="#ffffff",  # Blanco puro
            font=(self.theme.FONT_FAMILY, 13, "bold"),
            corner_radius=self.theme.CORNER_RADIUS,
            height=40,
            hover_color="#2ecc71",  # Verde hover
            border_width=0
        )
        self.btn_abrir_excel.pack(fill="x", pady=(0, 15))
        
        # Información de estado del archivo
        self.excel_status_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        self.excel_status_frame.pack(fill="x")
        
        self.excel_status_label = ctk.CTkLabel(
            self.excel_status_frame,
            text="📋 Listo para procesar archivo Excel",
            font=(self.theme.FONT_FAMILY, self.theme.FONT_SIZE_SMALL),
            text_color=self.theme.SUCCESS
        )
        self.excel_status_label.pack(anchor="w")
        
    def log(self, msg, color="#00FF00"):
        """Añadir mensaje al log con timestamp y color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Limpiar mensaje de caracteres que puedan causar problemas de codificación
        try:
            # Intentar codificar/decodificar para detectar problemas
            msg_safe = str(msg).encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        except:
            # Si falla, usar representación ASCII
            msg_safe = repr(msg)
        
        formatted_msg = f"[{timestamp}] {msg_safe}\n"
        
        # CTkTextbox no necesita cambiar estado, siempre es editable
        try:
            self.txt_log.insert("end", formatted_msg)
            self.txt_log.see("end")
        except Exception as e:
            # Si falla el insert, intentar sin emojis
            msg_ascii = formatted_msg.encode('ascii', errors='ignore').decode('ascii')
            self.txt_log.insert("end", msg_ascii)
            self.txt_log.see("end")
        
        self.root.update_idletasks()
        
    def actualizar_progreso(self, porcentaje, texto=""):
        """Actualizar la barra de progreso"""
        if hasattr(self, 'progress_bar'):
            self.progress_bar.set(porcentaje / 100)  # CTkProgressBar usa valores 0-1
            self.progress_percent_label.configure(text=f"{porcentaje:.0f}%")
            if texto and hasattr(self, 'progress_text'):
                self.progress_text.configure(text=texto)
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
        # CTkTextbox no necesita cambiar estado
        self.txt_salida.delete("0.0", "end")
        
        if df.empty:
            self.txt_salida.insert("0.0", "📭 No records in output.\n")
        else:
            # Mostrar columnas principales en el orden correcto
            cols_principales = ['ID PEDIDO', 'LOCAL', 'PROVEEDOR', 'FECHA_ENTREGA', 'SKU', 'CANTIDAD', 'OBSERVACION']
            cols_disponibles = [col for col in cols_principales if col in df.columns]
            
            if cols_disponibles:
                df_preview = df[cols_disponibles]
                header = f"📊 Total records: {len(df)}\n"
                header += f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                header += "=" * 80 + "\n\n"
                
                self.txt_salida.insert("0.0", header)
                self.txt_salida.insert("end", df_preview.head(20).to_string(index=False))
                
                if len(df) > 20:
                    self.txt_salida.insert("end", f"\n\n... and {len(df)-20} more rows ...")
            else:
                self.txt_salida.insert("end", df.head(20).to_string(index=False))
        
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
                
                self.excel_status_label.configure(
                    text=status_text,
                    text_color=self.theme.SUCCESS
                )
            else:
                self.excel_status_label.configure(
                    text="⚠️ No se encontró archivo Excel en Ordenes",
                    text_color=self.theme.WARNING
                )
        
        # Actualizar barra de estado
        self.status_bar.configure(text=f"📄 {len(excel_files)} Excel files found • Ready for processing")
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
                self.excel_status_label.configure(
                    text="⚠️ No se encontró archivo Excel en Ordenes",
                    text_color=self.theme.WARNING
                )
                return
            
            # Si hay múltiples archivos, usar el primero
            archivo_excel = excel_files[0]
            archivo_path = os.path.join(self.ORDENES_DIR, archivo_excel)
            
            # Abrir el archivo
            os.startfile(archivo_path)
            self.log(f"📂 Opening Excel file: {archivo_excel}")
            
            # Actualizar status
            self.excel_status_label.configure(
                text=f"📂 Archivo: {archivo_excel} ({len(excel_files)} archivos encontrados)",
                text_color=self.theme.SUCCESS
            )
            
        except Exception as e:
            self.log(f"❌ Error opening Excel file: {e}")
            messagebox.showerror("❌ Error", f"No se puede abrir el archivo Excel: {e}")
            self.excel_status_label.configure(
                text="❌ Error abriendo archivo Excel",
                text_color=self.theme.ERROR
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
            
    # DEPRECATED: Ya no se usa Items.xlsx, ahora se usa products.json
    # def abrir_items_xlsx(self):
    #     """Abrir archivo Items C.Calzada con validación"""
    #     if os.path.exists(self.ITEMS_XLSX):
    #         try:
    #             os.startfile(self.ITEMS_XLSX)
    #             self.log("📊 Opening Items C.Calzada")
    #         except Exception as e:
    #             self.log(f"❌ Error opening Items.xlsx: {e}")
    #             messagebox.showerror("❌ Error", f"Cannot open Items.xlsx: {e}")
    #     else:
    #         messagebox.showwarning(
    #             "⚠️ File Not Found", 
    #             "Items.xlsx does not exist in Full-Agenda folder."
    #         )
            
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
            self.ventana_reglas.lift()
            # NO usar -topmost porque interfiere con messageboxes
            self.ventana_reglas.focus_force()
            self.log("✅ Rules Manager opened successfully")
        except Exception as e:
            self.log(f"❌ Error opening Rules Manager: {e}")
            messagebox.showerror(
                "❌ Error", 
                f"Cannot open Rules Manager:\n\n{str(e)}",
                parent=self.root
            )
    
    def abrir_gestion_productos(self):
        """Abrir ventana de gestión de productos (maestra SKU)"""
        # Si ya está abierta, traerla al frente
        if self.ventana_productos and self.ventana_productos.winfo_exists():
            self.ventana_productos.lift()
            self.ventana_productos.focus_force()
            return
        
        try:
            self.log("📦 Opening Maestra C.Calzada...")
            dialog = ProductsDialog(self.root)
            self.ventana_productos = dialog.window
            self.ventana_productos.lift()
            self.ventana_productos.attributes('-topmost', True)
            self.ventana_productos.after(100, lambda: self.ventana_productos.attributes('-topmost', False))
            self.ventana_productos.focus_force()  # Traer al frente
            self.log("✅ Maestra C.Calzada opened successfully")
        except Exception as e:
            self.log(f"❌ Error opening Maestra C.Calzada: {e}")
            messagebox.showerror(
                "❌ Error", 
                f"Cannot open Maestra C.Calzada:\n\n{str(e)}",
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
                'bg_main': self.theme.BG_DARK,        # Fondo oscuro
                'bg_card': self.theme.BG_CARD,        # Card oscuro  
                'bg_surface': self.theme.BG_SURFACE,  # Superficie
                'fg_text': self.theme.TEXT_PRIMARY,   # Texto blanco
                'fg_secondary': self.theme.TEXT_SECONDARY, # Texto secundario
                'accent': self.theme.PRIMARY,         # Acento primario
                'accent_hover': self.theme.PRIMARY_DARK, # Hover del acento
                'secondary': self.theme.SECONDARY,    # Color secundario
                'button_bg': self.theme.BG_CARD,      # Fondo de botón
                'button_hover': self.theme.BORDER,    # Hover de botón
                'success': self.theme.SUCCESS,        # Verde de éxito
                'warning': self.theme.WARNING,        # Amarillo de advertencia
                'error': self.theme.ERROR,            # Rojo de error
                'info': self.theme.INFO               # Azul de información
            }
            dialog = AgendaDialog(self.root, theme_colors)
            self.ventana_agenda = dialog.dialog
            self.ventana_agenda.lift()
            self.ventana_agenda.attributes('-topmost', True)
            self.ventana_agenda.after(100, lambda: self.ventana_agenda.attributes('-topmost', False))
            self.ventana_agenda.focus_force()  # Traer al frente
            self.log("✅ Agenda Manager opened successfully")
        except Exception as e:
            self.log(f"❌ Error opening Agenda Manager: {e}")
            messagebox.showerror(
                "❌ Error", 
                f"Cannot open Agenda Manager:\n\n{str(e)}",
                parent=self.root
            )
    
    def verificar_actualizaciones(self):
        """Verificar si hay actualizaciones disponibles en GitHub"""
        self.log("🔄 Verificando actualizaciones en GitHub...")
        
        try:
            import subprocess
            
            # Verificar si estamos en un repositorio Git
            git_check = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if git_check.returncode != 0:
                self.log("❌ No se detectó repositorio Git")
                messagebox.showinfo(
                    "Sin Repositorio Git",
                    "Este sistema no está vinculado a un repositorio Git.\n\n"
                    "Para habilitar actualizaciones automáticas, clona el repositorio desde GitHub.",
                    parent=self.root
                )
                return
            
            # Obtener commit local actual
            local_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if local_result.returncode != 0:
                raise Exception("No se pudo obtener commit local")
            
            local_commit = local_result.stdout.strip()
            self.log(f"📌 Commit local: {local_commit[:8]}")
            
            # Obtener información de la rama actual
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "main"
            self.log(f"🌿 Rama actual: {branch}")
            
            # Fetch desde GitHub (sin merge)
            self.log("🔍 Consultando GitHub...")
            fetch_result = subprocess.run(
                ["git", "fetch", "origin", branch],
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if fetch_result.returncode != 0:
                raise Exception(f"Error al consultar GitHub: {fetch_result.stderr}")
            
            # Obtener commit remoto
            remote_result = subprocess.run(
                ["git", "rev-parse", f"origin/{branch}"],
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if remote_result.returncode != 0:
                raise Exception("No se pudo obtener commit remoto")
            
            remote_commit = remote_result.stdout.strip()
            self.log(f"☁️ Commit remoto: {remote_commit[:8]}")
            
            # Comparar commits
            if local_commit == remote_commit:
                self.log("✅ El sistema está actualizado")
                messagebox.showinfo(
                    "✅ Sistema Actualizado",
                    f"Tu sistema está actualizado con la última versión.\n\n"
                    f"Commit actual: {local_commit[:8]}\n"
                    f"Rama: {branch}",
                    parent=self.root
                )
            else:
                # Obtener lista de cambios
                changes_result = subprocess.run(
                    ["git", "log", f"{local_commit}..{remote_commit}", "--oneline", "--no-decorate"],
                    cwd=self.BASE_DIR,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                changes = changes_result.stdout.strip() if changes_result.returncode == 0 else "No disponible"
                num_commits = len(changes.split('\n')) if changes else 0
                
                self.log(f"📥 Hay {num_commits} actualizaciones disponibles")
                self.log("Cambios disponibles:")
                for line in changes.split('\n')[:10]:  # Mostrar máximo 10 commits
                    if line.strip():
                        self.log(f"  • {line}")
                
                # Preguntar si desea actualizar
                response = messagebox.askyesno(
                    "🔄 Actualizaciones Disponibles",
                    f"Hay {num_commits} actualizaciones disponibles en GitHub.\n\n"
                    f"Cambios recientes:\n{chr(10).join(['• ' + l for l in changes.split(chr(10))[:5]])}\n\n"
                    f"¿Deseas actualizar ahora?\n\n"
                    f"NOTA: Esto sobrescribirá cualquier cambio local no guardado.",
                    parent=self.root
                )
                
                if response:
                    self.aplicar_actualizacion(branch)
                else:
                    self.log("ℹ️ Actualización cancelada por el usuario")
        
        except subprocess.TimeoutExpired:
            self.log("⏱️ Timeout al consultar GitHub")
            messagebox.showerror(
                "Timeout",
                "La consulta a GitHub tardó demasiado.\n\nVerifica tu conexión a Internet.",
                parent=self.root
            )
        except FileNotFoundError:
            self.log("❌ Git no está instalado")
            messagebox.showerror(
                "Git No Encontrado",
                "Git no está instalado en tu sistema.\n\n"
                "Descarga Git desde: https://git-scm.com/downloads",
                parent=self.root
            )
        except Exception as e:
            self.log(f"❌ Error al verificar actualizaciones: {e}")
            messagebox.showerror(
                "Error",
                f"Error al verificar actualizaciones:\n\n{str(e)}",
                parent=self.root
            )
    
    def aplicar_actualizacion(self, branch="main"):
        """Aplicar actualizaciones desde GitHub"""
        self.log("📥 Aplicando actualizaciones...")
        
        try:
            import subprocess
            
            # Pull desde GitHub
            pull_result = subprocess.run(
                ["git", "pull", "origin", branch, "--rebase"],
                cwd=self.BASE_DIR,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if pull_result.returncode != 0:
                error_msg = pull_result.stderr if pull_result.stderr else pull_result.stdout
                raise Exception(f"Error al actualizar: {error_msg}")
            
            self.log("✅ Actualizaciones aplicadas correctamente")
            self.log(pull_result.stdout)
            
            messagebox.showinfo(
                "✅ Actualización Completada",
                "El sistema se ha actualizado correctamente.\n\n"
                "Se recomienda reiniciar la aplicación para aplicar todos los cambios.",
                parent=self.root
            )
            
        except subprocess.TimeoutExpired:
            self.log("⏱️ Timeout al aplicar actualizaciones")
            messagebox.showerror(
                "Timeout",
                "La actualización tardó demasiado.\n\nIntenta nuevamente.",
                parent=self.root
            )
        except Exception as e:
            self.log(f"❌ Error al aplicar actualizaciones: {e}")
            messagebox.showerror(
                "Error",
                f"Error al aplicar actualizaciones:\n\n{str(e)}\n\n"
                "Puedes intentar actualizar manualmente con:\n"
                "git pull origin main",
                parent=self.root
            )
            
    def ejecutar_procesamiento(self):
        """Ejecutar el procesamiento completo con logging mejorado"""
        self.btn_procesar.configure(state="disabled", text="🔄 PROCESANDO...")
        self.status_bar.configure(text="🔄 Procesando pedidos, por favor espere...")
        
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
                self.status_bar.configure(text="⚠️ No data to process")
                return
                
            # Paso 2: Validar SKUs
            self.siguiente_paso()
            self.log("🔍 Paso 2: Validando Items C.Calzada...")
            from products_manager import ProductsManager
            products_manager = ProductsManager()
            df_items_valid, df_err_items, warnings_items = validar_skus_items(df_pdfs, products_manager)
            
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
            self.status_bar.configure(
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
            self.status_bar.configure(text="❌ Error en procesamiento")
            messagebox.showerror(
                "❌ Error Crítico", 
                f"Error durante el procesamiento:\n\n{str(e)}\n\nRevise el registro de actividad para más detalles."
            )
            
        finally:
            self.btn_procesar.configure(state="normal", text="🚀 PROCESAR PEDIDOS")
            
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

