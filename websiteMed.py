from flask import Flask, render_template, redirect, url_for, request
import json
from deep_translator import GoogleTranslator
import re
app = Flask(__name__)

def trocar_ficheiro(lang):
    if lang == "en":
        file = open("dicionarios/doc_conc_en_V_GMS_outros_relacionados.json", 'r', encoding='UTF-8')
        conceitos = json.load(file)
    elif lang == "es":
        file = open("dicionarios/doc_conc_es_V_GMS_outros_relacionados.json", 'r',encoding='UTF-8')
        conceitos = json.load(file)
    else:
        file = open("dicionarios/doc_conc_pt_V_GMS_outros_relacionados.json", 'r', encoding='UTF-8')
        conceitos = json.load(file)
    file.close()
    return conceitos



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/conceitos/<lang>")
def pesquisa_conc(lang="es"):
    conceitos = trocar_ficheiro(lang)
    query = request.args.get("query_conceito_ou_desc")
    match = {}

    if query:
        for indice in conceitos:
            if conceitos[indice]['Termo']:
                conceito = conceitos[indice]['Termo']
                if query.lower() in conceito.lower():
                    conceiton = re.sub(rf'({query})', r'<b>\1</b>', conceito)
                    if query.lower() in conceitos[indice]["Termo"].lower():
                        descricaon = re.sub(rf'({query})', r'<b>\1</b>', conceitos[indice]["Descricao"].lower())
                        match[indice][conceiton] = {'Definicao': descricaon, "original": conceito}
                    else:
                        match[indice][conceiton] = {'Definicao': conceitos[indice]['Definicao'], "original": conceito}
                else:
                    if query.lower() in conceitos[indice]['Definicao'].lower():
                        descricaon = re.sub(rf'({query})', r'<b>\1</b>', conceitos[indice]['Definicao'].lower())
                        match[indice][conceito] = {'Definicao': descricaon, "original": conceito}

    if match:
        return render_template("conceitos.html", conceitos=match, pesquisa=query, res=len(match), lang=lang)
    else:
        return render_template("conceitos.html", conceitos=conceitos, pesquisa=False, lang=lang)
    
    


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
                if dupla[0]!= "Traducoes":
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




@app.route("/add_entrada", methods=["GET","POST"])
def add_entrada():
    conc = request.args.get("conc")
    defi = request.args.get("def")
    areas = request.args.get("areas")
    fontes = request.args.get("fontes")
    index_rem = request.args.get("index_rem")
    print(conc, defi, areas, fontes, index_rem)
    return render_template("home.html")





@app.route("/table")
def table():
    file = open("dicionarios/doc_conc_en_V_GMS_outros_semRepetidos.json", 'r', encoding='UTF-8')
    conceitos = json.load(file)
    return render_template("table.html", conceitos=conceitos)


@app.route("/pesquisa_detalhada", methods=['GET', 'POST'])
def pesquisa_detalhada():
    if request.method == 'POST':
        selected_sources = request.form.getlist('sources')
        selected_language = request.form.get('language')
        termo = request.form.get("termo")
        descricao = request.form.get("descricao")
        sinonimos = request.form.get("sinonimos")
        relacionados = request.form.get("relacionados")
        if selected_sources or selected_language or termo or descricao or sinonimos or relacionados:
            if selected_language:
                if selected_language == 'en':
                    conceitos = {'en': trocar_ficheiro('en')}
                elif selected_language == 'pt':
                    conceitos = {'pt': trocar_ficheiro('pt')}
                elif selected_language == 'es':
                    conceitos = {'es': trocar_ficheiro('es')}
            else:
                conceitosen = trocar_ficheiro('en')
                conceitoses = trocar_ficheiro('es')
                conceitospt = trocar_ficheiro('pt')
                conceitos = {'es': conceitoses, 'en': conceitosen, 'pt': conceitospt}

            matches = { 'en': {}, 'es': {}, 'pt': {} }
            if selected_sources:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Fontes' in conceitos[idioma][indice]:
                            for source in selected_sources:
                                if source in conceitos[idioma][indice]['Fontes']:
                                    print(source)
                                    matches[idioma][indice] = conceitos[idioma][indice]
            if termo:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if conceitos[idioma][indice]['Termo']:
                            if termo.lower() in conceitos[idioma][indice]['Termo'].lower():
                                matches[idioma][indice] = conceitos[idioma][indice]
            if descricao:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Definicao' in conceitos[idioma][indice]:
                            if descricao.lower() in conceitos[idioma][indice]['Definicao'].lower():
                                matches[idioma][indice] = conceitos[idioma][indice]
            if sinonimos:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Sinonimos' in conceitos[idioma][indice]:
                            s = ' '.join(conceitos[idioma][indice]['Sinonimos'])
                            if sinonimos.lower() in s.lower():
                                matches[idioma][indice] = conceitos[idioma][indice]
            if selected_language and not selected_sources and not termo and not relacionados and not sinonimos and not descricao:
                matches = conceitos
            
            return render_template("pesquisaDetalhada.html", pesquisa = True, matches = matches)
        else:
            return render_template("pesquisaDetalhada.html", pesquisa = False)
    else:
        return render_template("pesquisaDetalhada.html")







app.run(host="localhost", port=4002, debug=True)


