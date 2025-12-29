"""
Editor de Proveedor - Tkinter Puro
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def crear_editor_proveedor_mejorado(dialog, manager, colors, codigo_editar=None, callback_actualizar=None):
    """Editor de proveedor con Tkinter puro - tema moderno"""
    
    # Datos del proveedor si estamos editando
    proveedor_data = None
    if codigo_editar:
        proveedor_data = manager.obtener_proveedor(codigo_editar)
    
    # Ventana principal
    editor = tk.Toplevel(dialog)
    editor.title("✏️ Editar Proveedor" if codigo_editar else "➕ Nuevo Proveedor")
    
    # Hacer la ventana responsive a la pantalla
    screen_height = editor.winfo_screenheight()
    window_height = int(screen_height * 0.9)  # 90% de la altura de pantalla
    window_width = 700
    
    # Centrar ventana
    x_position = int((editor.winfo_screenwidth() - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)
    
    editor.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    editor.configure(bg=colors['bg_main'])
    editor.resizable(True, True)
    editor.grab_set()
    
    # Header
    header = tk.Frame(editor, bg=colors['bg_card'], height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    
    tk.Label(
        header,
        text="📝 DATOS DEL PROVEEDOR" if not codigo_editar else "✏️ EDITAR PROVEEDOR",
        font=("Segoe UI", 18, "bold"),
        bg=colors['bg_card'],
        fg=colors['accent']
    ).pack(expand=True)
    
    # Frame principal con scroll
    main_frame = tk.Frame(editor, bg=colors['bg_main'])
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Variables
    codigo_var = tk.StringVar(value=codigo_editar if codigo_editar else '')
    nombre_var = tk.StringVar(value=proveedor_data['nombre'] if proveedor_data else '')
    
    # Frame para código
    codigo_frame = tk.LabelFrame(
        main_frame,
        text=" 🏷️ Código del Proveedor ",
        bg=colors['bg_card'],
        fg=colors['fg_text'],
        font=("Segoe UI", 12, "bold"),
        relief='flat',
        bd=2
    )
    codigo_frame.pack(fill='x', pady=10)
    
    codigo_entry = tk.Entry(
        codigo_frame,
        textvariable=codigo_var,
        font=("Segoe UI", 13),
        bg=colors['bg_surface'],
        fg=colors['fg_text'],
        insertbackground=colors['fg_text'],
        relief='flat',
        bd=5
    )
    codigo_entry.pack(fill='x', padx=15, pady=15)
    
    if codigo_editar:
        codigo_entry.configure(state='readonly')
    
    # Frame para nombre
    nombre_frame = tk.LabelFrame(
        main_frame,
        text=" 📝 Nombre del Proveedor ",
        bg=colors['bg_card'],
        fg=colors['fg_text'],
        font=("Segoe UI", 12, "bold"),
        relief='flat',
        bd=2
    )
    nombre_frame.pack(fill='x', pady=10)
    
    nombre_entry = tk.Entry(
        nombre_frame,
        textvariable=nombre_var,
        font=("Segoe UI", 13),
        bg=colors['bg_surface'],
        fg=colors['fg_text'],
        insertbackground=colors['fg_text'],
        relief='flat',
        bd=5
    )
    nombre_entry.pack(fill='x', padx=15, pady=15)
    
    # === SECCIÓN: DÍAS DE ENTREGA ===
    dias_frame = tk.LabelFrame(
        main_frame,
        text=" 📅 Días de Entrega de la Semana ",
        bg=colors['bg_card'],
        fg=colors['fg_text'],
        font=("Segoe UI", 12, "bold"),
        relief='flat',
        bd=2
    )
    dias_frame.pack(fill='x', pady=10)
    
    # Variables para días
    dias_vars = {}
    dias_labels = ['LUN', 'MAR', 'MIE', 'JUE', 'VIE', 'SAB']
    
    # Container para checkboxes de días
    dias_container = tk.Frame(dias_frame, bg=colors['bg_card'])
    dias_container.pack(fill='x', padx=15, pady=15)
    
    for i, dia in enumerate(dias_labels):
        dias_vars[dia] = tk.BooleanVar()
        
        # Cargar estado existente si estamos editando
        if proveedor_data:
            valor_actual = proveedor_data.get(dia)
            # Convertir a booleano: 1, True, '1' -> True, None/0/False -> False
            dias_vars[dia].set(valor_actual == 1 or valor_actual == '1')
            
        checkbox = tk.Checkbutton(
            dias_container,
            text=f"  {dia}  ",
            variable=dias_vars[dia],
            font=("Segoe UI", 12, "bold"),
            bg=colors['bg_card'],
            fg=colors['fg_text'],
            selectcolor='#000000',  # Fondo negro cuando está marcado
            activebackground=colors['bg_surface'],
            activeforeground=colors['fg_text'],
            relief='raised',
            bd=2,
            indicatoron=True,
            offvalue=False,
            onvalue=True,
            cursor='hand2',
            highlightthickness=0
        )
        checkbox.grid(row=i//3, column=i%3, padx=20, pady=8, sticky='w')
    
    # D-2 (Domingo)
    d2_var = tk.BooleanVar()
    if proveedor_data:
        valor_d2 = proveedor_data.get('D-2')
        d2_var.set(valor_d2 == 1 or valor_d2 == '1')
    
    d2_checkbox = tk.Checkbutton(
        dias_container,
        text="  D-2  ",
        variable=d2_var,
        font=("Segoe UI", 12, "bold"),
        bg=colors['bg_card'],
        fg=colors['warning'],  # Color diferente para destacar
        selectcolor='#000000',  # Fondo negro cuando está marcado
        activebackground=colors['bg_surface'],
        activeforeground=colors['warning'],
        relief='raised',
        bd=2,
        indicatoron=True,
        offvalue=False,
        onvalue=True,
        cursor='hand2',
        highlightthickness=0
    )
    d2_checkbox.grid(row=2, column=0, padx=20, pady=8, sticky='w')
    
    # Explicación de D-2
    tk.Label(
        dias_frame,
        text="D-2: Entrega en 2 días hábiles (generalmente domingos)",
        font=("Segoe UI", 9, "italic"),
        bg=colors['bg_card'],
        fg=colors['fg_secondary']
    ).pack(anchor='w', padx=15, pady=(0, 10))
    
    # === SECCIÓN: FECHA MANUAL (OPCIONAL) ===
    fecha_info_frame = tk.LabelFrame(
        main_frame,
        text=" 📅 Fecha de Entrega Manual ",
        bg=colors['bg_card'],
        fg=colors['fg_text'],
        font=("Segoe UI", 12, "bold"),
        relief='flat',
        bd=2
    )
    fecha_info_frame.pack(fill='x', pady=10)
    
    tk.Label(
        fecha_info_frame,
        text="Si configuras una fecha manual, esta NO se calculará automáticamente.",
        bg=colors['bg_card'],
        fg=colors['fg_secondary'],
        font=("Segoe UI", 10, "italic")
    ).pack(anchor='w', padx=15, pady=(10, 5))
    
    tk.Label(
        fecha_info_frame,
        text="Deja vacío para calcular automáticamente según los días configurados arriba.",
        bg=colors['bg_card'],
        fg=colors['fg_secondary'],
        font=("Segoe UI", 10, "italic")
    ).pack(anchor='w', padx=15, pady=(0, 10))
    
    # Variables para fecha manual
    fecha_manual_var = tk.StringVar(value=proveedor_data.get('fecha_manual', '') if proveedor_data else '')
    
    # Campo de fecha manual
    fecha_frame = tk.Frame(fecha_info_frame, bg=colors['bg_card'])
    fecha_frame.pack(fill='x', padx=15, pady=(0, 15))
    
    tk.Label(
        fecha_frame,
        text="Fecha Manual:",
        font=("Segoe UI", 11, "bold"),
        bg=colors['bg_card'],
        fg=colors['fg_text']
    ).pack(side='left', padx=(0, 10))
    
    fecha_manual_entry = tk.Entry(
        fecha_frame,
        textvariable=fecha_manual_var,
        font=("Segoe UI", 11),
        bg=colors['bg_surface'],
        fg=colors['fg_text'],
        insertbackground=colors['fg_text'],
        relief='flat',
        bd=5,
        width=15
    )
    fecha_manual_entry.pack(side='left', padx=(0, 10))
    
    tk.Label(
        fecha_frame,
        text="(dd-mm-yyyy o dejar vacío)",
        font=("Segoe UI", 10),
        bg=colors['bg_card'],
        fg=colors['fg_secondary']
    ).pack(side='left')
    
    # === NOTA INFORMATIVA ===
    info_frame = tk.Frame(main_frame, bg=colors['info'], relief='solid', bd=1)
    info_frame.pack(fill='x', pady=20)
    
    tk.Label(
        info_frame,
        text="ℹ️ Configuración Completa",
        bg=colors['info'],
        fg='white',
        font=("Segoe UI", 11, "bold")
    ).pack(anchor='w', padx=15, pady=(10, 5))
    
    tk.Label(
        info_frame,
        text="Aquí puedes configurar todos los aspectos del proveedor: días de entrega y fecha manual.",
        bg=colors['info'],
        fg='white',
        font=("Segoe UI", 10),
        wraplength=520,
        justify='left'
    ).pack(anchor='w', padx=15, pady=(0, 5))
    
    tk.Label(
        info_frame,
        text="Los cambios también se reflejarán en la tabla principal automáticamente.",
        bg=colors['info'],
        fg='white',
        font=("Segoe UI", 10),
        wraplength=520,
        justify='left'
    ).pack(anchor='w', padx=15, pady=(0, 10))
    
    def guardar_proveedor():
        """Guarda el proveedor"""
        codigo = codigo_var.get().strip().upper()
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

        # Recopilar días seleccionados
        dias_entrega = {}
        for dia in dias_labels:
            # Solo asignar 1 si está marcado, None si no está marcado
            dias_entrega[dia] = 1 if dias_vars[dia].get() else None
        
        # D-2 por separado
        d2 = 1 if d2_var.get() else None

        # Guardar usando la función agregar_proveedor
        try:
            manager.agregar_proveedor(codigo, nombre, dias_entrega, d2, fecha_manual)
            
            if callback_actualizar:
                callback_actualizar()
            
            messagebox.showinfo("✅ Guardado", f"Proveedor {codigo} guardado correctamente", parent=editor)
            editor.destroy()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al guardar: {str(e)}", parent=editor)
    
    # Botones
    botones_frame = tk.Frame(main_frame, bg=colors['bg_main'])
    botones_frame.pack(fill='x', pady=20)
    
    # Botón Guardar
    tk.Button(
        botones_frame,
        text="💾 Guardar",
        command=guardar_proveedor,
        font=("Segoe UI", 14, "bold"),
        bg=colors['success'],
        fg='white',
        relief='flat',
        cursor='hand2',
        padx=30,
        pady=12
    ).pack(side='left', padx=(0, 10), fill='x', expand=True)
    
    # Botón Cancelar
    tk.Button(
        botones_frame,
        text="❌ Cancelar",
        command=editor.destroy,
        font=("Segoe UI", 14, "bold"),
        bg=colors['error'],
        fg='white',
        relief='flat',
        cursor='hand2',
        padx=30,
        pady=12
    ).pack(side='right', padx=(10, 0), fill='x', expand=True)
    
    # Centrar ventana
    editor.transient(dialog)
    editor.focus_set()
    
    # Enfocar el campo apropiado
    if codigo_editar:
        nombre_entry.focus_set()
        nombre_entry.select_range(0, tk.END)
    else:
        codigo_entry.focus_set()