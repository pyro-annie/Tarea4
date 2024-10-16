from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

def inicializar_votos(distritos, candidatos):
    random.seed()
    votos = [[random.randint(0, 10000) for _ in range(candidatos)] for _ in range(distritos)]
    return votos

def calcular_resultados(votos):
    distritos = len(votos)
    candidatos = len(votos[0])
    suma_candidatos = [0] * candidatos
    suma_distritos = [0] * distritos
    max_votos = 0
    candidato_ganador = -1

    for i in range(distritos):
        for j in range(candidatos):
            suma_candidatos[j] += votos[i][j]
            suma_distritos[i] += votos[i][j]

    for j in range(candidatos):
        if suma_candidatos[j] > max_votos:
            max_votos = suma_candidatos[j]
            candidato_ganador = j

    return votos, suma_candidatos, suma_distritos, candidato_ganador, max_votos

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        distritos = int(request.form["distritos"])
        candidatos = int(request.form["candidatos"])

        votos = inicializar_votos(distritos, candidatos)
        resultados = calcular_resultados(votos)
        votos, suma_candidatos, suma_distritos, candidato_ganador, max_votos = resultados

        return render_template("resultados.html", votos=votos, suma_candidatos=suma_candidatos, suma_distritos=suma_distritos, candidato_ganador=candidato_ganador, max_votos=max_votos, candidatos=candidatos)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
