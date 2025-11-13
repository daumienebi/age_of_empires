import tkinter as tk
from gui.pantalla_carga import PantallaCarga
from gui.age_of_empires_gui import AgeOfEmpiresGUI

if __name__ == "__main__":
    # Crear la ventana principal y ocultarlo immediatamente
    root = tk.Tk()
    root.withdraw()
    # Preparar la GUI principal (la ventana sigue oculta)
    # Hacemos esto ANTES de la splash, para que la "carga"
    # real de la GUI ocurra durante la simulación de carga.
    app = AgeOfEmpiresGUI(root)

    # Lanzar la pantalla de carga.
    # Esta ventana se muestra y su temporizador 'after' se pone en la cola de eventos.
    splash = PantallaCarga(root)
    # Iniciar el ÚNICO bucle de eventos (mainloop).
    # Esto permite que el temporizador 'after' de la
    # pantalla de carga se ejecute con normalidad.
    root.mainloop()