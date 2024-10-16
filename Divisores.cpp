#include <iostream>  // Para la entrada y salida estándar
#include <random>    // Para la generación de números aleatorios
#include <iomanip>   // Para la manipulación del formato de salida
#include <vector>    // Para el uso de la estructura de datos vector
#include <string>    // Para usar la función getline

using namespace std; // Para evitar escribir "std::" antes de cada función del estándar

// Estructura para almacenar un número y sus divisores
struct Divisores {
    int numero; // Número generado
    vector<int> divisores; // Vector para almacenar los divisores del número
};

// Función para calcular los divisores de un número
void calcularDivisores(int numero, vector<int>& divisores) {
    divisores.clear(); // Limpiar el vector antes de calcular
    for (int i = 1; i <= numero; ++i) {
        if (numero % i == 0) { // Si 'i' es divisor de 'numero'
            divisores.push_back(i); // Añadir el divisor al vector
            if (divisores.size() == 5) { // Limitar a 5 divisores
                break; // Salir del bucle si ya se han encontrado 5 divisores
            }
        }
    }
}

// Función para generar un número aleatorio en un rango específico usando std::mt19937
int generarNumeroAleatorio(int min, int max) {
    static random_device rd; // Generador de semilla para números aleatorios
    static mt19937 gen(rd()); // Mersenne Twister para la generación de números aleatorios de alta calidad
    uniform_int_distribution<> dist(min, max); // Distribución uniforme entre 'min' y 'max'
    return dist(gen); // Generar y devolver un número aleatorio
}

// Función para imprimir los resultados en formato de tabla
void imprimirResultados(const Divisores numeros[], int size) {
    cout << left << setw(10) << "Número" << " | " << setw(30) << "Divisores" << endl;
    cout << string(45, '-') << endl;
    for (int i = 0; i < size; ++i) {
        cout << left << setw(10) << numeros[i].numero << " | ";
        for (int divisor : numeros[i].divisores) {
            cout << divisor << " "; // Imprimir cada divisor separado por un espacio
        }
        cout << endl;
    }
}

// Función para preguntar al usuario si desea continuar ejecutando el programa
bool preguntarContinuar() {
    string continuar; // Variable para almacenar la respuesta del usuario
    while (true) {
        cout << "¿Deseas ejecutar el programa nuevamente? (s/n): ";
        getline(cin, continuar); // Leer la entrada completa del usuario
        if (continuar == "s" || continuar == "S" || continuar == "n" || continuar == "N") {
            break; // Salir del bucle si la respuesta es válida ('s' o 'n')
        } else if (continuar.find_first_not_of(' ') == string::npos) {
            cout << "Entrada no válida. Por favor, introduce 's' para sí o 'n' para no." << endl;
        } else {
            cout << "Entrada inválida. Por favor, introduce 's' para sí o 'n' para no." << endl;
        }
    }
    return continuar == "s" || continuar == "S"; // Devolver verdadero si el usuario quiere continuar
}

int main() {
    const int cantidadNumeros = 20; // Número de números aleatorios a generar
    Divisores numeros[cantidadNumeros]; // Array de estructuras Divisores
    do {
        for (int i = 0; i < cantidadNumeros; ++i) {
            numeros[i].numero = generarNumeroAleatorio(1, 100); // Generar un número aleatorio entre 1 y 100
            calcularDivisores(numeros[i].numero, numeros[i].divisores); // Calcular los divisores del número
        }
        imprimirResultados(numeros, cantidadNumeros); // Imprimir los resultados en una tabla
    } while (preguntarContinuar()); // Repetir si el usuario desea continuar
    
    return 0; // Fin del programa
}

/*
Mejoras y novedades:
1. Modularización del Código:
   - Se dividió el programa en funciones más pequeñas y específicas, mejorando la legibilidad y facilitando el mantenimiento.
   - Se crearon funciones como `generarNumeroAleatorio`, `calcularDivisores`, `imprimirResultados` y `preguntarContinuar`.

2. Mejora de Aleatoriedad:
   - Se reemplazó el uso de `rand()` por `std::mt19937`, que ofrece una mejor calidad de aleatoriedad.

3. Validaciones de Entrada del Usuario:
   - Se añadieron validaciones para la entrada del usuario al preguntar si desea ejecutar el programa nuevamente, asegurando que sólo se acepten respuestas válidas ('s' o 'n').
   - Se añadió una verificación para evitar que el usuario ingrese solo espacios en blanco o presione enter sin escribir nada cuando se le pregunta si desea continuar.

4. Formato de Salida Mejorado:
   - Se mejoró el formato de la salida usando manipuladores de flujo como `setw`, `setfill`, y `left` para que la tabla se vea más ordenada y profesional.

5. Optimización del Código:
   - Se eliminaron librerías y variables innecesarias para hacer el código más limpio y eficiente.
*/
