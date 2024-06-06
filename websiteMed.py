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

def getCampo(campoInteresse, concs):
    lista = []
    for conceito in concs:
        if campoInteresse in concs[conceito]:
            lista.extend(concs[conceito][campoInteresse])
    lista = list(set(lista))
    return lista

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/conceitos/<lang>")
def pesquisa_conc(lang="es"):
    conceitos = trocar_ficheiro(lang)
    query = request.args.get("query_conceito_ou_desc")
    match = {}

    areas = getCampo("Área(s) de aplicação", conceitos)
    areas = [area.strip("*") for area in areas]
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
        return render_template("conceitos.html", conceitos=match, pesquisa=query, res=len(match), lang=lang, areas = areas)
    else:
        return render_template("conceitos.html", conceitos=conceitos, pesquisa=False, lang=lang, areas = areas)
    



@app.route("/conceitos/<lang>/<id_conc>")
def consultar_Conceitos(id_conc, lang="es"):
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




@app.route("/add_entrada", methods=["POST"])
def add_entrada():
    conc = request.form["conc"]
    defi = request.form["def"]
    areas = request.form.get("areas")
    fontes = request.form.get("fontes")
    sinonimos = request.form["sinonimos"]
    index_rem = request.form["index_rem"]

    if areas:
        areas = areas.split(",")
    if fontes:
        fontes = fontes.split(",")
    if sinonimos:
        sinonimos = sinonimos.split(",")

    print(conc, defi, areas, fontes, index_rem, sinonimos)
    conceitos_en = trocar_ficheiro("en")
    conceitos_es = trocar_ficheiro("es")
    conceitos_pt = trocar_ficheiro("pt")


    conc_en = GoogleTranslator(source='auto', target='en').translate(conc)
    conc_es = GoogleTranslator(source='auto', target='es').translate(conc)
    conc_pt = GoogleTranslator(source='auto', target='pt').translate(conc)

    if conc_en in conceitos_en or conc_es in conceitos_es or conc_pt in conceitos_pt:
        print("Invalid")
        return render_template("pesquisa_conc", warning="Already exists in one of the files!")
    else:
        d_id = len(conceitos_en) + 1
        dic_es = {}
        dic_pt = {}
        dic_en = {}

        if defi:
            dic_es["Definicao"] = GoogleTranslator(source='auto', target='es').translate(defi)
            dic_en["Definicao"] = GoogleTranslator(source='auto', target='en').translate(defi)
            dic_pt["Definicao"] = GoogleTranslator(source='auto', target='pt').translate(defi)
        if index_rem:
            dic_es["Index_Remissivo"] = index_rem
            dic_en["Index_Remissivo"] = index_rem
            dic_pt["Index_Remissivo"] = index_rem
        if areas:
                dic_es["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='es').translate(area) for area in areas]
                dic_en["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='en').translate(area) for area in areas]
                dic_pt["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='pt').translate(area) for area in areas]
        if fontes:
                dic_es["Fontes"] = [fonte for fonte in fontes]
                dic_en["Fontes"] = [fonte for fonte in fontes]
                dic_pt["Fontes"] = [fonte for fonte in fontes]

        conceitos_en[d_id] = dic_en
        conceitos_es[d_id] = dic_es      
        conceitos_pt[d_id] = dic_pt              
        
        #file_en = open("dicionarios/doc_conc_en_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')
        #file_es = open("dicionarios/doc_conc_es_V_GMS_outros_relacionados.json", 'w',encoding='UTF-8')
        #file_pt = open("dicionarios/doc_conc_pt_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')

        #json.dump(conceitos_en, file_en, indent=4, ensure_ascii=False)
        #json.dump(conceitos_es, file_es, indent=4, ensure_ascii=False)
        #json.dump(conceitos_pt, file_pt, indent=4, ensure_ascii=False)

        #file_pt.close()
        #file_en.close()
        #file_es.close()

    print(dic_en)
    print(dic_es)
    print(dic_pt)
    return render_template("home.html", warning="Insert sucessfull!")





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


