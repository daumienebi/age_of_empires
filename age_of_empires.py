import time
from tablero import Tablero
from a_estrella import buscar_ruta, TROPAS_INICIALES

# Pedir las medidas del tablero / mapa al usuario
try:
    ANCHO_TABLERO = int(input("Introduce el ancho del tablero :"))
    ALTO_TABLERO = int(input("Introduce el alto del tablero :"))
except ValueError:
    print("Entrada no válida, se utilizará el tamaño [32x32] por defecto.")
    ANCHO_TABLERO = 32
    ALTO_TABLERO = 32

# Creación del Tablero ---
mi_tablero = Tablero(ancho=ANCHO_TABLERO, alto=ALTO_TABLERO)

print(mi_tablero.__repr__())

# Definición de Inicio y Fin ---
punto_inicio = (0, 0)
punto_fin = (mi_tablero.ancho - 1, mi_tablero.alto - 1)

print(f"\nBuscando la ruta más económica desde {punto_inicio} hasta {punto_fin}...")

# Ejecución del Algoritmo A* ---
start_time = time.time()  # Guardamos la hora de inicio

camino,coste_total,tropas_finales,tiempo_total = buscar_ruta(mi_tablero, punto_inicio, punto_fin)

end_time = time.time()  # Guardamos la hora de fin

# Muestra de Resultados ---
if camino:
    # Si la lista 'camino_encontrado' no está vacía, encontramos una ruta
    print(f"Ruta encontrada en {end_time - start_time:.4f} segundos.")
    print(f"Coste total de la ruta: {coste_total}")
    print(f"Tropas restantes: {tropas_finales} / {TROPAS_INICIALES}")
    print(f"Tiempo total: {tiempo_total}")
    print(f"Pasos en la ruta: {len(camino)}")

    # Imprimir el mapa visual
    mi_tablero.mostrar_camino(camino)
else:
    # Si la lista está vacía, no se encontró ruta
    print(f"No se encontró ruta en {end_time - start_time:.4f} segundos.")
    mi_tablero.mostrar_camino([])  # Imprimir el mapa sin ruta