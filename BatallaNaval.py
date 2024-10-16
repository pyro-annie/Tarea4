import random
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

def posicionar_barcos(tablero, barcos):
    for nombre, tamaño in barcos.items():
        colocado = False
        while not colocado:
            orientacion = random.choice(['H', 'V'])
            fila = random.randint(0, 9)
            columna = random.randint(0, 9)
            if orientacion == 'H':
                if columna + tamaño <= 10:
                    espacio_libre = all(tablero[fila][col] == 'O' for col in range(columna, columna + tamaño))
                    if espacio_libre:
                        for col in range(columna, columna + tamaño):
                            tablero[fila][col] = nombre[0]
                        colocado = True
            else:
                if fila + tamaño <= 10:
                    espacio_libre = all(tablero[fila + f][columna] == 'O' for f in range(tamaño))
                    if espacio_libre:
                        for f in range(tamaño):
                            tablero[fila + f][columna] = nombre[0]
                        colocado = True

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
        if not any(celda == barco for fila in tablero_enemigo for celda in fila):
            print(f"¡Hundiste un barco ({barco})!")
        else:
            print("¡Impacto!")
        return True

def todas_naves_hundidas(tablero):
    for fila in tablero:
        for celda in fila:
            if celda not in ['O', 'X', 'T']:
                return False
    return True

def jugar_turno(nombre_jugador, tablero_enemigo):
    print(f"Turno de {nombre_jugador}.")
    letras_columna = "ABCDEFGHIJ"
    while True:
        try:
            fila = int(input("Introduce la fila (0-9): "))
            columna_letra = input("Introduce la columna (A-J): ").upper()
            if 0 <= fila < 10 and columna_letra in letras_columna:
                columna = letras_columna.index(columna_letra)
                return disparar(tablero_enemigo, fila, columna)
            else:
                print("Por favor, introduce una fila entre 0 y 9 y una columna entre A y J.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce números enteros para la fila y letras para la columna.")

def main():
    print("Bienvenido a la Batalla Naval!")
    print("Reglas del juego:")
    print("1. El objetivo es hundir los 9 barcos de tu oponente antes que él hunda los tuyos.")
    print("2. Los barcos disponibles son:\n   - 1 Portaaviones (4 casillas)\n   - 3 Submarinos/Acorazados (3 casillas cada uno)\n   - 3 Destructores (2 casillas cada uno)\n   - 2 Fragatas (1 casilla cada una)\n")
    input("¿Listo para convertirte en un marine? Presiona Enter para continuar...\n")

    barcos = {
        "Portaaviones": 4,
        "Submarino": 3,
        "Acorazado": 3,
        "Destructor": 2,
        "Fragata": 1
    }

    tablero_jugador1 = crear_tablero()
    tablero_jugador2 = crear_tablero()
    posicionar_barcos(tablero_jugador1, barcos)
    posicionar_barcos(tablero_jugador2, barcos)

    jugadores = [("Jugador 1", tablero_jugador1), ("Jugador 2", tablero_jugador2)]
    turno = 0

    while True:
        nombre_jugador, tablero_propio = jugadores[turno]
        nombre_oponente, tablero_oponente = jugadores[1 - turno]

        mostrar_tablero(tablero_propio)
        jugar_turno(nombre_jugador, tablero_oponente)

        if todas_naves_hundidas(tablero_oponente):
            print(f"¡{nombre_jugador} ha ganado! Hundiste todas las naves de {nombre_oponente}.")
            break

        turno = 1 - turno

        input(f"\n¿Listo {jugadores[turno][0]}? Presiona Enter para continuar...\n")
        limpiar_consola()

if __name__ == "__main__":
    main()
