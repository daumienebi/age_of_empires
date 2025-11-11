import random

#Definir los valores de los costes
TERRENO_FACIL = 1
TERRENO_DIFICIL = 5
SIN_ACCESO = 9999
RECURSO = -5

class Tablero:
    def __init__(self,alto : int,ancho:int):
        self.alto = max(10,alto)
        self.ancho = max(10,ancho)
        self.mi_tablero = []
        self._generar_mapa()

    def _generar_mapa(self):
        """
            Primer intento de generar un tablero simple
            :return:
        """
        self.mi_tablero = [[TERRENO_FACIL for _ in range(self.ancho)] for _ in range(self.alto)]
        """
        for x in range(self.alto):
            fila_nueva = []
            for y in range(self.ancho):
                # Rellenamos de terrenos faciles
                fila_nueva.append(TERRENO_FACIL)
            # Agregamos cada fila al tablero
            self.mi_tablero.append(fila_nueva)
        """
        # Agregamos más detalles al tablero con los terrnos dificiles etc
        for y in range(self.alto):
            for x in range(self.ancho):
                if random.random() < 0.15:
                    self.mi_tablero[y][x] = TERRENO_DIFICIL
                elif random.random() < 0.05:
                    self.mi_tablero[y][x] = SIN_ACCESO
                elif random.random() < 0.03:
                    self.mi_tablero[y][x] = RECURSO
        #los del inicio y final tienen que ser terreno facil
        self.mi_tablero[0][0] = TERRENO_FACIL
        self.mi_tablero[self.alto - 1][self.ancho - 1] = TERRENO_FACIL

    def __repr__(self):
        repr = ""
        # "y" = alto (filas) y "x" = ancho (columnas)
        for y in range(self.alto):
            for x in range(self.ancho):
                repr += str(self.mi_tablero[y][x]) + "\t"
            repr+="\n"
        return repr

    def get_coste(self,x: int, y:int):
        """
        Funcion para obtener el coste
        :param x: Posicion x
        :param y: Posicion y
        :return:
        """
        if not self.esta_en_limites(x,y):
            return SIN_ACCESO
        return self.mi_tablero[y][x]

    def es_transitable(self,x:int, y:int):
        """
        Comprobar si una casilla se encuentra bloqueada o no
        :param x:
        :param y:
        :return:
        """
        return self.get_coste(x,y) < SIN_ACCESO

    def esta_en_limites(self,x:int,y:int):
        """
            Comprueba si la coordenada se encuentra dentro del mapa
            :param x:
            :param y:
            :return:
        """
        return (0 <= x < self.ancho) and (0 <= y < self.alto)

    def mostrar_camino(self,camino:list):
        """
        Mostrar el camino encontrado en el tablero
        :param camino:
        :return:
        """
        # Defino el tablero inicial a mostrar por comprension
        tablero_visual = [["-" for _ in range(self.ancho)] for _ in range(self.alto)]
        for y in range(self.alto): # filas (alto)
            for x in range(self.ancho): # columnas (ancho)
                coste = self.get_coste(x,y)
                if coste == SIN_ACCESO:ds
                    tablero_visual[y][x] = "█"
                elif coste == TERRENO_DIFICIL:
                    tablero_visual[y][x] = "▒"
                elif coste == RECURSO:
                    tablero_visual[y][x] = "R"
                elif coste == TERRENO_FACIL:
                    tablero_visual[y][x] = "."
                else: tablero_visual[y][x] = "?"

        if camino:
            for x,y in camino:
                if (x,y) != camino[0] and (x,y) != camino[-1]:
                    tablero_visual[y][x] = "*"
                inicio_x,inicio_y = camino[0]
                fin_x,fin_y = camino[-1]
                # Indicar posiciones iniciales y finales
                tablero_visual[inicio_y][inicio_x] = "I"
                tablero_visual[fin_y][fin_x] = "F"
        #Finalmente mostrar el camino
        print("\n--- Visualización del camino ---")
        for fila in tablero_visual:
            print(" ".join(fila))
        print("-----------------------------------")