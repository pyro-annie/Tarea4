#include <iostream>
#include <cstdlib>
#include <ctime>
#include <iomanip> // Para usar setw y setfill
#include <vector>  // Para usar el vector y almacenar divisores temporalmente

using namespace std;

struct Divisores {
    int numero;
    vector<int> divisores; // Usamos un vector para almacenar divisores dinámicamente
};

void calcularDivisores(int numero, vector<int>& divisores) {
    divisores.clear(); // Limpiamos el vector antes de calcular
    for (int i = 1; i <= numero; ++i) {
        if (numero % i == 0) {
            divisores.push_back(i);
            if (divisores.size() == 5) { // Si ya tenemos 5 divisores, paramos
                break;
            }
        }
    }
}

bool esPrimo(int numero) {
    if (numero <= 1) return false;
    for (int i = 2; i <= numero / 2; ++i) {
        if (numero % i == 0) return false;
    }
    return true;
}

int main() {
    srand(static_cast<unsigned>(time(0))); // Inicializa la semilla para números aleatorios
    Divisores numeros[20];
    char continuar;

    do {
        for (int i = 0; i < 20; ++i) {
            numeros[i].numero = rand(); // Genera un número aleatorio hasta el límite máximo de rand()
            calcularDivisores(numeros[i].numero, numeros[i].divisores);
        }

        // Mostrar resultados en formato de tabla
        cout << left << setw(10) << "Número" << " | " << setw(30) << "Divisores" << endl;
        cout << string(45, '-') << endl;
        for (int i = 0; i < 20; ++i) {
            cout << left << setw(10) << numeros[i].numero << " | ";
            for (int j = 0; j < numeros[i].divisores.size(); ++j) {
                cout << numeros[i].divisores[j] << " ";
            }
            cout << endl;
        }

        cout << "¿Deseas ejecutar el programa nuevamente? (s/n): ";
        cin >> continuar;

    } while (continuar == 's' || continuar == 'S');

    return 0;
}