import tkinter as tk
from gui.gui_pantalla_carga import PantallaCarga
from gui.gui_simulacion import GUISimulacion

if __name__ == "__main__":
    # Creamos la ventana principal y ocultamos immediatamente porque hay que mostrar la
    # pantalla de 'carga' falsa antes
    root = tk.Tk()
    root.withdraw()
    # Preparar la GUI principal (la ventana sigue oculta)
    app = GUISimulacion(root)
    # Lanzar la pantalla de carga.
    # Esta ventana se muestra y su temporizador 'after' se pone en la cola de eventos.
    splash = PantallaCarga(root)
    # Iniciar el ÚNICO bucle de eventos (mainloop).
    root.mainloop()