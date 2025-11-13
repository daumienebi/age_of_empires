import tkinter as tk
from tkinter import ttk  # Importamos ttk para la barra de progreso
import os

try:
    from PIL import ImageTk, Image
except ImportError:
    print("Error: La biblioteca 'Pillow' no está instalada.")
    print("Por favor, instálala para cargar imágenes JPG/PNG:")
    print("pip install Pillow")
    exit()

class PantallaCarga(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # Dejar la ventana sin titulo ni botones de minimizar, maximizar y salir
        self.overrideredirect(True)
        try:
            script_dir = os.path.dirname(__file__)  # la carpeta gui
            project_root = os.path.dirname(script_dir)  # Raíz del proyecto
            image_path = os.path.join(project_root, "resources", "splash_screen.jpeg")
            imagen = Image.open(image_path)
            # Convertir la imagen a un formato para Tkinter
            self.bg_image = ImageTk.PhotoImage(imagen)
            self.label_splash_screen = tk.Label(self, image=self.bg_image)
            self.label_splash_screen.pack(expand=True, fill="both")
            # Ajustar el tamaño de la ventana al de la imagen
            self.geometry(f"{self.bg_image.width()}x{self.bg_image.height()}")
        except FileNotFoundError:
            print(f"ERROR: No se pudo encontrar la imagen: {image_path}")
        except Exception as e:
            print(f"ERROR: No se pudo cargar la imagen: {e}")
        # La barra ocupa el 80% del ancho de la imagen
        bar_width = self.bg_image.width() * 0.8
        # La centramos horizontalmente
        bar_x = (self.bg_image.width() - bar_width) / 2
        # Colocarlo al 85% de la altura de la imagen
        bar_y = self.bg_image.height() * 0.85
        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=bar_width,mode='determinate')
        # La posicionamos usando .place() para ponerla sobre la imagen
        self.progress_bar.place(x=bar_x, y=bar_y)
        self.centrar_ventana()
        # Quitamos el 'after' de 3000ms y llamamos a nuestra nueva función
        self.progreso_actual = 0
        self.paso_progreso = 1
        # (3000ms / 100 pasos = 30ms por paso)
        self.tiempo_paso = 30
        self.actualizar_progreso()

    def centrar_ventana(self):
        """Centra esta ventana en la mitad de la pantalla."""
        self.update_idletasks()  # Asegurar que Tkinter tenga las dimensiones calculadas
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def actualizar_progreso(self):
        if self.progreso_actual < 100:
            # Avanzar la barra
            self.progreso_actual += self.paso_progreso
            self.progress_bar['value'] = self.progreso_actual
            self.after(self.tiempo_paso, self.actualizar_progreso)
        else:
            # lanza la GUI al 100%
            self.lanzar_gui_principal()

    def lanzar_gui_principal(self):
        """Destruye esta pantalla de carga y muestra la ventana principal."""
        self.destroy()  # Cierra la ventana de carga
        self.master.deiconify()  # Muestra la ventana principal
        print("Pantalla de carga finalizada. Lanzando GUI principal.")