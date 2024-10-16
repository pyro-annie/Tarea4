import os
from colorama import Fore, Style, init

init()

def limpiar_consola():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def crear_tablero():
    return [['O' for _ in range(10)] for _ in range(10)]

def mostrar_tablero(tablero):
    letras_columna = "ABCDEFGHIJ"
    print("  " + " ".join(letras_columna))
    for indice, fila in enumerate(tablero):
        fila_color = []
        for celda in fila:
            if celda == 'O':
                fila_color.append(Fore.BLUE + celda + Style.RESET_ALL)
            elif celda == 'X':
                fila_color.append(Fore.CYAN + celda + Style.RESET_ALL)
            elif celda == 'T':
                fila_color.append(Fore.RED + celda + Style.RESET_ALL)
            else:
                fila_color.append(celda)
        print(f"{indice} " + " ".join(fila_color))
    print()

def validar_entrada(prompt, validacion, error_msg="Entrada inválida. Intenta de nuevo."):
    while True:
        entrada = input(prompt)
        if validacion(entrada):
            return entrada
        print(error_msg)

def posicionar_barcos_manualmente(tablero, barcos):
    letras_columna = "ABCDEFGHIJ"
    for nombre, tamaño in sorted(barcos.items(), key=lambda item: item[1]):
        colocado = False
        while not colocado:
            print(f"Coloca tu {nombre} (tamaño {tamaño})")
            mostrar_tablero(tablero)
            orientacion = validar_entrada("Elija la orientación (H para horizontal, V para vertical): ", lambda x: x.upper() in ['H', 'V']).upper()
            fila = int(validar_entrada("Introduce la fila (0-9): ", lambda x: x.isdigit() and 0 <= int(x) < 10))
            columna_letra = validar_entrada("Introduce la columna (A-J): ", lambda x: x.upper() in letras_columna).upper()
            columna = letras_columna.index(columna_letra)
            if orientacion == 'H':
                if columna + tamaño <= 10 and all(tablero[fila][col] == 'O' for col in range(columna, columna + tamaño)):
                    for col in range(columna, columna + tamaño):
                        tablero[fila][col] = nombre[0]
                    colocado = True
                else:
                    print("¡Posición no válida! Intenta de nuevo.")
            else:
                if fila + tamaño <= 10 and all(tablero[fila + f][columna] == 'O' for f in range(tamaño)):
                    for f in range(tamaño):
                        tablero[fila + f][columna] = nombre[0]
                    colocado = True
                else:
                    print("¡Posición no válida! Intenta de nuevo.")
        mostrar_tablero(tablero)

def disparar(tablero_enemigo, fila, columna):
    if tablero_enemigo[fila][columna] == 'O':
        tablero_enemigo[fila][columna] = 'X'
        print("¡Agua!")
        return False
    elif tablero_enemigo[fila][columna] in ['X', 'T']:
        print("Ya has disparado en esta posición.")
        return False
    else:
        barco = tablero_enemigo[fila][columna]
        tablero_enemigo[fila][columna] = 'T'
        if not any(celda == barco for fila in tablero_enemigo for celda en fila):
            print(f"¡Hundiste un barco ({barco})!")
        else:
            print("¡Impacto!")
        return True

def todas_naves_hundidas(tablero):
    return all(celda in ['O', 'X', 'T'] for fila in tablero for celda en fila)

def jugar_turno(nombre_jugador, tablero_enemigo):
    print(f"Turno de {nombre_jugador}.")
    letras_columna = "ABCDEFGHIJ"
    while True:
        try:
            fila = int(validar_entrada("Introduce la fila (0-9): ", lambda x: x.isdigit() and 0 <= int(x) < 10))
            columna_letra = validar_entrada("Introduce la columna (A-J): ", lambda x: x.upper() in letras_columna).upper()
            columna = letras_columna.index(columna_letra)
            return disparar(tablero_enemigo, fila, columna)
        except ValueError:
            print("Entrada inválida. Por favor, introduce números enteros para la fila y letras para la columna.")

def mostrar_reglas():
    print("Bienvenido a la Batalla Naval!")
    print("Reglas del juego:")
    print("1. El objetivo es hundir los 9 barcos de tu oponente antes que él hunda los tuyos.")
    print("2. Los barcos disponibles son:\n   - 1 Portaaviones (4 casillas)\n   - 2 Acorazados (3 casillas cada uno)\n   - 2 Submarinos (3 casillas cada uno)\n   - 2 Destructores (2 casillas cada uno)\n   - 2 Fragatas (1 casilla cada una)\n")
    while True:
        ready = input("¿Listo para convertirte en un marine? Presiona Enter para continuar...\n")
        if ready == "":
            break
        print("Por favor, presiona Enter para continuar...")

def jugar():
    mostrar_reglas()
    barcos = {
        "Fragata1": 1,
        "Fragata2": 1,
        "Destructor1": 2,
        "Destructor2": 2,
        "Submarino1": 3,
        "Submarino2": 3,
        "Acorazado1": 3,
        "Acorazado2": 3,
        "Portaaviones": 4
    }
    tablero_jugador1 = crear_tablero()
    tablero_jugador2 = crear_tablero()
    print("Jugador 1, coloca tus barcos:")
    posicionar_barcos_manualmente(tablero_jugador1, barcos)
    input("¿Listo Jugador 2? Presiona Enter para continuar...\n")
    limpiar_consola()
    print("Jugador 2, coloca tus barcos:")
    posicionar_barcos_manualmente(tablero_jugador2, barcos)
    input("¿Listo Jugador 1? Presiona Enter para continuar...\n")
    limpiar_consola()
    jugadores = [("Jugador 1", tablero_jugador1), ("Jugador 2", tablero_jugador2)]
    turno = 0
    while True:
        limpiar_consola()
        nombre_jugador, tablero_propio = jugadores[turno]
        nombre_oponente, tablero_oponente = jugadores[1 - turno]
        input(f"\n¿Listo {nombre_jugador}? Presiona Enter para ver tu tablero...\n")
        mostrar_tablero(tablero_propio)
        jugar_turno(nombre_jugador, tablero_oponente)
        if todas_naves_hundidas(tablero_oponente):
            print(f"¡Felicidades {nombre_jugador}! Has ganado. Hundiste todas las naves de {nombre_oponente}.")
            break
        turno = 1 - turno

if __name__ == "__main__":
    while True:
        jugar()
        respuesta = validar_entrada("¿Quieres volver a jugar? (S/N): ", lambda x: x.upper() in ['S', 'N']).upper()
        if respuesta != 'S':
            break
        limpiar_consola()
