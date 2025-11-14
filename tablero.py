import random

#Definir los valores de los costes
TERRENO_FACIL = 1
TERRENO_DIFICIL = 7
TERRENO_RIO = 5
SIN_ACCESO = 9999
RECURSO = -10

class Tablero:
    def __init__(self,alto : int,ancho:int):
        self.alto = max(10,alto)
        self.ancho = max(10,ancho)
        self.mi_tablero = []
        # Otro "tablero" para indicar el riesgo de perder nuestras tropas en sus casillas
        self.riesgo = [[0 for _ in range(self.ancho)] for _ in range(self.alto)]
        # Otro "tablero" para indicar el coste de tiempo en cada casilla (indica cuantos turnos se pierden)
        self.coste_turno = [[1 for _ in range(self.ancho)] for _ in range(self.alto)]
        self._generar_tablero()

    def _generar_tablero(self):
        """
            Generar el tablero del juego para nuestros soldados
        """
        self.mi_tablero = [[TERRENO_FACIL for _ in range(self.ancho)] for _ in range(self.alto)]
        # Agregamos más detalles al tablero con los terrnos dificiles etc
        for y in range(self.alto):
            for x in range(self.ancho):
                if random.random() < 0.20:
                    self.mi_tablero[y][x] = TERRENO_DIFICIL
                    # Calcular el riesgo de perder tropas en los terrenos dificiles
                    if random.random() < 0.7:
                        self.riesgo[y][x] = 1 # Se perderia una tropa
                elif random.random() < 0.20:
                    self.mi_tablero[y][x] = SIN_ACCESO
                elif random.random() < 0.05:
                    self.mi_tablero[y][x] = RECURSO
                elif random.random() < 0.30:
                    self.mi_tablero[y][x] = TERRENO_RIO
                    # Indicamos el coste del rio
                    self.coste_turno[y][x] = 10
        #los del inicio y final tienen que ser terreno facil y sin costar tiempo extra
        self.mi_tablero[0][0] = TERRENO_FACIL
        self.mi_tablero[self.alto - 1][self.ancho - 1] = TERRENO_FACIL
        self.coste_turno[0][0] = 1
        self.coste_turno[self.alto - 1][0] = 1

    def get_riesgo(self,x:int, y:int):
        """
            Funcion para obtener el numero de tropas que se perderia en la casilla (x,y)
            :param x:
            :param y:
            :return: El riesgo de la casilla, devuelve 1 si hay riesgo y 0 si no
        """
        # Comprobamos si la posicion se encuentra en los limites
        if not self.esta_en_limites(x,y):
            return 0
        return self.riesgo[y][x]

    def get_coste_turno(self, x:int, y:int):
        """
            Obtener el numero de turnos que cuesta pasar por la casilla (x,y)
            :param x:
            :param y:
            :return: El coste del turno de la casilla en cuestion (fila,columna)
        """
        if not self.esta_en_limites(x,y):
            return 1 # Valor por defecto
        return self.coste_turno[y][x]

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

    def generar_visualizacion_camino(self, camino: list, inicio: tuple = None, fin: tuple = None) -> list:
        """
        Genera la lista de listas para la visualización del camino.
        Esta es la función CLAVE que usa la GUI.

        Si 'camino' está vacío, usará 'inicio' y 'fin' (si se proveen)
        para dibujar solo los marcadores.
        """
        # Crear tablero base con terreno
        tablero_visual = [["." for _ in range(self.ancho)] for _ in range(self.alto)]
        for y in range(self.alto):
            for x in range(self.ancho):
                coste = self.get_coste(x, y)
                if coste == SIN_ACCESO:
                    tablero_visual[y][x] = "M"
                elif coste == TERRENO_DIFICIL:
                    tablero_visual[y][x] = "D"
                elif coste == TERRENO_RIO:
                    tablero_visual[y][x] = "~"
                elif coste == RECURSO:
                    tablero_visual[y][x] = "R"
                else:  # Incluye TERRENO_FACIL
                    tablero_visual[y][x] = "."
        # Determinar puntos de Inicio y Fin
        inicio_pos, fin_pos = None, None

        if camino:
            # Si hay un camino, los puntos vienen de él
            inicio_pos = camino[0]
            fin_pos = camino[-1]
            # Dibujar el camino '*'
            for x, y in camino:
                if (x, y) != inicio_pos and (x, y) != fin_pos:
                    tablero_visual[y][x] = "*"
        elif inicio and fin:
            # Si no hay camino PERO se dieron puntos, lo usamos
            inicio_pos = inicio
            fin_pos = fin

        # Dibujar Inicio y Fin (si existen)
        if inicio_pos and fin_pos:
            try:
                # Asegurarse de que los puntos están en el mapa
                if self.esta_en_limites(inicio_pos[0], inicio_pos[1]):
                    tablero_visual[inicio_pos[1]][inicio_pos[0]] = "I"
                if self.esta_en_limites(fin_pos[0], fin_pos[1]):
                    tablero_visual[fin_pos[1]][fin_pos[0]] = "F"
            except IndexError:
                print("Error: Coordenadas de inicio/fin fuera de rango al dibujar.")

        return tablero_visual

    def mostrar_camino(self, camino: list):
        """Genera e imprime la visualización del camino."""
        tablero_visual = self.generar_visualizacion_camino(camino)
        print("\n--- Visualización del camino ---")
        for fila in tablero_visual:
            print(" ".join(fila))
        print("-----------------------------------")
        print("Leyenda: I=Inicio, F=Fin, *=Camino, R=Recurso, D=Difícil, M=Sin Acceso, ~=Rio .=Fácil,")