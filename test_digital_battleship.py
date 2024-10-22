import unittest
import os
from unittest.mock import patch
from DigitalBattleship import (
    limpiar_consola, crear_tablero, mostrar_tablero, validar_entrada,
    posicionar_barcos_manualmente, disparar, todas_naves_hundidas, jugar_turno
)

class TestDigitalBattleship(unittest.TestCase):

    @patch('builtins.input', side_effect=['5'])
    def test_validar_entrada(self, mock_input):
        validacion = lambda x: x.isdigit() and 0 <= int(x) < 10
        entrada = validar_entrada("Introduce un número (0-9): ", validacion)
        self.assertEqual(entrada, '5')

    def test_disparar_agua(self):
        tablero = crear_tablero()
        resultado = disparar(tablero, 0, 0)
        self.assertFalse(resultado)
        self.assertEqual(tablero[0][0], 'X')

    def test_disparar_impacto(self):
        tablero = crear_tablero()
        tablero[0][0] = 'B'
        resultado = disparar(tablero, 0, 0)
        self.assertTrue(resultado)
        self.assertEqual(tablero[0][0], 'T')

    def test_disparar_hundido(self):
        tablero = crear_tablero()
        tablero[0][0] = 'B'
        tablero[0][1] = 'B'
        resultado1 = disparar(tablero, 0, 0)
        self.assertTrue(resultado1)
        resultado2 = disparar(tablero, 0, 1)
        self.assertTrue(resultado2)
        self.assertEqual(tablero[0][0], 'T')
        self.assertEqual(tablero[0][1], 'T')

    def test_todas_naves_hundidas(self):
        tablero = crear_tablero()
        self.assertTrue(todas_naves_hundidas(tablero))
        tablero[0][0] = 'B'
        self.assertFalse(todas_naves_hundidas(tablero))

    @patch('builtins.input', side_effect=['H', '0', 'A'])
    def test_posicionar_barcos_manualmente(self, mock_input):
        tablero = crear_tablero()
        barcos = {"Barco1": 2}
        posicionar_barcos_manualmente(tablero, barcos)
        self.assertEqual(tablero[0][0], 'B')
        self.assertEqual(tablero[0][1], 'B')

    @patch('builtins.input', side_effect=['0', 'A'])
    def test_jugar_turno(self, mock_input):
        tablero = crear_tablero()
        tablero[0][0] = 'B'
        resultado = jugar_turno("Jugador1", tablero)
        self.assertTrue(resultado)
        self.assertEqual(tablero[0][0], 'T')

    def test_mostrar_tablero(self):
        tablero = crear_tablero()
        with patch('builtins.print') as mocked_print:
            mostrar_tablero(tablero)
            self.assertTrue(mocked_print.called)

    def test_limpiar_consola(self):
        with patch('os.system') as mocked_system:
            limpiar_consola()
            if os.name == 'nt':
                mocked_system.assert_called_with('cls')
            else:
                mocked_system.assert_called_with('clear')

    def test_limites_tablero(self):
        tablero = crear_tablero()
        barcos = {"Barco1": 2}
        with patch('builtins.input', side_effect=['H', '0', 'I']):
            posicionar_barcos_manualmente(tablero, barcos)
            self.assertEqual(tablero[0][8], 'B')
            self.assertEqual(tablero[0][9], 'B')

    @patch('builtins.input', side_effect=['A', 'K', '10'])
    def test_entradas_invalidas(self, mock_input):
        validacion = lambda x: x.isdigit() and 0 <= int(x) < 10
        with self.assertRaises(StopIteration):
            while True:
                validar_entrada("Introduce un número (0-9): ", validacion)

@patch('builtins.input', side_effect=[
    'H', '0', 'A',  # Jugador 1 coloca barco horizontalmente
    'H', '1', 'A',  # Jugador 2 coloca barco horizontalmente
    '', '',  # Entradas de "Enter" para limpiar consola
    '0', 'A', '', '1', 'A', '', '0', 'B', '', '1', 'B', '', '0', 'C', '', '0', 'D', '',  # Serie de disparos y más entradas de "Enter"
])
def test_juego_completo(self, mock_input):
    tablero_jugador1 = crear_tablero()
    tablero_jugador2 = crear_tablero()
    barcos = {"Barco1": 2}

    posicionar_barcos_manualmente(tablero_jugador1, barcos)
    posicionar_barcos_manualmente(tablero_jugador2, barcos)

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


if __name__ == '__main__':
    unittest.main()
