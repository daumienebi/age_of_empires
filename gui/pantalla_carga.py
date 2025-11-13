import tkinter as tk
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
        self.title("Cargando Age of Empires...")
        # Dejar la ventana sin titulo ni botones de minimizar, maximizar y salir
        self.overrideredirect(True)
        try:
            script_dir = os.path.dirname(__file__)  # la carpeta en la que nos encontramos
            project_root = os.path.dirname(script_dir)  # Raíz del proyecto
            #image_path = os.path.join(project_root, "resources", "splash_screen.jpeg")
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
        self.centrar_ventana()
        # Simular una carga falsa
        self.after(3000, self.lanzar_gui_principal)

    def centrar_ventana(self):
        """Centra esta ventana en la mitad de la pantalla."""
        self.update_idletasks()  # Asegurar que Tkinter tenga las dimensiones calculadas
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def lanzar_gui_principal(self):
        """Destruye esta pantalla de carga y muestra la ventana principal."""
        self.destroy()  # Cierra la ventana de carga
        self.master.deiconify()  # Muestra la ventana principal
        print("Pantalla de carga finalizada. Lanzando GUI principal.")