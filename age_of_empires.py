import time
from tablero import Tablero
from a_estrella import encontrar_ruta, TROPAS_INICIALES

# Pedir las medidas del tablero al usuario
try:
    ANCHO_TABLERO = int(input("Introduce el ancho del tablero (ej. 32): "))
    ALTO_TABLERO = int(input("Introduce el alto del tablero (ej. 32): "))
except ValueError:
    print("Entrada no válida, usando 32x32 por defecto.")
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

camino_encontrado, coste_total,tropas_finales = encontrar_ruta(mi_tablero, punto_inicio, punto_fin)

end_time = time.time()  # Guardamos la hora de fin

# Muestra de Resultados ---
if camino_encontrado:
    # Si la lista 'camino_encontrado' no está vacía, encontramos una ruta
    print(f"Ruta encontrada en {end_time - start_time:.4f} segundos.")
    print(f"Coste total de la ruta: {coste_total}")
    print(f"Tropas restantes: {tropas_finales} / {TROPAS_INICIALES}")
    print(f"Pasos en la ruta: {len(camino_encontrado)}")

    # Imprimir el mapa visual
    mi_tablero.mostrar_camino(camino_encontrado)
else:
    # Si la lista está vacía, no se encontró ruta
    print(f"No se encontró ruta en {end_time - start_time:.4f} segundos.")
    mi_tablero.mostrar_camino([])  # Imprimir el mapa sin ruta