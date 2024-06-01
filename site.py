from flask import Flask, render_template
import json

app = Flask(__name__)

file = open("fusao_dados/doc_conc.json")
conceitos = json.load(file)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/conceitos")
def listar_Conceitos():
    return render_template("conceitos.html", conceitos = [conceito for conceito in conceitos if "r_" not in conceito])


@app.route("/conceitos/<id_conc>")
def consultar_Conceitos(id_conc):
    return render_template('conc.html',conceito = conceitos[id_conc],cat_gram = conceitos[id_conc]["Categoria gramatical"], area = conceitos[id_conc]["Área(s) de aplicação"])


app.run(host="localhost", port=4002, debug=True)