from tablero import Tablero
from nodo import Nodo
import heapq

def calcular_heuristica(nodo_actual:Nodo,nodo_final:Nodo):
    """
    Calcula el coste estimando entre dos nodos utilizando la distancia de
    manhattan. h = |x0 - x1| + |y0 - y1|
    :param nodo_actual:
    :param nodo_final:
    :return:
    """
    return abs(nodo_actual.x - nodo_final.x) + abs(nodo_actual.y - nodo_final.y)

def reconstruir_camino(nodo_final:Nodo) -> (list, int):
    """
    :param nodo_final:
    :return: Una lista con el camino y un valor int que indica el coste total
    """
    camino = []
    coste_total = nodo_final.g # El coste acumulado del nodo final es el coste de la ruta
    actual = nodo_final
    while actual:
        # Agregar el las posiciones actuales al camino
        camino.append((actual.x,actual.y))
        # Accedemos al padre del nodo actual para poder seguir retrocediendo en el camino
        actual = actual.padre

    # Invertimos el camino para tenerlo en el orden [inicio -> fin] ya que tras el paso anterior
    # se encuentra en el otden [fin - inicio] y lo devolvemos con el coste total
    return camino[::-1], coste_total


def encontrar_ruta(tablero: Tablero, inicio: tuple, fin: tuple) -> (list, int):
    """
    Implementación del algoritmo A* (A Estrella).
    Encuentra la ruta de mínimo coste desde un punto de inicio a uno de fin.

    @param tablero: El objeto Tablero sobre el que buscar.
    @param inicio: Tupla (x, y) del punto de partida.
    @param fin: Tupla (x, y) del punto de destino.
    @return: Tupla (camino, coste) o ([], 0) si no se encuentra ruta.
    """

    # --- 1. Inicialización ---
    nodo_inicio = Nodo(inicio[0], inicio[1])
    nodo_fin = Nodo(fin[0], fin[1])

    # La 'Open List' (lista_abierta) es una COLA DE PRIORIDAD.
    # Contiene los nodos que hemos descubierto pero aún no hemos evaluado.
    # heapq nos garantiza que siempre sacaremos el nodo con el 'f' más bajo.
    lista_abierta = []
    heapq.heappush(lista_abierta, nodo_inicio)

    # La 'Closed List' (lista_cerrada) es un CONJUNTO (set).
    # Contiene las posiciones (x, y) de los nodos que YA hemos evaluado.
    # Usar un 'set' nos da búsquedas O(1) (casi instantáneas).
    lista_cerrada = set()

    # Calcular los costes iniciales del nodo de inicio
    nodo_inicio.g = 0
    nodo_inicio.h = calcular_heuristica(nodo_inicio, nodo_fin)
    nodo_inicio.f = nodo_inicio.g + nodo_inicio.h

    # --- 2. Bucle principal de A* ---
    # El bucle continúa mientras haya nodos por explorar en la lista abierta
    while lista_abierta:

        # Obtenemos el nodo con el MENOR coste 'f' de la cola de prioridad
        nodo_actual = heapq.heappop(lista_abierta)

        # Comprobamos si ya hemos procesado este nodo (su posición)
        # Esto es clave: si ya está en la lista cerrada, significa que
        # encontramos un camino *mejor* (más barato) a él en el pasado.
        if (nodo_actual.x, nodo_actual.y) in lista_cerrada:
            continue

        # Añadimos la posición actual a la lista cerrada (la "visitamos")
        lista_cerrada.add((nodo_actual.x, nodo_actual.y))

        # --- 3. Comprobar si hemos llegado al destino ---
        if nodo_actual == nodo_fin:
            print("¡Ruta encontrada!")
            # Si llegamos, reconstruimos el camino y lo devolvemos
            return reconstruir_camino(nodo_actual)

        # --- 4. Explorar vecinos (4 direcciones) ---
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Arriba, Abajo, Der, Izq

        for mov_x, mov_y in movimientos:
            vecino_x = nodo_actual.x + mov_x
            vecino_y = nodo_actual.y + mov_y

            # Si el vecino no es transitable (muro) o está fuera de límites, lo ignoramos
            if not tablero.es_transitable(vecino_x, vecino_y):
                continue

            # Creamos un nuevo objeto Nodo para el vecino
            vecino = Nodo(vecino_x, vecino_y, padre=nodo_actual)

            # --- 5. Calcular costes del vecino ---

            # Coste de moverse *desde* el nodo actual *hacia* el vecino
            coste_transito = tablero.get_coste(vecino.x, vecino.y)

            # El nuevo coste 'g' es el 'g' del padre + el coste de transitar
            nuevo_g = nodo_actual.g + coste_transito

            # Comprobación de optimización (no estrictamente necesaria
            # en esta implementación simple, pero es buena práctica):
            # Si ya hemos visto este vecino con un coste 'g' menor,
            # no lo volvemos a añadir. Pero nuestra lista cerrada ya
            # maneja la mayor parte de esto.

            vecino.g = nuevo_g
            vecino.h = calcular_heuristica(vecino, nodo_fin)
            vecino.f = vecino.g + vecino.h

            # Añadir el vecino a la lista abierta (cola de prioridad)
            # heapq lo colocará en la posición correcta según su coste 'f'
            heapq.heappush(lista_abierta, vecino)

    # Si la lista abierta se vacía y no encontramos el final, no hay ruta
    print("No se ha podido encontrar una ruta.")
    return [], 0

"""
def encontrar_ruta(tablero:Tablero, inicio:tuple, fin:tuple):
    
    Implementacion del algoritmo, aqui se intenta encontrar la ruta de coste
    minimo entre dos puntos.

    :param tablero:El tablero o mapa sobre el que se quiere
    :param inicio: La tupla (x,y) que indica el punto de partida
    :param fin: La tupla que (x,y) que indica el punto final
    :return:
    
"""