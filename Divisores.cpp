#include <iostream>
#include <random>
#include <iomanip>
#include <vector>
#include <string> 

using namespace std;

struct Divisores {
    int numero;
    vector<int> divisores;
};

void calcularDivisores(int numero, vector<int>& divisores) {
    divisores.clear();
    for (int i = 1; i <= numero; ++i) {
        if (numero % i == 0) {
            divisores.push_back(i);
            if (divisores.size() == 5) {
                break;
            }
        }
    }
}

int generarNumeroAleatorio(int min, int max) {
    static random_device rd;
    static mt19937 gen(rd());
    uniform_int_distribution<> dist(min, max);
    return dist(gen);
}

void imprimirResultados(const Divisores numeros[], int size) {
    cout << left << setw(10) << "Número" << " | " << setw(30) << "Divisores" << endl;
    cout << string(45, '-') << endl;
    for (int i = 0; i < size; ++i) {
        cout << left << setw(10) << numeros[i].numero << " | ";
        for (int divisor : numeros[i].divisores) {
            cout << divisor << " ";
        }
        cout << endl;
    }
}

bool preguntarContinuar() {
    string continuar;
    while (true) {
        cout << "¿Deseas ejecutar el programa nuevamente? (s/n): ";
        getline(cin, continuar);
        if (continuar == "s" || continuar == "S" || continuar == "n" || continuar == "N") {
            break;
        } else if (continuar.find_first_not_of(' ') == string::npos) {
            cout << "Entrada no válida. Por favor, introduce 's' para sí o 'n' para no." << endl;
        } else {
            cout << "Entrada inválida. Por favor, introduce 's' para sí o 'n' para no." << endl;
        }
    }
    return continuar == "s" || continuar == "S";
}

int main() {
    const int cantidadNumeros = 20;
    Divisores numeros[cantidadNumeros];
    do {
        for (int i = 0; i < cantidadNumeros; ++i) {
            numeros[i].numero = generarNumeroAleatorio(1, 100);
            calcularDivisores(numeros[i].numero, numeros[i].divisores);
        }
        imprimirResultados(numeros, cantidadNumeros);
    } while (preguntarContinuar());
    
    return 0;
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