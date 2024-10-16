# Importamos las bibliotecas necesarias
from flask import Flask, render_template, request, redirect, url_for  # Flask es el marco web que estamos utilizando
import random  # random es una biblioteca para generar números aleatorios

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Función para inicializar votos aleatorios para cada distrito y candidato
def inicializar_votos(distritos, candidatos):
    random.seed()  # Inicializa el generador de números aleatorios
    return [[random.randint(0, 10000) for _ in range(candidatos)] for _ in range(distritos)]
    # Genera una matriz de votos con valores aleatorios entre 0 y 10000

# Función para sumar votos por candidato en todos los distritos
def sumar_votos_por_candidato(votos):
    return [sum(distrito) for distrito in zip(*votos)]
    # Suma los votos de cada candidato a lo largo de todos los distritos

# Función para sumar votos por distrito en todos los candidatos
def sumar_votos_por_distrito(votos):
    return [sum(candidato) for candidato in votos]
    # Suma los votos de cada distrito a lo largo de todos los candidatos

# Función para encontrar el candidato ganador
def encontrar_candidato_ganador(suma_candidatos):
    max_votos = max(suma_candidatos)  # Encuentra el número máximo de votos
    return suma_candidatos.index(max_votos), max_votos  # Devuelve el índice y el número máximo de votos

# Función para encontrar el distrito con más votos
def encontrar_distrito_ganador(suma_distritos):
    max_distrito = max(suma_distritos)  # Encuentra el número máximo de votos en un distrito
    return suma_distritos.index(max_distrito), max_distrito  # Devuelve el índice y el número máximo de votos en un distrito

# Función para encontrar el distrito que más votó por el candidato ganador
def distrito_que_mas_voto_por_candidato(votos, candidato_ganador):
    max_votos_candidato = max(voto[candidato_ganador] for voto in votos)  # Encuentra el máximo de votos para el candidato ganador
    for i, distrito in enumerate(votos):  # Itera sobre los distritos
        if distrito[candidato_ganador] == max_votos_candidato:  # Si encuentra el distrito con el máximo de votos para el candidato ganador
            return i, max_votos_candidato  # Devuelve el índice del distrito y el número de votos

# Función principal para calcular todos los resultados de la simulación
def calcular_resultados(votos):
    suma_candidatos = sumar_votos_por_candidato(votos)  # Suma los votos por candidato
    suma_distritos = sumar_votos_por_distrito(votos)  # Suma los votos por distrito
    candidato_ganador, max_votos = encontrar_candidato_ganador(suma_candidatos)  # Encuentra el candidato ganador
    distrito_ganador, max_distrito = encontrar_distrito_ganador(suma_distritos)  # Encuentra el distrito con más votos
    distrito_max_votos_candidato_ganador, max_votos_candidato_ganador = distrito_que_mas_voto_por_candidato(votos, candidato_ganador)
    # Encuentra el distrito que más votó por el candidato ganador
    return votos, suma_candidatos, suma_distritos, candidato_ganador, max_votos, distrito_ganador, max_distrito, distrito_max_votos_candidato_ganador, max_votos_candidato_ganador
    # Devuelve todos los resultados

# Ruta principal para la página de inicio
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        distritos = int(request.form["distritos"])  # Obtiene el número de distritos del formulario
        candidatos = int(request.form["candidatos"])  # Obtiene el número de candidatos del formulario
        votos = inicializar_votos(distritos, candidatos)  # Inicializa los votos
        resultados = calcular_resultados(votos)  # Calcula los resultados
        votos, suma_candidatos, suma_distritos, candidato_ganador, max_votos, distrito_ganador, max_distrito, distrito_max_votos_candidato_ganador, max_votos_candidato_ganador = resultados
        # Renderiza la plantilla de resultados con todos los datos necesarios
        return render_template("resultados.html", votos=votos, suma_candidatos=suma_candidatos, suma_distritos=suma_distritos, candidato_ganador=candidato_ganador, max_votos=max_votos, candidatos=candidatos, distrito_ganador=distrito_ganador, max_distrito=max_distrito, distrito_max_votos_candidato_ganador=distrito_max_votos_candidato_ganador, max_votos_candidato_ganador=max_votos_candidato_ganador)
    return render_template("index.html")
    # Renderiza la plantilla de inicio

# Ejecuta la aplicación Flask en modo debug
if __name__ == "__main__":
    app.run(debug=True)

