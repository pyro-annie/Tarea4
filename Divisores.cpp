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


