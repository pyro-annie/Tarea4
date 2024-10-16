from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

def inicializar_votos(distritos, candidatos):
    random.seed()
    return [[random.randint(0, 10000) for _ in range(candidatos)] for _ in range(distritos)]

def sumar_votos_por_candidato(votos):
    return [sum(distrito) for distrito in zip(*votos)]

def sumar_votos_por_distrito(votos):
    return [sum(candidato) for candidato in votos]

def encontrar_candidato_ganador(suma_candidatos):
    max_votos = max(suma_candidatos)
    return suma_candidatos.index(max_votos), max_votos

def encontrar_distrito_ganador(suma_distritos):
    max_distrito = max(suma_distritos)
    return suma_distritos.index(max_distrito), max_distrito

def distrito_que_mas_voto_por_candidato(votos, candidato_ganador):
    max_votos_candidato = max(voto[candidato_ganador] for voto in votos)
    for i, distrito in enumerate(votos):
        if distrito[candidato_ganador] == max_votos_candidato:
            return i, max_votos_candidato

def calcular_resultados(votos):
    suma_candidatos = sumar_votos_por_candidato(votos)
    suma_distritos = sumar_votos_por_distrito(votos)
    candidato_ganador, max_votos = encontrar_candidato_ganador(suma_candidatos)
    distrito_ganador, max_distrito = encontrar_distrito_ganador(suma_distritos)
    distrito_max_votos_candidato_ganador, max_votos_candidato_ganador = distrito_que_mas_voto_por_candidato(votos, candidato_ganador)
    return votos, suma_candidatos, suma_distritos, candidato_ganador, max_votos, distrito_ganador, max_distrito, distrito_max_votos_candidato_ganador, max_votos_candidato_ganador

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        distritos = int(request.form["distritos"])
        candidatos = int(request.form["candidatos"])
        votos = inicializar_votos(distritos, candidatos)
        resultados = calcular_resultados(votos)
        votos, suma_candidatos, suma_distritos, candidato_ganador, max_votos, distrito_ganador, max_distrito, distrito_max_votos_candidato_ganador, max_votos_candidato_ganador = resultados
        return render_template("resultados.html", votos=votos, suma_candidatos=suma_candidatos, suma_distritos=suma_distritos, candidato_ganador=candidato_ganador, max_votos=max_votos, candidatos=candidatos, distrito_ganador=distrito_ganador, max_distrito=max_distrito, distrito_max_votos_candidato_ganador=distrito_max_votos_candidato_ganador, max_votos_candidato_ganador=max_votos_candidato_ganador)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
