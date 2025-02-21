import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import subprocess
import json
import os
import datetime
import locale
import base64
import urllib.request
import threading
import sys
import logging
from typing import List, Optional

# Configuración de logging para depuración
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Base64 del icono PNG (placeholder)
ICON_BASE64 = """
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
"""

# Widget de indicador de actividad con efecto parpadeante,
# que mantiene su tamaño fijo usando una imagen vacía para evitar desplazar el texto.
class ActivityIndicator(tk.Label):
    def __init__(self, master: tk.Widget, icon_image: tk.PhotoImage, blink_interval: int = 1000, **kwargs) -> None:
        """
        :param blink_interval: Intervalo de parpadeo en milisegundos.
        """
        super().__init__(master, **kwargs)
        self.icon_image = icon_image
        # Imagen vacía para mantener el tamaño del widget
        self.empty_image = tk.PhotoImage(width=icon_image.width(), height=icon_image.height())
        self.blink_interval = blink_interval
        self._blinking = False
        self._job = None
        self._visible = True

    def _blink(self) -> None:
        if not self._blinking:
            return
        # Alterna sin cambiar la dimensión: muestra icono o imagen vacía.
        self.config(image=self.icon_image if self._visible else self.empty_image)
        self._visible = not self._visible
        self._job = self.after(self.blink_interval, self._blink)

    def start(self) -> None:
        if not self._blinking:
            self._blinking = True
            self._visible = True
            self.config(image=self.icon_image)
            self._job = self.after(self.blink_interval, self._blink)

    def stop(self) -> None:
        if self._blinking:
            self._blinking = False
            if self._job:
                self.after_cancel(self._job)
                self._job = None
            # Al detenerse, se muestra la imagen vacía para conservar el espacio.
            self.config(image=self.empty_image)
            self._visible = True

