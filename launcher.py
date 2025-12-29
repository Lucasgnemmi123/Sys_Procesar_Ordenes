"""
====================================================================
LAUNCHER PRINCIPAL - Sistema Procesar Pedidos v3.0
====================================================================
Interfaz gráfica para iniciar, actualizar y verificar el sistema
Created by Lucas Gnemmi
====================================================================
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import threading

# Agregar directorio del script al path
script_dir = Path(__file__).parent.resolve()
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

# Agregar carpeta libs al path
libs_path = script_dir / 'libs'
if libs_path.exists() and str(libs_path) not in sys.path:
    sys.path.insert(0, str(libs_path))

class SystemLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Procesamiento de Pedidos v3.0")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Obtener directorio del script
        if getattr(sys, 'frozen', False):
            self.base_dir = Path(sys.executable).parent
        else:
            self.base_dir = Path(__file__).parent.resolve()
        
        # Configurar icono si existe
        icon_path = self.base_dir / "launcher_icon.ico"
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except:
                pass
        
        # Archivo de configuración local
        self.config_file = self.base_dir / "launcher_config.json"
        
        # Colores tema oscuro moderno (igual que gui_moderna_v2.py)
        self.bg_dark = "#1a1d29"          # Azul oscuro profundo
        self.bg_surface = "#242837"       # Superficie elevada
        self.bg_card = "#2d3142"          # Cards
        self.primary = "#00d4ff"          # Cyan brillante
        self.primary_dark = "#00b8d9"     # Cyan oscuro hover
        self.text_primary = "#ffffff"     # Blanco
        self.text_secondary = "#e5e7eb"   # Gris claro
        self.text_muted = "#9ca3af"       # Gris medio
        self.success = "#34d399"          # Verde
        self.warning = "#fbbf24"          # Amarillo
        self.error = "#f87171"            # Rojo
        
        self.root.configure(bg=self.bg_dark)
        
        self.create_widgets()
        self.setup_hover_effects()
        self.check_git_status()
    
    def get_python_executable(self):
        """
        Devuelve el ejecutable de Python interno (python/python.exe) si existe,
        si no, usa el Python del sistema.
        """
        internal_python = self.base_dir / "python" / "python.exe"
        if internal_python.exists():
            return str(internal_python)
        # Si no existe python interno, usar el del sistema
        return sys.executable
    
    def set_python_executable(self, python_path):
        # Ya no se usa configuración personalizada, solo python interno o sistema
        pass
    
    def configure_python(self):
        """
        Mostrar información sobre el Python interno.
        """
        internal_python = self.base_dir / "python" / "python.exe"
        if internal_python.exists():
            messagebox.showinfo(
                "Python interno",
                f"Se detectó Python interno en:\n{internal_python}\n\n"
                "Este Python será usado siempre que esté presente.\n"
                "Para actualizarlo, reemplaza la carpeta 'python'."
            )
        else:
            messagebox.showinfo(
                "Python del sistema",
                f"No se detectó Python interno.\n"
                f"Se usará el Python del sistema: {sys.executable}"
            )
    
    def setup_hover_effects(self):
        """Configurar efectos hover para los botones"""
        # Hover para botón INICIAR
        def on_enter_start(e):
            self.btn_start.config(bg=self.primary_dark)
        
        def on_leave_start(e):
            self.btn_start.config(bg=self.primary)
        
        self.btn_start.bind("<Enter>", on_enter_start)
        self.btn_start.bind("<Leave>", on_leave_start)
        
        # Hover para botón ACTUALIZAR
        def on_enter_update(e):
            self.btn_update.config(bg=self.bg_surface)
        
        def on_leave_update(e):
            self.btn_update.config(bg=self.bg_card)
        
        self.btn_update.bind("<Enter>", on_enter_update)
        self.btn_update.bind("<Leave>", on_leave_update)
        
        # Hover para botón VERIFICAR
        def on_enter_check(e):
            self.btn_check.config(bg=self.bg_surface)
        
        def on_leave_check(e):
            self.btn_check.config(bg=self.bg_card)
        
        self.btn_check.bind("<Enter>", on_enter_check)
        self.btn_check.bind("<Leave>", on_leave_check)
    
    def create_widgets(self):
        # Frame superior con título
        header_frame = tk.Frame(self.root, bg=self.bg_surface, height=120)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="SISTEMA PROCESAMIENTO DE PEDIDOS",
            font=("Segoe UI", 22, "bold"),
            bg=self.bg_surface,
            fg=self.text_primary
        )
        title_label.pack(pady=(25, 5))
        
        # Subtítulo con autor
        subtitle_label = tk.Label(
            header_frame,
            text="Created by Lucas Gnemmi",
            font=("Segoe UI", 11),
            bg=self.bg_surface,
            fg=self.text_muted
        )
        subtitle_label.pack()
        
        # Versión
        version_label = tk.Label(
            header_frame,
            text="v3.0",
            font=("Segoe UI", 10),
            bg=self.bg_surface,
            fg=self.text_muted
        )
        version_label.place(relx=0.95, rely=0.85, anchor="e")
        
        # Frame central con botones
        buttons_frame = tk.Frame(self.root, bg=self.bg_dark)
        buttons_frame.pack(expand=True, pady=10)
        
        # Botón INICIAR (primario con cyan)
        self.btn_start = tk.Button(
            buttons_frame,
            text="▶  INICIAR SISTEMA",
            font=("Segoe UI", 15, "bold"),
            bg=self.primary,
            fg=self.bg_dark,
            activebackground=self.primary_dark,
            activeforeground=self.bg_dark,
            width=30,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            command=self.start_system
        )
        self.btn_start.pack(pady=12)
        
        # Botón ACTUALIZAR
        self.btn_update = tk.Button(
            buttons_frame,
            text="⟳  ACTUALIZAR SISTEMA",
            font=("Segoe UI", 13),
            bg=self.bg_card,
            fg=self.text_primary,
            activebackground=self.bg_surface,
            activeforeground=self.text_primary,
            width=30,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            command=self.update_system
        )
        self.btn_update.pack(pady=12)
        
        # Botón CHECK FILES
        self.btn_check = tk.Button(
            buttons_frame,
            text="✓  VERIFICAR ARCHIVOS",
            font=("Segoe UI", 13),
            bg=self.bg_card,
            fg=self.text_primary,
            activebackground=self.bg_surface,
            activeforeground=self.text_primary,
            width=30,
            height=2,
            cursor="hand2",
            relief="flat",
            bd=0,
            command=self.check_files
        )
        self.btn_check.pack(pady=12)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg=self.bg_surface, height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Sistema listo",
            font=("Segoe UI", 10),
            bg=self.bg_surface,
            fg=self.text_secondary,
            anchor="w"
        )
        self.status_label.pack(fill=tk.BOTH, padx=15, pady=8)
    
    def update_status(self, message, color=None):
        if color is None:
            color = self.text_secondary
        self.status_label.config(text=message, fg=color)
        self.root.update()
    
    def check_git_status(self):
        """Verificar si hay actualizaciones disponibles"""
        try:
            # Verificar si Git está disponible
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                cwd=str(self.base_dir),
                timeout=5
            )
            
            if result.returncode == 0:
                # Verificar si hay actualizaciones
                subprocess.run(
                    ["git", "fetch", "origin", "main"],
                    capture_output=True,
                    cwd=str(self.base_dir),
                    timeout=10
                )
                
                local_commit = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    capture_output=True,
                    text=True,
                    cwd=str(self.base_dir),
                    timeout=5
                ).stdout.strip()
                
                remote_commit = subprocess.run(
                    ["git", "rev-parse", "origin/main"],
                    capture_output=True,
                    text=True,
                    cwd=str(self.base_dir),
                    timeout=5
                ).stdout.strip()
                
                if local_commit != remote_commit:
                    self.btn_update.config(
                        text="⟳  ACTUALIZAR SISTEMA (¡Disponible!)",
                        bg=self.warning,
                        fg=self.bg_dark
                    )
                    self.update_status("¡Nueva versión disponible!", self.warning)
        except:
            pass  # Si falla, no hacer nada
    
    def start_system(self):
        """Iniciar el sistema principal"""
        self.update_status("Iniciando sistema...", self.success)
        self.btn_start.config(state="disabled")
        
        try:
            # Verificar que existe el archivo principal
            main_file = self.base_dir / "gui_moderna_v2.py"
            if not main_file.exists():
                messagebox.showerror(
                    "Error",
                    "No se encontró gui_moderna_v2.py\n\nUsa 'Verificar Archivos' para reparar."
                )
                self.update_status("Error: Archivo principal no encontrado", self.error)
                self.btn_start.config(state="normal")
                return
            
            # Usar el mismo Python que está ejecutando este script
            python_exe = self.get_python_executable()
            
            if not python_exe or not Path(python_exe).exists():
                messagebox.showerror(
                    "Error",
                    "No se encontró Python interno (python/python.exe) ni Python en el sistema.\n\n"
                    "Por favor, instala Python 3.10+ o copia la carpeta 'python' completa dentro de la app."
                )
                self.update_status("Error: Python no encontrado", self.error)
                self.btn_start.config(state="normal")
                return
            
            # Verificar dependencias rápidamente
            self.update_status("Verificando dependencias...", self.warning)
            
            try:
                test_result = subprocess.run(
                    [python_exe, "-c", "import customtkinter, pandas, openpyxl"],
                    cwd=str(self.base_dir),
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if test_result.returncode != 0:
                    error_output = test_result.stderr if test_result.stderr else test_result.stdout
                    response = messagebox.askyesno(
                        "Dependencias Faltantes",
                        f"Faltan módulos requeridos.\n\n" +
                        f"¿Deseas instalarlos automáticamente?\n\n" +
                        f"(Si no, usa 'Verificar Archivos' para más detalles)"
                    )
                    if response:
                        self.install_packages(['customtkinter', 'pandas', 'openpyxl', 'numpy'])
                    self.btn_start.config(state="normal")
                    return
            except subprocess.TimeoutExpired:
                pass
            except Exception as e:
                # Continuar aunque falle la verificación
                pass
            
            self.update_status("Iniciando interfaz...", self.success)
            
            # Ejecutar sistema - método que funciona en todas las versiones de Windows
            if sys.platform == 'win32':
                # Usar pythonw.exe para aplicaciones GUI (sin consola)
                python_gui_exe = python_exe.replace("python.exe", "pythonw.exe")
                if not Path(python_gui_exe).exists():
                    python_gui_exe = python_exe  # Fallback a python.exe normal
                
                # Ejecutar en proceso independiente sin bloquear
                process = subprocess.Popen(
                    [python_gui_exe, str(main_file)],
                    cwd=str(self.base_dir),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL
                )
            else:
                process = subprocess.Popen(
                    [python_exe, str(main_file)],
                    cwd=str(self.base_dir),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Esperar un momento para verificar que el proceso inició
            import time
            time.sleep(2.0)
            
            # Verificar si el proceso sigue corriendo
            if process.poll() is not None:
                # El proceso terminó inmediatamente, probablemente hubo un error
                messagebox.showerror(
                    "Error al iniciar",
                    f"El sistema se cerró inesperadamente.\n\n" +
                    "Posibles causas:\n" +
                    "• Falta alguna dependencia\n" +
                    "• Error en el código\n\n" +
                    "Intenta ejecutar desde terminal:\n" +
                    f"cd {self.base_dir}\n" +
                    f"python gui_moderna_v2.py\n\n" +
                    "Para ver el error completo."
                )
                self.update_status("Error al iniciar", self.error)
                self.btn_start.config(state="normal")
                return
            
            self.update_status("Sistema iniciado correctamente", self.success)
            
            # Cerrar launcher después de 1.5 segundos
            self.root.after(1500, self.root.destroy)
            
        except subprocess.TimeoutExpired:
            messagebox.showerror(
                "Error de Timeout",
                "La verificación de dependencias tardó demasiado.\n\n" +
                "Intenta ejecutar manualmente:\n" +
                "python gui_moderna_v2.py"
            )
            self.update_status("Timeout", self.error)
            self.btn_start.config(state="normal")
        except Exception as e:
            messagebox.showerror(
                "Error Inesperado",
                f"Error al iniciar sistema:\n\n{str(e)}\n\n" +
                f"Python: {sys.executable}\n" +
                f"Directorio: {self.base_dir}"
            )
            self.update_status(f"Error: {str(e)}", self.error)
            self.btn_start.config(state="normal")
    
    def update_system(self):
        """Actualizar sistema desde GitHub"""
        response = messagebox.askyesno(
            "Actualizar Sistema",
            "¿Deseas actualizar a la última versión?\n\n" +
            "Se descargarán los últimos cambios desde GitHub.\n" +
            "Tus configuraciones se mantendrán intactas."
        )
        
        if not response:
            return
        
        # Deshabilitar botones durante actualización
        self.btn_start.config(state="disabled")
        self.btn_update.config(state="disabled")
        self.btn_check.config(state="disabled")
        
        self.update_status("Actualizando sistema...", self.warning)
        
        # Abrir ventana de progreso
        self.show_update_window()
    
    def show_update_window(self):
        """Mostrar ventana con progreso de actualización"""
        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizando Sistema")
        update_window.geometry("600x400")
        update_window.resizable(False, False)
        update_window.configure(bg=self.bg_dark)
        update_window.transient(self.root)
        update_window.grab_set()
        
        # Título
        title = tk.Label(
            update_window,
            text="Actualizando Sistema",
            font=("Segoe UI", 14, "bold"),
            bg=self.bg_dark,
            fg=self.text_primary
        )
        title.pack(pady=10)
        
        # Área de texto para log
        log_text = scrolledtext.ScrolledText(
            update_window,
            font=("Consolas", 9),
            bg=self.bg_surface,
            fg=self.success,
            height=20
        )
        log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def log_message(message):
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            log_text.see(tk.END)
            log_text.update()
        
        def run_update():
            try:
                log_message("Iniciando actualización...")
                
                # Verificar Git
                result = subprocess.run(
                    ["git", "--version"],
                    capture_output=True,
                    text=True,
                    cwd=str(self.base_dir),
                    timeout=5
                )
                
                if result.returncode != 0:
                    log_message("ERROR: Git no está instalado")
                    messagebox.showerror("Error", "Git no está instalado\n\nDescarga desde: https://git-scm.com/download/win")
                    update_window.destroy()
                    return
                
                log_message(f"Git instalado: {result.stdout.strip()}")
                
                # Guardar archivos de configuración
                log_message("Guardando configuraciones locales...")
                backup_dir = self.base_dir / "backup_temp"
                backup_dir.mkdir(exist_ok=True)
                
                config_files = ["agenda_config.json", "rules.json", "products.json"]
                for file in config_files:
                    src = self.base_dir / file
                    if src.exists():
                        import shutil
                        shutil.copy2(src, backup_dir / file)
                        log_message(f"  Respaldado: {file}")
                
                # Fetch cambios
                log_message("Descargando cambios desde GitHub...")
                result = subprocess.run(
                    ["git", "fetch", "origin", "main"],
                    capture_output=True,
                    text=True,
                    cwd=str(self.base_dir),
                    timeout=30
                )
                
                if result.returncode != 0:
                    log_message(f"ERROR: {result.stderr}")
                    raise Exception("Error al descargar cambios")
                
                log_message("Cambios descargados")
                
                # Reset hard
                log_message("Aplicando actualización...")
                result = subprocess.run(
                    ["git", "reset", "--hard", "origin/main"],
                    capture_output=True,
                    text=True,
                    cwd=str(self.base_dir),
                    timeout=30
                )
                
                if result.returncode != 0:
                    log_message(f"ERROR: {result.stderr}")
                    raise Exception("Error al aplicar cambios")
                
                log_message("Actualización aplicada")
                
                # Restaurar configuraciones
                log_message("Restaurando configuraciones...")
                for file in config_files:
                    src = backup_dir / file
                    if src.exists():
                        import shutil
                        shutil.copy2(src, self.base_dir / file)
                        log_message(f"  Restaurado: {file}")
                
                # Limpiar backup
                import shutil
                shutil.rmtree(backup_dir)
                
                log_message("")
                log_message("✓ ¡ACTUALIZACIÓN COMPLETADA!")
                log_message("")
                log_message("Ya puedes usar el sistema con la nueva versión")
                
                self.update_status("Actualización completada", self.success)
                
                messagebox.showinfo(
                    "Actualización Completada",
                    "El sistema se actualizó correctamente.\n\nYa puedes iniciar el sistema."
                )
                
                # Reactivar botones
                self.btn_start.config(state="normal")
                self.btn_update.config(state="normal")
                self.btn_check.config(state="normal")
                
            except Exception as e:
                log_message(f"ERROR: {str(e)}")
                messagebox.showerror("Error", f"Error durante actualización:\n{str(e)}")
                self.update_status("Error en actualización", self.error)
                
                # Reactivar botones
                self.btn_start.config(state="normal")
                self.btn_update.config(state="normal")
                self.btn_check.config(state="normal")
            
            finally:
                # Botón cerrar
                close_btn = tk.Button(
                    update_window,
                    text="Cerrar",
                    command=update_window.destroy,
                    font=("Segoe UI", 10),
                    bg=self.bg_card,
                    fg=self.text_primary,
                    width=15,
                    relief="flat"
                )
                close_btn.pack(pady=10)
        
        # Ejecutar actualización en thread separado
        thread = threading.Thread(target=run_update, daemon=True)
        thread.start()
    
    def check_files(self):
        """Verificar integridad de archivos y carpeta libs"""
        self.update_status("Verificando archivos...", self.warning)
        
        critical_files = [
            ("gui_moderna_v2.py", "Interfaz principal"),
            ("procesamiento_v2.py", "Motor de procesamiento"),
            ("agenda_manager.py", "Gestor de agenda"),
            ("rules_manager.py", "Gestor de reglas"),
            ("products_manager.py", "Gestor de productos"),
            ("EXE_Procesar_Ordenes.bat", "Launcher batch"),
            ("launcher.py", "Launcher Python"),
        ]
        
        # Carpetas críticas
        critical_dirs = [
            ("libs", "Librerías empaquetadas"),
            ("libs/customtkinter", "CustomTkinter"),
            ("libs/pandas", "Pandas"),
            ("libs/openpyxl", "OpenPyXL"),
        ]
        
        missing_files = []
        missing_dirs = []
        
        report = "VERIFICACION DEL SISTEMA\n"
        report += "=" * 50 + "\n\n"
        
        # Verificar archivos
        report += "ARCHIVOS:\n"
        for file, description in critical_files:
            file_path = self.base_dir / file
            exists = file_path.exists()
            status = "[OK]" if exists else "[FALTA]"
            report += f"  {status:10} {description:25} ({file})\n"
            
            if not exists:
                missing_files.append((file, description))
        
        # Verificar carpetas de librerías
        report += "\nLIBRERIAS EMPAQUETADAS:\n"
        for dir_name, description in critical_dirs:
            dir_path = self.base_dir / dir_name
            exists = dir_path.exists() and dir_path.is_dir()
            status = "[OK]" if exists else "[FALTA]"
            report += f"  {status:10} {description:25} ({dir_name})\n"
            
            if not exists:
                missing_dirs.append((dir_name, description))
        
        report += "\nNOTA: El sistema usa librerias empaquetadas en libs/\n"
        report += "   No necesitas instalar dependencias con pip.\n"
        
        # Resumen
        has_issues = missing_files or missing_dirs
        
        if has_issues:
            report += f"\n{'='*50}\n"
            report += "ADVERTENCIA - SE ENCONTRARON PROBLEMAS:\n"
            
            if missing_files:
                report += f"\n  Archivos faltantes: {len(missing_files)}\n"
                for file, desc in missing_files:
                    report += f"    - {desc}\n"
            
            if missing_dirs:
                report += f"\n  Carpetas faltantes: {len(missing_dirs)}\n"
                for dir_name, desc in missing_dirs:
                    report += f"    - {desc}\n"
            
            self.update_status(f"Problemas encontrados", self.error)
            self.update_status(f"Problemas encontrados", self.error)
            
            if missing_files or missing_dirs:
                response = messagebox.askquestion(
                    "Archivos/Carpetas Faltantes",
                    report + "\n\n¿Deseas intentar reparar descargando la última versión?",
                    icon='warning'
                )
                
                if response == 'yes':
                    self.update_system()
                    return
        else:
            report += "\n" + "=" * 50 + "\n"
            report += "SISTEMA LISTO - Todo verificado correctamente\n"
            report += "\nTodas las librerias estan empaquetadas.\n"
            report += "No necesitas instalar nada adicional.\n"
            messagebox.showinfo("Verificacion Completa", report)


def main():
    root = tk.Tk()
    root.lift()  # Traer ventana al frente
    root.attributes('-topmost', True)  # Mantener al frente
    root.after(100, lambda: root.attributes('-topmost', False))  # Desactivar después de 100ms
    app = SystemLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
