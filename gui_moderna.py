"""
DHL Order Processing System - Modern GUI
Created by Lucas Gnemmi
Version: 2.0

Sistema profesional para el procesamiento de órdenes de DHL con interfaz gráfica moderna.
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
from procesamiento import (
    procesar_pdfs,
    validar_skus_items,
    mapear_proveedor_por_sku,
    rellenar_fecha_entrega_y_observacion,
    asignar_id_final,
    formatear_excel_salida,
    obtener_nombre_archivo_salida
)

# Configuración de colores del tema DHL
class DHLTheme:
    """Clase para definir el tema visual de DHL"""
    # Colores principales DHL
    PRIMARY = "#D40511"      # Rojo DHL
    SECONDARY = "#FFCC00"    # Amarillo DHL
    DARK = "#1A1A1A"        # Negro DHL
    LIGHT_GRAY = "#F5F5F5"  # Gris claro
    MEDIUM_GRAY = "#E0E0E0" # Gris medio
    WHITE = "#FFFFFF"       # Blanco
    
    # Colores funcionales
    SUCCESS = "#27AE60"     # Verde éxito
    WARNING = "#F39C12"     # Naranja advertencia
    ERROR = "#E74C3C"       # Rojo error
    INFO = "#3498DB"        # Azul información
    
    # Colores de texto
    TEXT_PRIMARY = "#2C3E50"
    TEXT_SECONDARY = "#7F8C8D"
    TEXT_WHITE = "#FFFFFF"

class ModernGUI:
    """
    Interfaz gráfica moderna para el sistema de procesamiento de órdenes DHL
    Created by Lucas Gnemmi
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.theme = DHLTheme()
        self.setup_main_window()
        self.setup_paths()
        self.setup_widgets()
        self.refrescar_archivos()
        
    def setup_main_window(self):
        """Configuración de la ventana principal con diseño profesional"""
        self.root.title("🚚 DHL Order Processing System - Created by Lucas Gnemmi")
        self.root.geometry("1400x900")
        self.root.configure(bg=self.theme.LIGHT_GRAY)
        self.root.minsize(1200, 800)
        
        # Centrar ventana en pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Configurar estilo TTK moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados
        self._configure_styles()
        
    def _configure_styles(self):
        """Configurar estilos personalizados para widgets TTK"""
        # Estilo para botones principales
        self.style.configure(
            "DHL.TButton",
            background=self.theme.PRIMARY,
            foreground=self.theme.WHITE,
            font=("Arial", 10, "bold"),
            padding=(10, 5)
        )
        
        # Estilo para frames
        self.style.configure(
            "DHL.TLabelFrame",
            background=self.theme.LIGHT_GRAY,
            relief="solid",
            borderwidth=1
        )
        
        # Estilo para labels
        self.style.configure(
            "DHL.TLabel",
            background=self.theme.LIGHT_GRAY,
            foreground=self.theme.TEXT_PRIMARY,
            font=("Arial", 9)
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
        """Crear encabezado con branding DHL"""
        header_frame = tk.Frame(self.root, bg=self.theme.PRIMARY, height=100)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Contenedor del título
        title_container = tk.Frame(header_frame, bg=self.theme.PRIMARY)
        title_container.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Título principal
        title_label = tk.Label(
            title_container, 
            text="🚚 DHL ORDER PROCESSING SYSTEM", 
            font=("Arial", 20, "bold"),
            fg=self.theme.WHITE, 
            bg=self.theme.PRIMARY
        )
        title_label.pack(anchor="w")
        
        # Subtítulo con autoría
        subtitle_label = tk.Label(
            title_container, 
            text="Professional Order Management Solution • Created by Lucas Gnemmi", 
            font=("Arial", 11),
            fg=self.theme.SECONDARY, 
            bg=self.theme.PRIMARY
        )
        subtitle_label.pack(anchor="w", pady=(0, 5))
        
    def _create_main_layout(self):
        """Crear el layout principal de la aplicación"""
        # Contenedor principal con padding mejorado
        main_container = tk.Frame(self.root, bg=self.theme.LIGHT_GRAY)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Panel izquierdo (Controles)
        self._create_left_panel(main_container)
        
        # Panel derecho (Logs y resultados)
        self._create_right_panel(main_container)
        
    def _create_left_panel(self, parent):
        """Crear panel izquierdo con controles"""
        left_panel = tk.LabelFrame(
            parent, 
            text="📁 Control Panel", 
            font=("Arial", 14, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        # Sección de archivos PDF
        self._create_pdf_section(left_panel)
        
        # Sección de pasos de procesamiento
        self._create_processing_section(left_panel)
        
        # Sección de accesos rápidos
        self._create_quick_access_section(left_panel)
        
    def _create_pdf_section(self, parent):
        """Crear sección de gestión de archivos PDF"""
        pdf_section = tk.LabelFrame(
            parent, 
            text="📄 PDF Files Management", 
            font=("Arial", 12, "bold"),
            bg=self.theme.WHITE,
            fg=self.theme.TEXT_PRIMARY,
            relief="groove",
            bd=1
        )
        pdf_section.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Lista de PDFs con diseño mejorado
        list_container = tk.Frame(pdf_section, bg=self.theme.WHITE)
        list_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(
            list_container, 
            text="� Files in Ordenes folder:", 
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
            ("➕ Add PDFs", self.agregar_archivo, self.theme.SUCCESS),
            ("🗑️ Clear All", self.eliminar_archivo, self.theme.ERROR),
            ("🔄 Refresh", self.refrescar_archivos, self.theme.INFO)
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
        
        # Pasos de Procesamiento
        pasos_frame = tk.LabelFrame(
            left_panel, 
            text="� Pasos de Procesamiento", 
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        pasos_frame.pack(fill="x", padx=10, pady=10)
        
        pasos_buttons = tk.Frame(pasos_frame, bg="#f0f0f0")
        pasos_buttons.pack(fill="x", padx=10, pady=10)
        
        # Paso 1: Abrir Full
        paso1_frame = tk.Frame(pasos_buttons, bg="#f0f0f0")
        paso1_frame.pack(fill="x", pady=2)
        tk.Label(paso1_frame, text="1.", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#e74c3c", width=3).pack(side="left")
        self.btn_full = tk.Button(
            paso1_frame, 
            text="📋 Abrir Full.xlsx", 
            command=self.abrir_full_xlsx,
            bg="#9b59b6", 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief="flat",
            pady=3
        )
        self.btn_full.pack(side="left", fill="x", expand=True)
        
        # Paso 2: Abrir Agenda
        paso2_frame = tk.Frame(pasos_buttons, bg="#f0f0f0")
        paso2_frame.pack(fill="x", pady=2)
        tk.Label(paso2_frame, text="2.", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#e74c3c", width=3).pack(side="left")
        self.btn_agenda = tk.Button(
            paso2_frame, 
            text="📅 Abrir Agenda.xlsm", 
            command=self.abrir_agenda_xlsm,
            bg="#e67e22", 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief="flat",
            pady=3
        )
        self.btn_agenda.pack(side="left", fill="x", expand=True)
        
        # Paso 3: Seleccionar Región
        paso3_frame = tk.Frame(pasos_buttons, bg="#f0f0f0")
        paso3_frame.pack(fill="x", pady=5)
        tk.Label(paso3_frame, text="3.", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#e74c3c", width=3).pack(side="left")
        
        region_config_frame = tk.Frame(paso3_frame, bg="#f0f0f0")
        region_config_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(region_config_frame, text="Seleccionar Región:", font=("Arial", 9, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        region_input = tk.Frame(region_config_frame, bg="#f0f0f0")
        region_input.pack(fill="x", pady=2)
        
        self.region_var = tk.StringVar(value="099")
        self.region_entry = tk.Entry(
            region_input,
            textvariable=self.region_var,
            font=("Arial", 10),
            width=8,
            justify="center"
        )
        self.region_entry.pack(side="left")
        
        tk.Label(region_input, text=" (por defecto: 099)", font=("Arial", 8), bg="#f0f0f0", fg="#7f8c8d").pack(side="left", padx=5)
        
        # Paso 4: Procesar
        paso4_frame = tk.Frame(pasos_buttons, bg="#f0f0f0")
        paso4_frame.pack(fill="x", pady=5)
        tk.Label(paso4_frame, text="4.", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#e74c3c", width=3).pack(side="left")
        self.btn_procesar = tk.Button(
            paso4_frame, 
            text="🚀 PROCESAR ÓRDENES", 
            command=self.ejecutar_procesamiento_async,
            bg="#e74c3c", 
            fg="white", 
            font=("Arial", 12, "bold"),
            relief="flat",
            pady=10
        )
        self.btn_procesar.pack(side="left", fill="x", expand=True)
        
        # Sección separada para otros accesos
        otros_frame = tk.LabelFrame(
            left_panel, 
            text="📂 Otros Accesos", 
            font=("Arial", 10, "bold"),
            bg="#f0f0f0"
        )
        otros_frame.pack(fill="x", padx=10, pady=10)
        
        otros_buttons = tk.Frame(otros_frame, bg="#f0f0f0")
        otros_buttons.pack(fill="x", padx=10, pady=10)
        
        self.btn_salidas = tk.Button(
            otros_buttons, 
            text="� Abrir Carpeta Salidas", 
            command=self.abrir_carpeta_salidas,
            bg="#16a085", 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief="flat",
            pady=3
        )
        self.btn_salidas.pack(fill="x", pady=2)
        
        self.btn_items = tk.Button(
            otros_buttons, 
            text="� Abrir Items C.Calzada", 
            command=self.abrir_items_xlsx,
            bg="#f39c12", 
            fg="white", 
            font=("Arial", 9, "bold"),
            relief="flat",
            pady=3
        )
        self.btn_items.pack(fill="x", pady=2)
        
        # Panel derecho (Logs y resultados)
        right_panel = tk.Frame(main_container, bg="#f0f0f0")
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Log de actividades
        log_frame = tk.LabelFrame(
            right_panel, 
            text="📜 Log de Actividades", 
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            relief="ridge",
            bd=2
        )
        log_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        self.txt_log = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            state="disabled", 
            font=("Consolas", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            wrap=tk.WORD
        )
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Vista previa de resultados
        preview_frame = tk.LabelFrame(
            right_panel, 
            text="📊 Vista Previa de Resultados", 
            font=("Arial", 12, "bold"),
            bg="#f0f0f0",
            relief="ridge",
            bd=2
        )
        preview_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        self.txt_salida = scrolledtext.ScrolledText(
            preview_frame, 
            height=15, 
            state="disabled", 
            font=("Consolas", 8),
            bg="white",
            wrap=tk.NONE
        )
        self.txt_salida.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de estado
        self.status_bar = tk.Label(
            self.root, 
            text="✅ Sistema listo para procesar", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#34495e",
            fg="white",
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def log(self, msg, color="#ecf0f1"):
        """Añadir mensaje al log con color"""
        self.txt_log.configure(state="normal")
        self.txt_log.insert(tk.END, f"{msg}\n")
        self.txt_log.see(tk.END)
        self.txt_log.configure(state="disabled")
        self.root.update_idletasks()
        
    def mostrar_salida(self, df):
        """Mostrar vista previa de la salida"""
        self.txt_salida.configure(state="normal")
        self.txt_salida.delete("1.0", tk.END)
        if df.empty:
            self.txt_salida.insert(tk.END, "📭 No hay registros en la salida.")
        else:
            # Mostrar columnas principales en el orden correcto
            cols_principales = ['ID PEDIDO', 'LOCAL', 'PROVEEDOR', 'FECHA_ENTREGA', 'SKU', 'CANTIDAD', 'OBSERVACION']
            cols_disponibles = [col for col in cols_principales if col in df.columns]
            
            if cols_disponibles:
                df_preview = df[cols_disponibles]
                self.txt_salida.insert(tk.END, f"📊 Total de registros: {len(df)}\n\n")
                self.txt_salida.insert(tk.END, df_preview.head(20).to_string(index=False))
                if len(df) > 20:
                    self.txt_salida.insert(tk.END, f"\n\n... y {len(df)-20} filas más ...")
            else:
                self.txt_salida.insert(tk.END, df.head(20).to_string(index=False))
        self.txt_salida.configure(state="disabled")
        
    def refrescar_archivos(self):
        """Refrescar lista de archivos PDF"""
        self.listbox_archivos.delete(0, tk.END)
        os.makedirs(self.ORDENES_DIR, exist_ok=True)
        
        pdfs = [f for f in sorted(os.listdir(self.ORDENES_DIR)) if f.lower().endswith(".pdf")]
        
        for pdf in pdfs:
            self.listbox_archivos.insert(tk.END, pdf)
            
        # Actualizar barra de estado
        self.status_bar.config(text=f"📄 {len(pdfs)} archivos PDF encontrados")
        self.log(f"🔄 Lista actualizada: {len(pdfs)} archivos PDF")
        
    def eliminar_archivo(self):
        """Eliminar todos los archivos PDF"""
        pdfs = [f for f in os.listdir(self.ORDENES_DIR) if f.lower().endswith(".pdf")]
        if not pdfs:
            messagebox.showinfo("ℹ️ Información", "No hay archivos PDF para eliminar")
            return
            
        if messagebox.askyesno("🗑️ Confirmar Eliminación", 
                              f"¿Eliminar todos los PDFs ({len(pdfs)} archivos)?\n\nEsta acción no se puede deshacer."):
            try:
                for pdf in pdfs:
                    os.remove(os.path.join(self.ORDENES_DIR, pdf))
                self.log(f"🗑️ Eliminados {len(pdfs)} archivos PDF", "#e74c3c")
                self.refrescar_archivos()
                messagebox.showinfo("✅ Éxito", f"Se eliminaron {len(pdfs)} archivos PDF correctamente")
            except Exception as e:
                self.log(f"❌ Error eliminando archivos: {e}", "#e74c3c")
                messagebox.showerror("❌ Error", f"Error al eliminar archivos: {e}")
                
    def agregar_archivo(self):
        """Agregar archivos PDF"""
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        
        if archivos:
            try:
                copiados = 0
                for archivo in archivos:
                    nombre = os.path.basename(archivo)
                    destino = os.path.join(self.ORDENES_DIR, nombre)
                    shutil.copy2(archivo, destino)
                    self.log(f"📄 Copiado: {nombre}", "#27ae60")
                    copiados += 1
                    
                self.refrescar_archivos()
                messagebox.showinfo("✅ Éxito", f"Se agregaron {copiados} archivos PDF correctamente")
                
            except Exception as e:
                self.log(f"❌ Error copiando archivos: {e}", "#e74c3c")
                messagebox.showerror("❌ Error", f"Error al copiar archivos: {e}")
                
    def abrir_full_xlsx(self):
        """Abrir archivo Full.xlsx"""
        if os.path.exists(self.FULL_XLSX):
            try:
                os.startfile(self.FULL_XLSX)
                self.log("📋 Abriendo Full.xlsx", "#9b59b6")
            except Exception as e:
                self.log(f"❌ Error abriendo Full.xlsx: {e}", "#e74c3c")
        else:
            messagebox.showwarning("⚠️ Archivo no encontrado", "El archivo Full.xlsx no existe")
            
    def abrir_agenda_xlsm(self):
        """Abrir archivo Agenda.xlsm"""
        if os.path.exists(self.AGENDA_XLSM):
            try:
                os.startfile(self.AGENDA_XLSM)
                self.log("📅 Abriendo Agenda.xlsm", "#e67e22")
            except Exception as e:
                self.log(f"❌ Error abriendo Agenda.xlsm: {e}", "#e74c3c")
        else:
            messagebox.showwarning("⚠️ Archivo no encontrado", "El archivo Agenda.xlsm no existe")
            
    def abrir_salida_xlsx(self):
        """Abrir archivo de salida"""
        archivo_salida = self.get_nombre_archivo_salida()
        if os.path.exists(archivo_salida):
            try:
                os.startfile(archivo_salida)
                nombre_archivo = os.path.basename(archivo_salida)
                self.log(f"📤 Abriendo {nombre_archivo}", "#16a085")
            except Exception as e:
                self.log(f"❌ Error abriendo archivo de salida: {e}", "#e74c3c")
        else:
            messagebox.showwarning("⚠️ Archivo no encontrado", "El archivo de salida no existe. Ejecute el procesamiento primero.")
            
    def abrir_carpeta_salidas(self):
        """Abrir carpeta Salidas donde se guardan los archivos procesados"""
        try:
            salidas_dir = os.path.join(self.BASE_DIR, "Salidas")
            if not os.path.exists(salidas_dir):
                os.makedirs(salidas_dir, exist_ok=True)
            os.startfile(salidas_dir)
            self.log("� Abriendo carpeta Salidas", "#16a085")
        except Exception as e:
            self.log(f"❌ Error abriendo carpeta Salidas: {e}", "#e74c3c")
            
    def abrir_items_xlsx(self):
        """Abrir archivo Items C.Calzada"""
        if os.path.exists(self.ITEMS_XLSX):
            try:
                os.startfile(self.ITEMS_XLSX)
                self.log("📋 Abriendo Items C.Calzada", "#f39c12")
            except Exception as e:
                self.log(f"❌ Error abriendo Items.xlsx: {e}", "#e74c3c")
        else:
            messagebox.showwarning("⚠️ Archivo no encontrado", "El archivo Items.xlsx no existe en Full-Agenda")
            
    def ejecutar_procesamiento(self):
        """Ejecutar el procesamiento completo"""
        self.btn_procesar.config(state="disabled", text="🔄 PROCESANDO...")
        self.status_bar.config(text="🔄 Procesando órdenes...")
        
        try:
            self.log("=" * 60, "#3498db")
            self.log("🚀 INICIANDO PROCESAMIENTO DE ÓRDENES", "#3498db")
            self.log("=" * 60, "#3498db")
            
            # Paso 1: Leer PDFs
            self.log("📖 Paso 1: Leyendo archivos PDF...", "#f39c12")
            df_pdfs = procesar_pdfs(self.ORDENES_DIR)
            self.log(f"✅ Procesados {len(df_pdfs)} registros desde {len([f for f in os.listdir(self.ORDENES_DIR) if f.endswith('.pdf')])} archivos PDF", "#27ae60")
            
            if df_pdfs.empty:
                self.log("⚠️ No se encontraron registros en los PDFs.", "#f39c12")
                self.status_bar.config(text="⚠️ No hay datos para procesar")
                return
                
            # Paso 2: Validar Items de compra calzada
            self.log("🔍 Paso 2: Validando Items de compra calzada...", "#f39c12")
            df_items_valid, df_err_items, warnings_items = validar_skus_items(df_pdfs, self.ITEMS_XLSX)
            
            for warning in warnings_items:
                self.log(warning, "#e67e22")
                
            self.log(f"✅ Registros válidos en items: {len(df_items_valid)}", "#27ae60")
            if len(df_err_items) > 0:
                self.log(f"⚠️ Registros no encontrados en items: {len(df_err_items)}", "#e67e22")
                
            # Paso 3: Mapear proveedores
            self.log("🔍 Paso 3: Mapeando proveedores desde Full.xlsx...", "#f39c12")
            region_seleccionada = self.region_var.get().strip() or "099"
            self.log(f"📍 Usando región: {region_seleccionada}", "#3498db")
            df_map, df_err_prov, warnings = mapear_proveedor_por_sku(df_items_valid, self.FULL_XLSX, region_seleccionada)
            
            for warning in warnings:
                self.log(warning, "#e67e22")
                
            self.log(f"✅ Registros válidos con proveedor: {len(df_map)}", "#27ae60")
            if len(df_err_prov) > 0:
                self.log(f"⚠️ Registros con error de precio: {len(df_err_prov)}", "#e67e22")
                
            # Paso 4: Fechas y observaciones
            self.log("📅 Paso 4: Procesando fechas y observaciones desde Agenda.xlsm...", "#f39c12")
            df_final_valid, df_err_fecha = rellenar_fecha_entrega_y_observacion(df_map, self.AGENDA_XLSM)
            
            self.log(f"✅ Registros con fecha asignada: {len(df_final_valid)}", "#27ae60")
            if len(df_err_fecha) > 0:
                self.log(f"⚠️ Registros con error de agenda: {len(df_err_fecha)}", "#e67e22")
                
            # Combinar todos los errores
            df_errores = pd.concat([df_err_items, df_err_prov, df_err_fecha], ignore_index=True)
            
            # Paso 5: Asignar IDs y guardar
            self.log("🏷️ Paso 5: Asignando IDs finales...", "#f39c12")
            df_final = asignar_id_final(df_final_valid)
            
            self.log("💾 Paso 6: Guardando resultados en Excel...", "#f39c12")
            # Obtener nombre dinámico del archivo
            archivo_salida = self.get_nombre_archivo_salida()
            nombre_archivo = os.path.basename(archivo_salida)
            
            with pd.ExcelWriter(archivo_salida, engine="openpyxl") as writer:
                df_final.to_excel(writer, sheet_name="PEDIDOS_CD", index=False)
                if not df_errores.empty:
                    df_errores.to_excel(writer, sheet_name="Errores", index=False)
                    
            self.log(f"✅ Archivo guardado: {nombre_archivo}", "#27ae60")
            
            # Formatear el archivo Excel
            self.log("🎨 Paso 7: Aplicando formato profesional...", "#f39c12")
            formatear_excel_salida(archivo_salida)
            
            # Mostrar resumen
            self.log("=" * 60, "#27ae60")
            self.log("📊 RESUMEN DE PROCESAMIENTO:", "#27ae60")
            self.log(f"   • Total registros procesados: {len(df_final)}", "#27ae60")
            self.log(f"   • Total errores: {len(df_errores)}", "#e67e22")
            self.log(f"   • Archivo de salida: {nombre_archivo}", "#27ae60")
            self.log("🎉 PROCESAMIENTO COMPLETADO EXITOSAMENTE", "#27ae60")
            self.log("=" * 60, "#27ae60")
            
            # Mostrar vista previa
            self.mostrar_salida(df_final)
            
            # Actualizar barra de estado
            self.status_bar.config(text=f"✅ Procesamiento completado: {len(df_final)} registros, {len(df_errores)} errores")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo(
                "🎉 Procesamiento Completado", 
                f"✅ Procesamiento exitoso!\n\n"
                f"📊 Registros procesados: {len(df_final)}\n"
                f"❌ Errores encontrados: {len(df_errores)}\n"
                f"📁 Archivo guardado: {nombre_archivo}\n\n"
                f"¿Desea abrir el archivo de resultados?"
            )
            
            # Preguntar si quiere abrir el archivo
            if messagebox.askyesno("📤 Abrir Resultados", "¿Desea abrir el archivo de salida ahora?"):
                self.abrir_salida_xlsx()
                
        except Exception as e:
            self.log(f"❌ ERROR CRÍTICO: {e}", "#e74c3c")
            self.status_bar.config(text="❌ Error en el procesamiento")
            messagebox.showerror("❌ Error Crítico", f"Error durante el procesamiento:\n\n{str(e)}")
            
        finally:
            self.btn_procesar.config(state="normal", text="🚀 PROCESAR ÓRDENES")
            
    def ejecutar_procesamiento_async(self):
        """Ejecutar procesamiento en hilo separado"""
        threading.Thread(target=self.ejecutar_procesamiento, daemon=True).start()
        
    def run(self):
        """Iniciar la aplicación"""
        self.log("🚀 Sistema de Procesamiento DHL iniciado", "#3498db")
        self.log("📂 Directorio base: " + self.BASE_DIR, "#7f8c8d")
        self.root.mainloop()

def main():
    app = ModernGUI()
    app.run()

if __name__ == "__main__":
    main()