class CondaEnvMaster(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        # Ocultar la ventana principal mientras se inicializa
        self.withdraw()
        logging.debug("Ventana principal oculta para inicialización.")

        # Verificar que 'conda' esté instalado y en el PATH
        if not self.is_conda_installed():
            logging.error("Conda no está instalado o no se encuentra en el PATH.")
            self.show_conda_required_message()
            self.destroy()
            sys.exit(1)

        self.title("CondaEnv Master")
        self.geometry("800x350")
        self.texts = self.load_translations()
        self.set_icon()  # Guarda self.icon_image para uso posterior
        self.create_widgets()

        # Al iniciar, se muestra el estado de "Cargando entornos..."
        self.update_env_list()
        logging.debug("Inicialización completada, se mostrará la ventana principal.")
        self.deiconify()

    def run_conda_command(self, args: List[str], check: bool = False,
                          capture_output: bool = True, text: bool = True) -> subprocess.CompletedProcess:
        """Ejecuta un comando de conda y retorna el resultado."""
        cmd = ["conda"] + args
        logging.debug(f"Ejecutando comando: {' '.join(cmd)}")
        return subprocess.run(cmd, check=check, capture_output=capture_output, text=text)

    def is_conda_installed(self) -> bool:
        """Verifica que 'conda' esté instalado."""
        try:
            result = self.run_conda_command(["--version"], check=True)
            logging.debug(f"Conda instalado: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"Error al verificar conda: {e}")
            return False

    def show_conda_required_message(self) -> None:
        """Muestra un mensaje informativo si 'conda' no está disponible."""
        messagebox.showinfo(
            "Conda Required",
            "Conda is required to run this application. Please install it from the following link:\n\n"
            "https://docs.anaconda.com/miniconda/miniconda-install/"
        )

    def set_icon(self) -> None:
        """Decodifica y asigna el icono de la aplicación, guardándolo para uso posterior."""
        try:
            self.icon_image = tk.PhotoImage(data=base64.b64decode(ICON_BASE64.strip()))
            self.iconphoto(True, self.icon_image)
        except Exception as e:
            logging.error(f"Error al establecer el icono: {e}")
            self.icon_image = None

    def load_translations(self) -> dict:
        """Carga las traducciones desde una URL o utiliza valores por defecto."""
        try:
            with urllib.request.urlopen("https://raw.githubusercontent.com/flowese/statics/main/condaenvmaster-translations.json") as url:
                translations = json.loads(url.read().decode())
            logging.debug("Traducciones cargadas desde la URL.")
        except Exception as e:
            logging.error(f"Error al cargar traducciones: {e}")
            translations = {"en": {
                "app_name": "CondaEnv Master",
                "env_name": "Environment Name:",
                "python_version": "Python Version:",
                "create_button": "➕",
                "env_name_col": "Environment Name",
                "python_version_col": "Python Version",
                "creation_date_col": "Creation Date and Time",
                "export_col": "Export",
                "delete_col": "Delete",
                "success_create": "Success",
                "success_create_msg": "Environment '{env_name}' created with Python {python_version}",
                "error_create": "Error",
                "error_create_msg": "Failed to create the environment",
                "error_create_exists_msg": "Environment '{env_name}' already exists",
                "warning": "Warning",
                "warning_msg": "All fields must be completed",
                "confirm_delete": "Confirmation",
                "confirm_delete_msg": "Are you sure you want to delete the environment '{env_name}'?",
                "success_delete_msg": "Environment '{env_name}' deleted",
                "error_delete_msg": "Failed to delete the environment '{env_name}'",
                "delete_button": "❌",
                "export_button": "⬇️",
                "creating_env": "Creating environment...",
                "deleting_env": "Deleting environment...",
                "exporting_env": "Exporting environment...",
                "success_export": "Success",
                "success_export_msg": "Environment '{env_name}' exported successfully",
                "error_export_msg": "Failed to export the environment '{env_name}'",
                "import_env": "Import Environment",
                "import_button": "Import",
                "importing_env": "Importing environment...",
                "success_import": "Success",
                "success_import_msg": "Environment '{env_name}' imported successfully",
                "error_import_msg": "Failed to import the environment"
            }}
        lang, encoding = locale.getlocale()
        if not lang:
            lang, encoding = locale.getdefaultlocale()
        lang = lang[:2] if lang else 'en'
        return translations.get(lang, translations["en"])

    def create_widgets(self) -> None:
        """Crea y organiza los widgets de la interfaz."""
        # --- Panel superior para controles de creación e importación ---
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10, padx=20, fill=tk.X)
        for i in range(6):
            control_frame.grid_columnconfigure(i, weight=1)

        tk.Label(control_frame, text=self.texts["env_name"], font=("Helvetica", 12))\
            .grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.env_name_entry = tk.Entry(control_frame, width=20, font=("Helvetica", 12))
        self.env_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(control_frame, text=self.texts["python_version"], font=("Helvetica", 12))\
            .grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.python_version_combo = ttk.Combobox(control_frame, state="readonly", width=15, font=("Helvetica", 12))
        self.python_version_combo.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.load_python_versions()

        self.create_button = tk.Button(control_frame, text=self.texts["create_button"],
                                       command=self.create_env, width=3, font=("Helvetica", 12))
        self.create_button.grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.import_button = tk.Button(control_frame, text=self.texts["import_button"],
                                       command=self.import_env, width=10, font=("Helvetica", 12))
        self.import_button.grid(row=0, column=5, padx=10, pady=5, sticky="w")

        # --- Panel central para la lista de entornos ---
        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
        columns = ("#1", "#2", "#3", "#4", "#5")
        self.env_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Custom.Treeview")
        self.env_tree.heading("#1", text=self.texts["env_name_col"], anchor="center")
        self.env_tree.heading("#2", text=self.texts["python_version_col"], anchor="center")
        self.env_tree.heading("#3", text=self.texts["creation_date_col"], anchor="center")
        self.env_tree.heading("#4", text=self.texts["export_col"], anchor="center")
        self.env_tree.heading("#5", text=self.texts["delete_col"], anchor="center")
        for col in columns:
            self.env_tree.column(col, anchor="center", width=130)
        self.env_tree.column("#4", anchor="center", width=60)
        self.env_tree.column("#5", anchor="center", width=60)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.env_tree.yview)
        self.env_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.env_tree.pack(expand=True, fill=tk.BOTH)
        style = ttk.Style()
        style.configure("Custom.Treeview.Heading", font=("Helvetica", 12))
        style.configure("Custom.Treeview", font=("Helvetica", 12))
        self.env_tree.bind("<Button-1>", self.on_treeview_click)

        # --- Barra de estado inferior centrada y con altura fija ---
        status_frame = tk.Frame(self, height=25)
        status_frame.pack(side="bottom", fill="x", padx=20, pady=5)
        status_frame.pack_propagate(False)
        status_container = tk.Frame(status_frame)
        status_container.pack(expand=True)

        # Marco fijo para el indicador, a la izquierda del texto
        indicator_frame = tk.Frame(status_container, width=20, height=20)
        indicator_frame.pack_propagate(False)
        indicator_frame.grid(row=0, column=0, padx=(0, 5))
        if self.icon_image:
            small_icon = self.icon_image.subsample(12, 12)
            self.status_indicator = ActivityIndicator(indicator_frame, icon_image=small_icon, blink_interval=1000,
                                                       bg=indicator_frame.cget("bg"))
            self.status_indicator.pack(fill="both", expand=True)
            self.status_indicator.grid_remove()  # Inicialmente oculto
        else:
            self.status_indicator = None

        self.status_label = tk.Label(status_container, text="", font=("Helvetica", 10))
        self.status_label.grid(row=0, column=1, sticky="w")

    def disable_ui(self) -> None:
        """Deshabilita los controles para prevenir acciones concurrentes."""
        self.env_name_entry.config(state="disabled")
        self.python_version_combo.config(state="disabled")
        self.create_button.config(state="disabled")
        self.import_button.config(state="disabled")
        self.env_tree.unbind("<Button-1>")

    def enable_ui(self) -> None:
        """Habilita los controles de la interfaz."""
        self.env_name_entry.config(state="normal")
        self.python_version_combo.config(state="readonly")
        self.create_button.config(state="normal")
        self.import_button.config(state="normal")
        self.env_tree.bind("<Button-1>", self.on_treeview_click)

    def start_status(self, message: str) -> None:
        """Muestra un mensaje de estado y activa el indicador de actividad."""
        self.status_label.config(text=message)
        if self.status_indicator:
            self.status_indicator.grid()  # Asegura que se muestre
            self.status_indicator.start()
        self.update_idletasks()  # Forzar actualización inmediata

    def stop_status(self) -> None:
        """Limpia el mensaje de estado y oculta el indicador de actividad."""
        self.status_label.config(text="")
        if self.status_indicator:
            self.status_indicator.stop()
            self.status_indicator.grid_remove()
        self.update_idletasks()

    def run_in_thread(self, target, *args) -> None:
        """Ejecuta una función en un hilo separado para no bloquear la UI."""
        thread = threading.Thread(target=target, args=args, daemon=True)
        thread.start()

    def load_python_versions(self) -> None:
        """Carga las versiones de Python disponibles usando 'conda search'."""
        try:
            result = self.run_conda_command(["search", "python", "--json"])
            data = json.loads(result.stdout)
            versions = sorted(
                {pkg["version"] for pkg in data.get("python", [])
                 if pkg["version"].replace('.', '').isdigit()},
                key=self.version_key,
                reverse=True
            )
            self.python_version_combo["values"] = versions
            if versions:
                self.python_version_combo.set(versions[0])
            logging.debug("Versiones de Python cargadas.")
        except Exception as e:
            logging.error(f"Error al cargar versiones de Python: {e}")
            self.python_version_combo["values"] = []
            self.python_version_combo.set("")

    def version_key(self, version_str: str) -> tuple:
        """Convierte una versión en una tupla de enteros para ordenarla."""
        return tuple(map(int, version_str.split(".")))

    def get_creation_date(self, path: str) -> str:
        """Obtiene la fecha de creación (o modificación) de un directorio."""
        try:
            stat = os.stat(path)
            creation_time = getattr(stat, 'st_birthtime', stat.st_mtime)
            return datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logging.error(f"Error al obtener fecha de creación: {e}")
            return "Desconocida" if self.texts["app_name"] == 'CondaEnv Master' else "Unknown"

    def update_env_list(self) -> None:
        """Muestra el estado de carga y actualiza la lista de entornos en segundo plano."""
        self.start_status("Cargando entornos...")
        self.run_in_thread(self.update_env_list_thread)

    def update_env_list_thread(self) -> None:
        env_list = []
        try:
            result = self.run_conda_command(["env", "list"])
            envs = [line.split() for line in result.stdout.splitlines() if line and not line.startswith("#")]
            envs = [env for env in envs if env[0] != "base" and not env[0].startswith("/Users/")]
        except Exception as e:
            logging.error(f"Error al obtener lista de entornos: {e}")
            envs = []
        for env in envs:
            env_name = env[0]
            try:
                result = self.run_conda_command(["list", "-n", env_name, "--json"])
                packages = json.loads(result.stdout)
                python_version = next((pkg["version"] for pkg in packages if pkg["name"] == "python"), "Unknown")
            except Exception as e:
                logging.error(f"Error al obtener versión de Python para {env_name}: {e}")
                python_version = "Unknown"
            try:
                result = self.run_conda_command(["info", "--json"])
                conda_info = json.loads(result.stdout)
                envs_dirs = conda_info.get('envs_dirs', [])
                env_dir: Optional[str] = next((os.path.join(dir_path, env_name)
                                               for dir_path in envs_dirs
                                               if os.path.exists(os.path.join(dir_path, env_name))), None)
                creation_date = self.get_creation_date(env_dir) if env_dir else (
                    "Desconocida" if self.texts["app_name"] == 'CondaEnv Master' else "Unknown")
            except Exception as e:
                logging.error(f"Error al obtener información del entorno {env_name}: {e}")
                creation_date = "Unknown"
            env_list.append((env_name, python_version, creation_date))
        def finish_update():
            self.populate_env_tree(env_list)
            self.stop_status()
        self.after(0, finish_update)

    def populate_env_tree(self, env_list: List[tuple]) -> None:
        """Rellena el Treeview con la lista de entornos."""
        for item in self.env_tree.get_children():
            self.env_tree.delete(item)
        for env in env_list:
            env_name, python_version, creation_date = env
            self.env_tree.insert("", "end", values=(
                env_name,
                python_version,
                creation_date,
                self.texts["export_button"],
                self.texts["delete_button"]
            ))

    def on_treeview_click(self, event) -> None:
        """Detecta clics en el Treeview para exportar o eliminar entornos."""
        item = self.env_tree.identify_row(event.y)
        if item:
            column = self.env_tree.identify_column(event.x)
            env_name = self.env_tree.item(item, "values")[0]
            if column == "#5":  # Botón de eliminar
                if messagebox.askyesno(self.texts["confirm_delete"],
                                       self.texts["confirm_delete_msg"].format(env_name=env_name)):
                    self.delete_env(env_name)
            elif column == "#4":  # Botón de exportar
                self.export_env(env_name)

    def create_env(self) -> None:
        """Inicia la creación de un entorno en un hilo aparte."""
        env_name = self.env_name_entry.get().strip()
        python_version = self.python_version_combo.get().strip()
        if not env_name or not python_version:
            messagebox.showwarning(self.texts["warning"], self.texts["warning_msg"])
            return
        self.disable_ui()
        self.start_status(self.texts["creating_env"])
        self.run_in_thread(self.create_env_thread, env_name, python_version)

    def create_env_thread(self, env_name: str, python_version: str) -> None:
        try:
            result = self.run_conda_command(["env", "list"])
            envs = [line.split()[0] for line in result.stdout.splitlines() if line and not line.startswith("#")]
            if env_name in envs:
                self.after(0, lambda: messagebox.showerror(
                    self.texts["error_create"],
                    self.texts["error_create_exists_msg"].format(env_name=env_name)
                ))
                return
            subprocess.check_call(["conda", "create", "-n", env_name, f"python={python_version}", "--yes"])
            self.after(0, lambda: messagebox.showinfo(
                self.texts["success_create"],
                self.texts["success_create_msg"].format(env_name=env_name, python_version=python_version)
            ))
            self.after(0, self.update_env_list)
            self.after(0, lambda: self.env_name_entry.delete(0, tk.END))
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al crear entorno: {e}")
            self.after(0, lambda: messagebox.showerror(
                self.texts["error_create"], self.texts["error_create_msg"]
            ))
        finally:
            self.after(0, self.stop_status)
            self.after(0, self.enable_ui)

    def delete_env(self, env_name: str) -> None:
        """Inicia la eliminación de un entorno en un hilo aparte."""
        self.disable_ui()
        self.start_status(self.texts["deleting_env"])
        self.run_in_thread(self.delete_env_thread, env_name)

    def delete_env_thread(self, env_name: str) -> None:
        try:
            subprocess.check_call(["conda", "env", "remove", "-n", env_name, "--yes"])
            self.after(0, lambda: messagebox.showinfo(
                self.texts["success_delete_msg"],
                self.texts["success_delete_msg"].format(env_name=env_name)
            ))
            self.after(0, self.update_env_list)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al eliminar entorno {env_name}: {e}")
            self.after(0, lambda: messagebox.showerror(
                self.texts["error_delete_msg"].format(env_name=env_name),
                self.texts["error_delete_msg"].format(env_name=env_name)
            ))
        finally:
            self.after(0, self.stop_status)
            self.after(0, self.enable_ui)

    def export_env(self, env_name: str) -> None:
        """Inicia la exportación de un entorno a YAML en un hilo aparte."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".yml",
            initialfile=f"{env_name}.yml",
            filetypes=[("YAML files", "*.yml"), ("All files", "*.*")]
        )
        if not file_path:
            return
        self.disable_ui()
        self.start_status(self.texts["exporting_env"])
        self.run_in_thread(self.export_env_thread, env_name, file_path)

    def export_env_thread(self, env_name: str, file_path: str) -> None:
        try:
            with open(file_path, 'w') as f:
                subprocess.check_call(["conda", "env", "export", "-n", env_name], stdout=f)
            self.after(0, lambda: messagebox.showinfo(
                self.texts["success_export"],
                self.texts["success_export_msg"].format(env_name=env_name)
            ))
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al exportar entorno {env_name}: {e}")
            self.after(0, lambda: messagebox.showerror(
                self.texts["error_export_msg"].format(env_name=env_name)
            ))
        finally:
            self.after(0, self.stop_status)
            self.after(0, self.enable_ui)

    def import_env(self) -> None:
        """Inicia la importación de un entorno desde YAML en un hilo aparte."""
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yml"), ("All files", "*.*")])
        if not file_path:
            return
        self.disable_ui()
        self.start_status(self.texts["importing_env"])
        self.run_in_thread(self.import_env_thread, file_path)

    def import_env_thread(self, file_path: str) -> None:
        try:
            env_name = self.extract_env_name(file_path)
            subprocess.check_call(["conda", "env", "create", "-f", file_path])
            self.after(0, lambda: messagebox.showinfo(
                self.texts["success_import"],
                self.texts["success_import_msg"].format(env_name=env_name)
            ))
            self.after(0, self.update_env_list)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al importar entorno desde {file_path}: {e}")
            self.after(0, lambda: messagebox.showerror(self.texts["error_import_msg"]))
        finally:
            self.after(0, self.stop_status)
            self.after(0, self.enable_ui)

    def extract_env_name(self, file_path: str) -> str:
        """Extrae el nombre del entorno desde el archivo YAML."""
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if line.strip().startswith('name:'):
                        return line.split(':', 1)[1].strip()
        except Exception as e:
            logging.error(f"Error al extraer el nombre del entorno: {e}")
        return "Unknown"

if __name__ == "__main__":
    app = CondaEnvMaster()
    app.mainloop()
