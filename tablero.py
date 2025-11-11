import random

#Definir los valores de los costes
TERRENO_FACIL = 1
TERRENO_DIFICIL = 10
SIN_ACCESO = 9999
RECURSO = -5

class Tablero:
    def __init__(self,alto : int,ancho:int):
        self.alto = max(10,alto)
        self.ancho = max(10,ancho)
        self.mi_tablero = []

    def _generar_mapa(self):
        """
        Primer intento de generar un tablero simple
        :return:
        """
        #self.mi_tablero = [[TERRENO_FACIL for _ in range(self.ancho)] for _ in range(self.alto)]
        for x in range(self.alto):
            fila_nueva = []
            for y in range(self.ancho):
                # Rellenamos de terrenos faciles
                fila_nueva.append(TERRENO_FACIL)
            # Agregamos cada fila al tablero
            self.mi_tablero.append(fila_nueva)
        # Agregamos más detalles al tablero con los terrnos dificiles etc
        for x in range(self.alto):
            for y in range(self.ancho):
                if random.random() < 0.15:
                    self.mi_tablero[x][y] = TERRENO_DIFICIL
                if random.random() < 0.5:
                    self.mi_tablero[x][y] = SIN_ACCESO
                if random.random() < 0.03:
                    self.mi_tablero[x][y] = RECURSO
        #los del inicio y final tienen que ser terreno facil
        self.mi_tablero[0][0] = TERRENO_FACIL
        self.mi_tablero[self.alto - 1][self.ancho - 1] = TERRENO_FACIL

    def get_coste(self,x: int, y:int):
        """
        Funcion para obtener el coste
        :param x: Posicion x
        :param y: Posicion y
        :return:
        """
        if not self.esta_en_limites(x,y):
            return SIN_ACCESO
        return self.mi_tablero[x][y]

    def es_transitable(self,x:int, y:int):
        """
        Comprobar si una casilla se encuentra bloqueada o no
        :param x:
        :param y:
        :return:
        """
        if self.get_coste(x,y) < SIN_ACCESO:
            return True
        return False

    def esta_en_limites(self,x:int,y:int):
        """
        Funcion para comprobar si la coordenada se encuentra dentro del mapa
        :param x:
        :param y:
        :return:
        """
        return (0 <= self.ancho < x) and (0 <= self.alto < y)

    def imprimir_camino(self,camino:list):
        """
        Imprimir el camino encontrado en el tablero
        :param camino:
        :return:
        """
        #TO-DO