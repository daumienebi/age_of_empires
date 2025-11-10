#https://stackoverflow.com/questions/56723852/console-select-menu-in-python
tablero = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1],
]

def mostrar_menu_inicial():
    print("BIENVENIDO AL JUEGO: \n")
    print("La idea del juego es mover un conjunto de 4 soldados a una determinada posición a través de la ruta mas eficaz")

    while True:
        print("1. Jugar")
        print("2. Detalles")
        print("3. Ayuda")
        print("0. Salir")
        opcion = int(input("Introduce una opción : \n"))
        match opcion:
            case 1: print("Opcion 1")
            case 2: print("Opcion 2")
            case 3: print("Opcion 3")
            case 0: break

def mostrar_tablero():
    print(tablero)


mostrar_menu_inicial()
