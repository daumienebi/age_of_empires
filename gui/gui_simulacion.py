# Colores : https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

try:
    from PIL import ImageTk, Image, ImageOps
except ImportError:
    print("Error: La biblioteca 'Pillow' no está instalada.")
    print("Por favor, instálala para cargar imágenes JPG/PNG:")
    print("pip install Pillow")
    sys.exit(1)

# Importar desde la carpeta raíz, nbs facilitará la empaquetación del codigo
script_dir = os.path.dirname(__file__)
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

try:
    from tablero import Tablero
    from tablero import TERRENO_FACIL, TERRENO_DIFICIL, TERRENO_RIO, RECURSO, SIN_ACCESO
    from a_estrella import buscar_ruta, TROPAS_INICIALES
except ImportError as e:
    print(f"Error: No se pudieron importar los módulos de lógica: {e}")
    print(f"Asegúrate de que 'tablero.py' y 'a_estrella.py' están en {project_root}")
    sys.exit(1)

class GUISimulacion:
    """
        Clase principal de la interfaz gráfica.
        Contiene los controles (botones, entradas) y el canvas del tablero.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Age of Empires - Simulación Algoritmo A*")
        self.master.geometry("1024x768")

        self.mi_tablero = None
        self.tamanho_celda = 40  # Tamaño para las imágenes

        self.punto_inicio = (0, 0)
        self.punto_fin = None  # Se definirá al generar el tablero
        self.modo_seleccion = None  # Puede ser "inicio" o "fin"

        # Carga de Imágenes
        self.imagenes_terreno = {}  # Diccionario para guardar las referencias
        self.cargar_imagenes()

        # Barra de menu
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # --- Menú "Ayuda" ---
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Añadir items al menú Ayuda
        menu_ayuda.add_command(label="Manual", command=self.mostrar_acerca_de)
        menu_ayuda.add_command(label="Mostrar Leyenda", command=self.mostrar_leyenda)
        menu_ayuda.add_command(label="Acerca de...", command=self.mostrar_acerca_de)

        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Salir", command=self.master.quit)

        # Frame superior con los controles
        frame_controles = ttk.Frame(master, padding="10")
        frame_controles.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(frame_controles, text="Ancho (Tablero):").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_ancho = ttk.Entry(frame_controles, width=5)
        self.entry_ancho.insert(0, "20")  # Valor por defecto
        self.entry_ancho.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_controles, text="Alto (Tablero):").pack(side=tk.LEFT, padx=5)
        self.entry_alto = ttk.Entry(frame_controles, width=5)
        self.entry_alto.insert(0, "15")  # Valor por defecto
        self.entry_alto.pack(side=tk.LEFT, padx=5)

        self.btn_generar = tk.Button(frame_controles, text="1.Generar tablero",bg='SpringGreen1',command=self.generar_y_dibujar_tablero)
        self.btn_generar.pack(side=tk.LEFT, padx=10)

        # Botones del frame superior
        self.btn_set_inicio = tk.Button(frame_controles, text="2.Elegir Inicio",bg='DarkOliveGreen1', command=self.activar_modo_inicio)
        self.btn_set_inicio.pack(side=tk.LEFT, padx=5)

        self.btn_set_fin = tk.Button(frame_controles, text="3.Elegir Fin",bg='IndianRed2',command=self.activar_modo_fin)
        self.btn_set_fin.pack(side=tk.LEFT, padx=5)

        self.btn_ruta = tk.Button(frame_controles, text="4.Buscar Ruta 🔍", bg='goldenrod1', command=self.buscar_y_dibujar_ruta)
        self.btn_ruta.pack(side=tk.LEFT, padx=10)

        self.status_label = ttk.Label(frame_controles, text="Ajusta el tamaño y genera un tablero.", font=("Arial", 10))
        self.status_label.pack(side=tk.LEFT, padx=20, fill=tk.X, expand=True)

        self.results_label = tk.Label(master,
                                      text="Resultados: (Genera un tablero y busca una ruta)",
                                      font=("Arial", 14, "bold"),
                                      fg="#00008B",  # Color "DarkBlue"
                                      pady=5)  # Un poco de espacio vertical
        self.results_label.pack(side=tk.TOP, fill=tk.X)

        # Frame inferior que contiene el tablero
        frame_tablero = ttk.Frame(master, padding="10")
        frame_tablero.pack(expand=True, fill=tk.BOTH)

        # --- PASO 1: Canvas "Scrollable" ---
        v_scroll = ttk.Scrollbar(frame_tablero, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(frame_tablero, orient=tk.HORIZONTAL)

        self.canvas_tablero = tk.Canvas(frame_tablero, bg="gray75",yscrollcommand=v_scroll.set,
                                        xscrollcommand=h_scroll.set,borderwidth=0,
                                        highlightthickness=0)

        v_scroll.config(command=self.canvas_tablero.yview)
        h_scroll.config(command=self.canvas_tablero.xview)

        frame_tablero.grid_rowconfigure(0, weight=1)
        frame_tablero.grid_columnconfigure(0, weight=1)

        self.canvas_tablero.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        # Vincular el clic del Canvas ---
        self.canvas_tablero.bind("<Button-1>", self.on_canvas_click)

    def mostrar_leyenda(self):
        """Crea una nueva ventana Toplevel para mostrar la leyenda."""
        legend_window = tk.Toplevel(self.master)
        legend_window.title("Leyenda")
        legend_window.resizable(False, False)  # Evitar que se redimensione

        # Lo convertimos en una ventana modal, bloqueando la ventana principal
        legend_window.transient(self.master)
        legend_window.grab_set()

        frame_leyenda = ttk.Frame(legend_window, padding="20")
        frame_leyenda.pack(expand=True, fill="both")

        # Lista de items de la leyenda (char, descripción)
        orden_leyenda = [
            ("I", "Punto de Inicio"),
            ("F", "Punto Final"),
            ("*", "Camino Encontrado"),
            (".", "Terreno Fácil (Coste 1, 1 Turno)"),
            ("▒", "Terreno Difícil (Coste 5, Riesgo)"),
            ("~", "Río (Coste 3, 10 Turnos)"),
            ("R", "Recurso (Coste -5, 1 Turno)"),
            ("█", "Muro (Sin Acceso)")
        ]

        # Iterar y crear la leyenda usando
        for i, (char, text) in enumerate(orden_leyenda):
            # Obtener la imagen que ya cargamos en __init__
            img = self.imagenes_terreno.get(char)
            if img:
                # Label para la imagen
                img_label = ttk.Label(frame_leyenda, image=img)
                img_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                # Label para el texto
                text_label = ttk.Label(frame_leyenda, text=text, font=("Arial", 10))
                text_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        # Botón para cerrar la leyenda
        btn_cerrar = ttk.Button(frame_leyenda, text="Cerrar", command=legend_window.destroy)
        btn_cerrar.grid(row=len(orden_leyenda), column=0, columnspan=2, pady=(15, 0))

    def mostrar_acerca_de(self):
        messagebox.showinfo(
            "Acerca de este Simulador",
            "Simulador de Algoritmo A* (Multiobjetivo)\n\n"
            "Proyecto para la asignatura 'Sistemas Inteligentes'.\n"
            "Desarrollado por: Derick Daumienebi Sakpa\n"
            "Tutor : Jose Alberto"
        )

    def cargar_imagenes(self):
        """Carga, redimensiona y almacena todas las imágenes del terreno."""
        print(f"Cargando imágenes (tamaño {self.tamanho_celda}x{self.tamanho_celda})...")
        # Mapeo de caracteres del tablero visual a nombres de archivo
        nombres_imagenes = {
            ".": "terreno_facil.jpg",
            "▒": "tree.png",
            "~": "rio.jpg",
            "█": "sin_acceso.jpg",
            "R": "recurso.jpg",
            "I": "inicio.png",
            "F": "fin.jpg",
        }
        for char, nombre_archivo in nombres_imagenes.items():
            ruta = os.path.join(project_root, "resources", nombre_archivo)
            try:
                img_pil = Image.open(ruta)
                # Reducir la imagen con ALTA CALIDAD (LANCZOS)
                img_pil = img_pil.resize((self.tamanho_celda, self.tamanho_celda), Image.Resampling.LANCZOS)
                # Convertir la  imagen para que sirva para Tkinter
                self.imagenes_terreno[char] = ImageTk.PhotoImage(img_pil)
            except Exception as e:
                print(f"Error al cargar imagen {nombre_archivo}: {e}")
                # Si falla, creamos una imagen de color de fallback
                img_por_defecto = Image.new("RGB", (self.tamanho_celda, self.tamanho_celda), "yellow")
                self.imagenes_terreno[char] = ImageTk.PhotoImage(img_por_defecto)

    def generar_y_dibujar_tablero(self):
        """Lee los valores, crea un nuevo Tablero y lo dibuja."""
        try:
            ancho = int(self.entry_ancho.get())
            alto = int(self.entry_alto.get())
            if ancho < 10 or alto < 10: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Alto y Ancho deben ser números enteros >= 10.")
            return
        self.status_label.config(text=f"Generando tablero de {ancho}x{alto}...")
        self.master.update_idletasks()
        # Creamos el Tablero
        self.mi_tablero = Tablero(alto=alto, ancho=ancho)
        # Resetear puntos de inicio/fin en el caso de que se hayan modificado previamente
        self.punto_inicio = (0, 0)
        self.punto_fin = (ancho - 1, alto - 1)

        # Obtener la visualización (con I y F, pero sin camino)
        visual = self.mi_tablero.generar_visualizacion_camino(
            camino=[],
            inicio=self.punto_inicio,
            fin=self.punto_fin
        )
        self.dibujar_tablero(visual)
        self.status_label.config(text=f"Tablero de {ancho}x{alto} generado. Listo para buscar ruta.")
        # Resetea el label de resultados
        self.results_label.config(text="Resultados: (Elige puntos y busca una ruta)")

    def buscar_y_dibujar_ruta(self):
        if not self.mi_tablero:
            messagebox.showwarning("Aviso", "Primero debes generar un tablero.")
            return

        # Validar que los puntos son transitables
        if not self.mi_tablero.es_transitable(*self.punto_inicio) or \
                not self.mi_tablero.es_transitable(*self.punto_fin):
            messagebox.showerror("Error", "El punto de inicio o fin está en un muro. Elige nuevos puntos.")
            return
        self.status_label.config(text="Buscando ruta... (puede tardar)")
        self.master.update_idletasks()
        # Ejecutar nuestro algoritmo usando los puntos guardados
        camino, coste, tropas, tiempo = buscar_ruta(
            self.mi_tablero,
            self.punto_inicio,
            self.punto_fin
        )
        # Obtener la visualización con el camino
        visual = self.mi_tablero.generar_visualizacion_camino(
            camino=camino,
            inicio=self.punto_inicio,
            fin=self.punto_fin
        )

        # 3. Redibujar
        self.dibujar_tablero(visual)

        if camino:
            self.results_label.config(
                text=f"Coste: {coste} | Tropas: {tropas}/{TROPAS_INICIALES} | Tiempo: {tiempo} turnos"
            )
            self.status_label.config(
                text=f"¡Ruta encontrada!")
        else:
            self.status_label.config(text="No se pudo encontrar una ruta.")

    def dibujar_tablero(self, tablero_visual):
        """Dibuja la lista de listas en el Canvas usando IMÁGENES y BORDES."""
        self.canvas_tablero.delete("all")
        if not self.mi_tablero: return

        ancho_tablero_px = self.mi_tablero.ancho * self.tamanho_celda
        alto_tablero_px = self.mi_tablero.alto * self.tamanho_celda
        self.canvas_tablero.config(scrollregion=(0, 0, ancho_tablero_px, alto_tablero_px))

        for y, fila in enumerate(tablero_visual):
            for x, char_visual in enumerate(fila):
                x0 = x * self.tamanho_celda
                y0 = y * self.tamanho_celda
                x1 = x0 + self.tamanho_celda
                y1 = y0 + self.tamanho_celda
                # 1. Determinar el terreno base
                char_terreno = char_visual
                if char_visual in ("*", "I", "F"):
                    # Si es un overlay, preguntar al tablero qué terreno hay debajo
                    coste = self.mi_tablero.get_coste(x, y)
                    if coste == TERRENO_FACIL:
                        char_terreno = "."
                    elif coste == TERRENO_DIFICIL:
                        char_terreno = "▒"
                    elif coste == TERRENO_RIO:
                        char_terreno = "~"
                    elif coste == RECURSO:
                        char_terreno = "R"
                    elif coste == SIN_ACCESO:
                        char_terreno = "█"

                # 2. Dibujar la IMAGEN del terreno base
                imagen_terreno = self.imagenes_terreno.get(char_terreno)
                if imagen_terreno:
                    self.canvas_tablero.create_image(x0, y0, image=imagen_terreno, anchor="nw")
                # Dibujar el "overlay" (Imagen de Inicio/Fin o Borde de Camino)
                if char_visual == "*":
                    # dibujar el BORDE
                    self.canvas_tablero.create_rectangle(x0, y0, x1, y1,outline="goldenrod1",width=4)
                elif char_visual in ("I", "F"):
                    # Es Inicio o Fin: dibujar la IMAGEN
                    imagen_overlay = self.imagenes_terreno.get(char_visual)
                    if imagen_overlay:
                        self.canvas_tablero.create_image(x0, y0, image=imagen_overlay, anchor="nw")
                elif char_visual == "█":
                    # Es un muro, asegurarnos de que se dibuja (si no lo hizo ya la capa base)
                    # Esto es un seguro en caso de que "I" o "F" estuvieran en un muro
                    imagen_muro = self.imagenes_terreno.get("█")
                    if imagen_muro:
                        self.canvas_tablero.create_image(x0, y0, image=imagen_muro, anchor="nw")

    # Seleccionar una casilla de inicio
    def activar_modo_inicio(self):
        """Activa el modo de selección para el punto de inicio."""
        self.modo_seleccion = "inicio"
        self.status_label.config(text="MODO SELECCIÓN: Haz clic en el tablero para elegir la casilla de INICIO.")

    def activar_modo_fin(self):
        """Activa el modo de selección para el punto final."""
        self.modo_seleccion = "fin"
        self.status_label.config(text="MODO SELECCIÓN: Haz clic en el tablero para elegir la casilla FINAL.")

    def on_canvas_click(self, event):
        """Manejador para cuando el usuario hace clic en el canvas."""
        if not self.mi_tablero: return  # No hacer nada si no hay tablero
        if not self.modo_seleccion: return  # No hacer nada si no estamos en "modo selección"

        # Convertir píxeles de clic a coordenadas de cuadrícula
        # Usamos canvas.canvasx/y para compensar el scroll
        columna = int(self.canvas_tablero.canvasx(event.x) // self.tamanho_celda)
        fila = int(self.canvas_tablero.canvasy(event.y) // self.tamanho_celda)

        # Asegurarse de que el clic está dentro del tablero
        if 0 <= columna < self.mi_tablero.ancho and 0 <= fila < self.mi_tablero.alto:
            nueva_coordenada = (columna, fila)
            # Validar que no sea un muro
            if not self.mi_tablero.es_transitable(columna, fila):
                self.status_label.config(text="¡No puedes colocar un punto en un muro!")
                self.modo_seleccion = None
                return
            if self.modo_seleccion == "inicio":
                self.punto_inicio = nueva_coordenada
                self.status_label.config(text=f"Nuevo inicio: {self.punto_inicio}. Elige Fin o Busca Ruta.")

            elif self.modo_seleccion == "fin":
                self.punto_fin = nueva_coordenada
                self.status_label.config(text=f"Nuevo fin: {self.punto_fin}. Listo para Buscar Ruta.")
            self.modo_seleccion = None  # Desactivar modo selección
            # Redibujar el tablero para mostrar el nuevo 'I' o 'F'
            self.redibujar_tablero_visual()

    def redibujar_tablero_visual(self):
        """Función auxiliar para redibujar sin regenerar el tablero."""
        if not self.mi_tablero: return

        # Genera la visualización con los puntos actualizados (aún sin camino)
        visual = self.mi_tablero.generar_visualizacion_camino(
            camino=[],
            inicio=self.punto_inicio,
            fin=self.punto_fin
        )
        self.dibujar_tablero(visual)

# --- MODO DE PRUEBA ---
if __name__ == "__main__":
    print("Iniciando GUI en modo de prueba (saltando pantalla de carga)...")
    root = tk.Tk()
    app = GUISimulacion(root)
    root.mainloop()
