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
    Recorre la cadena de padres desde el nodo final hacia atrás para construir
    la ruta optima
    :param nodo_final:
    :return: Una lista con el camino y un valor int que indica el coste total
    """
    camino = []
    coste_total = nodo_final.g # El coste acumulado del nodo final es el coste de la ruta
    actual = nodo_final
    while actual: # Mientras no sea None, el nodo nodo inicial no tiene padare
        # Agregar el las posiciones actuales al camino
        camino.append((actual.x,actual.y))
        # Accedemos al padre del nodo actual para poder seguir retrocediendo en el camino
        actual = actual.padre

    # Invertimos el camino para tenerlo en el orden [inicio -> fin] ya que tras el paso anterior
    # se encuentra en el otden [fin - inicio] y lo devolvemos con el coste total
    return camino[::-1], coste_total


def encontrar_ruta(tablero:Tablero, inicio:tuple, fin:tuple):
    """
        Implementacion del algoritmo, aqui se intenta encontrar la ruta de coste
        minimo entre dos puntos.

        :param tablero:El tablero o mapa sobre el que se quiere
        :param inicio: La tupla (x,y) que indica el punto de partida
        :param fin: La tupla que (x,y) que indica el punto final
        :return: una tupla de (camino,coste_total) si lo encuentra y ([],0) si no.
    """
    # Inicializamos los nodos
    nodo_inicio = Nodo(inicio[0],inicio[1])
    nodo_final = Nodo(fin[0],fin[1])

    # Creamos la cola de prioridad para almacenar los nodos abiertos pero
    # sin evaluar. Utilizando heapq, siempre podremos obtener el nodo con la 'f' mas bajo
    lista_abiertos = []
    heapq.heappush(lista_abiertos,nodo_inicio)
    # Ahora necesitamos otra estructura para almacenar los nodos cerrados
    # Estos son los elementos que ya hemos evaluado
    lista_cerrados = set()
    # Costes iniciales del nodo de inicio
    nodo_inicio.g = 0
    nodo_inicio.h = calcular_heuristica(nodo_inicio,nodo_final)
    nodo_inicio.f = nodo_inicio.g + nodo_inicio.h

    # Bucle del A* que se ejecuta mientras haya nodos por explorar en la lista de abiertos
    while lista_abiertos:
        # Obtenemos el nodo con el menor f de nuestra cola de prioridad
        nodo_actual = heapq.heappop(lista_abiertos)
        # Comprobamos si ha se ha explorado este nodo, si es el caso, significa que
        # hemos encontrado uno mas barato anteriormente
        if(nodo_actual.x,nodo_actual.y) in  lista_cerrados:
            continue
        # Agregar la posicion actual a la lista cerrada ya que se acaba de visitar
        lista_cerrados.add((nodo_actual.x,nodo_actual.y))

        # Comprobamos si hemos llegado al destino
        if nodo_actual == nodo_final:
            return  reconstruir_camino(nodo_actual)

        #Explorar los vecinos
        posibles_movimientos = [(0,1),(0,-1),(-1,0),(1,0)] # arriba,abajo,izq,der
        for mov_x, mov_y in posibles_movimientos:
            vecino_x = nodo_actual.x + mov_x
            vecino_y = nodo_actual.y + mov_y

            if not tablero.es_transitable(vecino_x,vecino_y):
                continue

            vecino = Nodo(vecino_x,vecino_y,padre=nodo_actual)
            # Calculamos los costes del vecino
            coste_vecino = tablero.get_coste(vecino.x,vecino.y)
            # Actualizar el valor de g
            nuevo_g = nodo_actual.g + coste_vecino
            # En caso de que el vecino tenga un coste menor, nuestra cola de prioridad
            # ya se encargará se sacar la que tenga el f mas bajo primero.
            # Gracias a tener el metodo __lt__ definido en cada nodo, la cola de prioridad
            # podra comparar todos los nodos por su f y ordenarlos
            vecino.g = nuevo_g
            vecino.h = calcular_heuristica(vecino,nodo_final)
            vecino.f = vecino.g + vecino.h
            # Agregar el vecino a la cola de prioridad para explorarlo
            heapq.heappush(lista_abiertos,vecino)


    # En el caso de que se haya recorrido todos los elementos de lista_abiertos y
    # no encontremos el final, no se ha encontrado una ruta
    return [],0