from flask import Flask, render_template
import json

app = Flask(__name__)

file = open("conceitos_relacoes_e_sinonimos.json")
conceitos = json.load(file)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/conceitos")
def listar_Conceitos():
    return render_template("conceitos.html", conceitos = conceitos)


@app.route("/conceitos/<designacao>")
def consultar_Conceitos(designacao):
    return render_template('conc.html',conceito = conceitos[designacao], designacao = designacao)


app.run(host="localhost", port=4002, debug=True)