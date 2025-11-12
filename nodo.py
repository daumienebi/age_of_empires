
class Nodo:
    """
    Clase que nos sirve para almacenar un estado de la busqueda del algoritmo A*,
    contiene las posiciones (x,y), el coste real (g), la heuristica (h) y f (g+h)
    """
    def __init__(self,x:int,y:int,padre = None):
        self.x = x
        self.y = y
        self.padre = padre
        self.g = 0 # El coste real
        self.h = 0 # La heuristica
        self.f = 0 # g+h
        self.tropas = 0 # Numero de tropas al llegar a este nodo
        self.tiempo = 0 # Tiempo total hasta llegar a ese nodo

    def __eq__(self, otro_nodo):
        """
        Comprobar si dos nodos representan la misma casilla en el tablero
        :param __value:
        :return:
        """
        return isinstance(otro_nodo, Nodo) and self.x == otro_nodo.x and self.y == otro_nodo.y

    def __lt__(self, otro_nodo):
        """
        Comparar si un nodo es menor que otro dado que en la cola de prioridad
        tenemos que ordenarlos de menor a mayor
        :param otro_nodo:
        :return:
        """
        return self.f < otro_nodo.f

    def __repr__(self):
        """
        Función para mostrar los detalles del nodo
        :return:
        """
        return f"Nodo({self.x}, {self.y}, - f:{self.f})"

    def __hash__(self):
        return hash((self.x,self.y))
