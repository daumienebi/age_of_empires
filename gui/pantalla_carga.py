import tkinter as tk
from tkinter import ttk


class PantallaCarga(ttk.Frame):

    def __init__(self, ventana):
        super().__init__(ventana)
        ventana.title("Barra de progreso en Tk")
        self.progressbar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=160)
        self.progressbar.place(x=30, y=30)
        self.place(width=300, height=200)
        ventana.geometry("500x300")
        ventana.resizable(False, False)
        # Mostrar la barra de progreso completa.
        for progreso in range(0,100):
            progreso = tk.IntVar()
            progreso.set(progreso)
            self.progressbar.step(progreso)

main_window = tk.Tk()
app = PantallaCarga(main_window)
app.mainloop()