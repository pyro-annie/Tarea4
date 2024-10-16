# Importación de módulos
import os  # Utilizado para ejecutar comandos del sistema, como limpiar la consola
from colorama import Fore, Style, init  # Utilizado para dar color al texto en la consola

# Inicialización del módulo colorama
init()

# Función para limpiar la consola dependiendo del sistema operativo
def limpiar_consola():
    if os.name == 'nt':  # Si el sistema operativo es Windows
        os.system('cls')  # Comando para limpiar la consola en Windows
    else:
        os.system('clear')  # Comando para limpiar la consola en sistemas Unix (Linux, MacOS)

# Función para crear un tablero vacío de 10x10
def crear_tablero():
    return [['O' for _ in range(10)] for _ in range(10)]  # 'O' representa agua en el tablero

# Función para mostrar el tablero en la consola con colores
def mostrar_tablero(tablero):
    letras_columna = "ABCDEFGHIJ"  # Letras para las columnas del tablero
    print("  " + " ".join(letras_columna))  # Imprimir letras de las columnas
    for indice, fila in enumerate(tablero):  # Iterar sobre las filas del tablero
        fila_color = []  # Lista para almacenar los colores de las celdas
        for celda in fila:
            if celda == 'O':
                fila_color.append(Fore.BLUE + celda + Style.RESET_ALL)  # Color azul para agua
            elif celda == 'X':
                fila_color.append(Fore.CYAN + celda + Style.RESET_ALL)  # Color cian para disparo en agua
            elif celda == 'T':
                fila_color.append(Fore.RED + celda + Style.RESET_ALL)  # Color rojo para disparo en barco
            else:
                fila_color.append(celda)  # Mantener el color por defecto para barcos no tocados
        print(f"{indice} " + " ".join(fila_color))  # Imprimir índice de fila y las celdas con color
    print()  # Línea en blanco para separar visualmente

# Función para validar la entrada del usuario
def validar_entrada(prompt, validacion, error_msg="Entrada inválida. Intenta de nuevo."):
    while True:
        entrada = input(prompt)  # Solicitar entrada al usuario
        if validacion(entrada):  # Validar la entrada
            return entrada  # Devolver la entrada válida
        print(error_msg)  # Imprimir mensaje de error si la entrada no es válida

# Función para posicionar los barcos manualmente
def posicionar_barcos_manualmente(tablero, barcos):
    letras_columna = "ABCDEFGHIJ"  # Letras para las columnas del tablero
    for nombre, tamaño in sorted(barcos.items(), key=lambda item: item[1]):  # Ordenar barcos por tamaño
        colocado = False
        while not colocado:
            print(f"Coloca tu {nombre} (tamaño {tamaño})")
            mostrar_tablero(tablero)  # Mostrar el tablero antes de colocar el barco
            orientacion = validar_entrada("Elija la orientación (H para horizontal, V para vertical): ", lambda x: x.upper() in ['H', 'V']).upper()
            fila = int(validar_entrada("Introduce la fila (0-9): ", lambda x: x.isdigit() and 0 <= int(x) < 10))
            columna_letra = validar_entrada("Introduce la columna (A-J): ", lambda x: x.upper() in letras_columna).upper()
            columna = letras_columna.index(columna_letra)
            if orientacion == 'H':  # Colocación horizontal
                if columna + tamaño <= 10 and all(tablero[fila][col] == 'O' for col in range(columna, columna + tamaño)):
                    for col in range(columna, columna + tamaño):
                        tablero[fila][col] = nombre[0]  # Colocar barco en el tablero
                    colocado = True
                else:
                    print("¡Posición no válida! Intenta de nuevo.")
            else:  # Colocación vertical
                if fila + tamaño <= 10 and all(tablero[fila + f][columna] == 'O' for f in range(tamaño)):
                    for f in range(tamaño):
                        tablero[fila + f][columna] = nombre[0]  # Colocar barco en el tablero
                    colocado = True
                else:
                    print("¡Posición no válida! Intenta de nuevo.")
        mostrar_tablero(tablero)  # Mostrar el tablero después de colocar el barco

# Función para disparar en el tablero enemigo
def disparar(tablero_enemigo, fila, columna):
    if tablero_enemigo[fila][columna] == 'O':
        tablero_enemigo[fila][columna] = 'X'
        print("¡Agua!")  # No se golpeó ningún barco
        return False
    elif tablero_enemigo[fila][columna] in ['X', 'T']:
        print("Ya has disparado en esta posición.")  # Ya se había disparado en esta posición
        return False
    else:
        barco = tablero_enemigo[fila][columna]
        tablero_enemigo[fila][columna] = 'T'
        if not any(celda == barco for fila in tablero_enemigo for celda en fila):
            print(f"¡Hundiste un barco ({barco})!")  # Barco hundido
        else:
            print("¡Impacto!")  # Barco golpeado
        return True

# Función para verificar si todas las naves han sido hundidas
def todas_naves_hundidas(tablero):
    return all(celda in ['O', 'X', 'T'] for fila in tablero for celda en fila)

# Función para jugar un turno
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

# Función para mostrar las reglas del juego
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

# Función principal para ejecutar el juego
def jugar():
    mostrar_reglas()  # Mostrar las reglas al inicio del juego
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
