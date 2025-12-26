"""
Editor de Proveedor Mejorado - Versión Simplificada
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime


def crear_editor_proveedor_mejorado(dialog, manager, colors, codigo_editar=None, callback_actualizar=None):
    """
    Crea un editor de proveedor más claro y fácil de usar
    
    Args:
        dialog: Ventana padre
        manager: AgendaManager
        colors: Diccionario de colores
        codigo_editar: Código del proveedor a editar (None para nuevo)
        callback_actualizar: Función a llamar después de guardar
    """
    
    # Datos del proveedor si estamos editando
    proveedor_data = None
    if codigo_editar:
        proveedor_data = manager.obtener_proveedor(codigo_editar)
    
    # Ventana principal
    editor = tk.Toplevel(dialog)
    editor.title("✏️ Editar Proveedor" if codigo_editar else "➕ Nuevo Proveedor")
    
    # Adaptar altura a la pantalla del usuario (ventana más pequeña)
    screen_height = editor.winfo_screenheight()
    window_height = min(550, int(screen_height * 0.6))  # Máximo 550 o 60% de pantalla
    window_width = 600
    
    # Centrar ventana
    x_position = int((editor.winfo_screenwidth() - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)
    
    editor.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    editor.configure(bg=colors['bg_main'])
    editor.resizable(True, True)
    editor.grab_set()
    
    # Frame principal con scroll
    canvas = tk.Canvas(editor, bg=colors['bg_card'], highlightthickness=0)
    scrollbar = tk.Scrollbar(editor, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=colors['bg_card'])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar.pack(side="right", fill="y")
    
    # === SECCIÓN 1: DATOS BÁSICOS ===
    tk.Label(
        scrollable_frame,
        text="📝 DATOS DEL PROVEEDOR",
        bg=colors['bg_card'],
        fg=colors['accent'],
        font=('Segoe UI', 12, 'bold')
    ).pack(anchor='w', pady=(10, 15), padx=10)
    
    # Código
    codigo_frame = tk.Frame(scrollable_frame, bg=colors['bg_card'])
    codigo_frame.pack(fill='x', padx=10, pady=5)
    tk.Label(codigo_frame, text="Código:", bg=colors['bg_card'], fg=colors['fg_text'], font=('Segoe UI', 10, 'bold'), width=15, anchor='w').pack(side='left')
    codigo_var = tk.StringVar(value=codigo_editar if codigo_editar else '')
    codigo_entry = tk.Entry(codigo_frame, textvariable=codigo_var, font=('Segoe UI', 10), width=30, relief='solid', bd=1, bg='#FAFAFA')
    codigo_entry.pack(side='left', padx=5)
    if codigo_editar:
        codigo_entry.config(state='readonly', bg='#e0e0e0')
    
    # Nombre
    nombre_frame = tk.Frame(scrollable_frame, bg=colors['bg_card'])
    nombre_frame.pack(fill='x', padx=10, pady=5)
    tk.Label(nombre_frame, text="Nombre:", bg=colors['bg_card'], fg=colors['fg_text'], font=('Segoe UI', 10, 'bold'), width=15, anchor='w').pack(side='left')
    nombre_var = tk.StringVar(value=proveedor_data['nombre'] if proveedor_data else '')
    nombre_entry = tk.Entry(nombre_frame, textvariable=nombre_var, font=('Segoe UI', 10), width=30, relief='solid', bd=1, bg='#FAFAFA')
    nombre_entry.pack(side='left', padx=5)
    
    # === SECCIÓN 2: FECHA MANUAL (OPCIONAL) ===
    tk.Label(
        scrollable_frame,
        text="📅 FECHA DE ENTREGA MANUAL",
        bg=colors['bg_card'],
        fg=colors['accent'],
        font=('Segoe UI', 12, 'bold')
    ).pack(anchor='w', pady=(20, 10), padx=10)
    
    tk.Label(
        scrollable_frame,
        text="Si configuras una fecha manual, esta NO se calculará automáticamente.",
        bg=colors['bg_card'],
        fg='#666666',
        font=('Segoe UI', 9, 'italic')
    ).pack(anchor='w', padx=10, pady=(0, 10))
    
    tk.Label(
        scrollable_frame,
        text="Deja vacío para calcular automáticamente según los días configurados en la tabla.",
        bg=colors['bg_card'],
        fg='#666666',
        font=('Segoe UI', 9, 'italic')
    ).pack(anchor='w', padx=10, pady=(0, 10))
    
    # Campo de fecha manual
    fecha_manual_frame = tk.Frame(scrollable_frame, bg=colors['bg_card'])
    fecha_manual_frame.pack(fill='x', padx=10, pady=5)
    tk.Label(fecha_manual_frame, text="Fecha Manual:", bg=colors['bg_card'], fg=colors['fg_text'], font=('Segoe UI', 10, 'bold'), width=15, anchor='w').pack(side='left')
    fecha_manual_var = tk.StringVar(value=proveedor_data.get('fecha_manual', '') if proveedor_data else '')
    fecha_manual_entry = tk.Entry(fecha_manual_frame, textvariable=fecha_manual_var, font=('Segoe UI', 10), width=20, relief='solid', bd=1, bg='#FAFAFA')
    fecha_manual_entry.pack(side='left', padx=5)
    tk.Label(fecha_manual_frame, text="(dd-mm-yyyy o dejar vacío)", bg=colors['bg_card'], fg='gray', font=('Segoe UI', 9)).pack(side='left')
    
    # === NOTA INFORMATIVA ===
    info_frame = tk.Frame(scrollable_frame, bg='#E3F2FD', relief='solid', bd=1)
    info_frame.pack(fill='x', padx=10, pady=20)
    
    tk.Label(
        info_frame,
        text="ℹ️ Configuración de Días de Entrega",
        bg='#E3F2FD',
        fg='#1976D2',
        font=('Segoe UI', 10, 'bold')
    ).pack(anchor='w', padx=10, pady=(10, 5))
    
    tk.Label(
        info_frame,
        text="Los días de entrega (LUN-SAB, D-2) se configuran directamente en la tabla principal.",
        bg='#E3F2FD',
        fg='#424242',
        font=('Segoe UI', 9),
        wraplength=520,
        justify='left'
    ).pack(anchor='w', padx=10, pady=(0, 5))
    
    tk.Label(
        info_frame,
        text="Haz clic en las columnas de días en la tabla para cambiar los valores.",
        bg='#E3F2FD',
        fg='#424242',
        font=('Segoe UI', 9),
        wraplength=520,
        justify='left'
    ).pack(anchor='w', padx=10, pady=(0, 10))
    
    # === BOTONES ===
    botones_frame = tk.Frame(scrollable_frame, bg=colors['bg_card'])
    botones_frame.pack(pady=20)
    
    def guardar():
        codigo = codigo_var.get().strip()
        nombre = nombre_var.get().strip()
        fecha_manual = fecha_manual_var.get().strip() if fecha_manual_var.get().strip() else None
        
        if not codigo:
            messagebox.showerror("Error", "Ingrese el código del proveedor", parent=editor)
            return
        if not nombre:
            messagebox.showerror("Error", "Ingrese el nombre del proveedor", parent=editor)
            return
        
        # Validar fecha manual si se ingresó
        if fecha_manual:
            try:
                datetime.strptime(fecha_manual, "%d-%m-%Y")
            except:
                messagebox.showerror("Error", "Formato de fecha inválido. Use dd-mm-yyyy", parent=editor)
                return
        
        # Si estamos editando, preservar los días existentes
        # Si es nuevo, usar valores por defecto (None)
        if proveedor_data:
            dias_entrega = {
                'LUN': proveedor_data.get('LUN'),
                'MAR': proveedor_data.get('MAR'),
                'MIE': proveedor_data.get('MIE'),
                'JUE': proveedor_data.get('JUE'),
                'VIE': proveedor_data.get('VIE'),
                'SAB': proveedor_data.get('SAB')
            }
            d2 = proveedor_data.get('D-2')
        else:
            # Proveedor nuevo: todos los días en None (ignorar)
            dias_entrega = {dia: None for dia in ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB']}
            d2 = None
        
        # Guardar
        manager.agregar_proveedor(codigo, nombre, dias_entrega, d2, fecha_manual)
        
        if callback_actualizar:
            callback_actualizar()
        
        messagebox.showinfo("✅ Guardado", f"Proveedor {codigo} guardado correctamente", parent=editor)
        editor.destroy()
    
    tk.Button(
        botones_frame,
        text="💾 Guardar Proveedor",
        command=guardar,
        bg=colors['success'],
        fg='white',
        font=('Segoe UI', 11, 'bold'),
        relief='flat',
        cursor='hand2',
        padx=30,
        pady=10
    ).pack(side='left', padx=5)
    
    tk.Button(
        botones_frame,
        text="❌ Cancelar",
        command=editor.destroy,
        bg=colors['accent'],
        fg='white',
        font=('Segoe UI', 11, 'bold'),
        relief='flat',
        cursor='hand2',
        padx=30,
        pady=10
    ).pack(side='left', padx=5)
    
    # Binding para scroll con rueda del mouse
    def _on_mousewheel(event):
        try:
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except:
            pass
    
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def on_close():
        canvas.unbind_all("<MouseWheel>")
        editor.destroy()
    
    editor.protocol("WM_DELETE_WINDOW", on_close)
    
    return editor
