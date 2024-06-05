from flask import Flask, render_template, redirect, url_for, request
import json
from deep_translator import GoogleTranslator
import re
app = Flask(__name__)

def trocar_ficheiro(lang):
    if lang == "en":
        file = open("fusao_dados/doc_conc_en.json")
        conceitos = json.load(file)
    elif lang == "es":
        file = open("fusao_dados/doc_conc_es.json")
        conceitos = json.load(file)
    else:
        file = open("fusao_dados/doc_conc_pt.json")
        conceitos = json.load(file)
    file.close()
    return conceitos



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/conceitos/<lang>")
def listar_Conceitos(lang="es"):
    conceitos = trocar_ficheiro(lang)
    return render_template("conceitos.html", conceitos = conceitos, lang=lang)


@app.route("/conceitos/<lang>/<id_conc>")
def consultar_Conceitos(id_conc, lang="es"):

# str(GoogleTranslator(source="auto", target=lang).translate())
    if lang !="es" and lang!="pt" and lang!="en":
        conceitos = trocar_ficheiro("en")
        dic_list = list(conceitos[id_conc].items())
        conceito = {}
        for dupla in dic_list:
            if isinstance(dupla[1],list):
                if dupla[0]!= "Fontes":
                    conceito[dupla[0]] = [str(GoogleTranslator(source="auto", target=lang).translate(elem)) for elem in dupla[1]]
                else:
                    conceito[dupla[0]] = dupla[1]
            else:
                    conceito[dupla[0]] = str(GoogleTranslator(source="auto", target=lang).translate(dupla[1])) 
                    
    else:
        conceitos = trocar_ficheiro(lang)
        conceito = conceitos[id_conc]
        
    chaves_trad = {chave : GoogleTranslator(source="auto", target=lang).translate(chave) for chave in conceitos[id_conc].keys()}
    return render_template('conc.html',conceito = conceito, lang= lang, id_conc = id_conc, conceitos = conceitos, ch_tr = chaves_trad)




@app.route('/change_language', methods=['GET'])
def change_language():
    lang = request.args.get("lang")
    id_c = request.args.get("id_conc")
    return redirect(url_for('consultar_Conceitos', id_conc=id_c, lang=lang))

@app.route("/procuraSec")
def procura():
    conceitos = trocar_ficheiro("es")
    return render_template("procura.html")


@app.route("/add_entrada", methods=["GET","POST"])
def add_entrada():
    conc = request.args.get("conc")
    defi = request.args.get("def")
    areas = request.args.get("areas")
    fontes = request.args.get("fontes")
    index_rem = request.args.get("index_rem")
    print(conc, defi, areas, fontes, index_rem)
    return render_template("home.html")

app.run(host="localhost", port=4002, debug=True)