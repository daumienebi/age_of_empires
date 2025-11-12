from tkinter import *
# https://www.geeksforgeeks.org/python/what-are-widgets-in-tkinter/
# https://www.geeksforgeeks.org/python/python-grid-method-in-tkinter/
# http://recursospython.com/guias-y-manuales/barra-de-progreso-progressbar-tcltk-tkinter/

class AgeOfEmpiresGUI(Frame):
    def __init__(self,ventana):
        super().__init__(ventana)
        ventana.title("Age of Empires")
        ventana.geometry("720x500")
        ventana.resizable(False,False)

ventana_principal = Tk()
app = AgeOfEmpiresGUI(ventana_principal)
app.mainloop()



