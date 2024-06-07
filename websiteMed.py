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
def consultar_Conceitos(id_conc, lang="es", warning=None):
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
        
    chaves_trad = {chave : GoogleTranslator(source="auto", target=lang).translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Nota', 'Categoria gramatical', 'não disponível']}
    return render_template('conc.html',conceito = conceito, lang= lang, id_conc = id_conc, conceitos = conceitos, ch_tr = chaves_trad, warning = warning)




@app.route('/change_language', methods=['GET'])
def change_language():
    lang = request.args.get("lang")
    id_c = request.args.get("id_conc")
    return redirect(url_for('consultar_Conceitos', id_conc=id_c, lang=lang))




@app.route("/add_entrada", methods=["POST"])
def add_entrada_nova():
    data = request.form.to_dict(flat=True)
    conc = data["conc"]
    conceitos_en = trocar_ficheiro("en")
    if conc:
        defi = data["def"]
        areas = data["areasAp"]
        print(areas)
        fontes = data["fontesAp"]
        print(fontes)
        sinonimos = data["SinAp"]
        print(sinonimos)
        index_rem = data["index_rem"]

        conceitos_en = trocar_ficheiro("en")
        conceitos_es = trocar_ficheiro("es")
        conceitos_pt = trocar_ficheiro("pt")
        conc_en = GoogleTranslator(source='auto', target='en').translate(conc)
        conc_es = GoogleTranslator(source='auto', target='es').translate(conc)
        conc_pt = GoogleTranslator(source='auto', target='pt').translate(conc)

        if conc_en in [conceitos_en[conceito]["Termo"] for conceito in conceitos_en] or conc_es in [conceitos_es[conceito]["Termo"] for conceito in conceitos_es] or conc_pt in [conceitos_pt[conceito]["Termo"] for conceito in conceitos_pt]:
            print("Invalid")
            return render_template('conceitos.html', warning="Term already exists in one of the files! Insert failed!", lang="en", conceitos = conceitos_en)
        else:
            d_id = int(list(conceitos_en.keys())[-1]) + 1
            print(d_id)
            while d_id in conceitos_pt or d_id in conceitos_en or d_id in conceitos_es:   # failsafe
                d_id +=1

            print(d_id)
            dic_es = {}
            dic_pt = {}
            dic_en = {}

            dic_en["Termo"] = GoogleTranslator(source='auto', target='en').translate(conc)
            dic_es["Termo"] = GoogleTranslator(source='auto', target='es').translate(conc)
            dic_pt["Termo"] = GoogleTranslator(source='auto', target='pt').translate(conc)

            if defi:
                dic_es["Definicao"] = GoogleTranslator(source='auto', target='es').translate(defi)
                dic_en["Definicao"] = GoogleTranslator(source='auto', target='en').translate(defi)
                dic_pt["Definicao"] = GoogleTranslator(source='auto', target='pt').translate(defi)
            if index_rem:
                dic_es["Index_Remissivo"] = index_rem
                dic_en["Index_Remissivo"] = index_rem
                dic_pt["Index_Remissivo"] = index_rem
            if areas:
                dic_es["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='es').translate(area.strip("*")) for area in areas.split(',')]
                dic_en["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='en').translate(area.strip("*")) for area in areas.split(',')]
                dic_pt["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='pt').translate(area.strip("*")) for area in areas.split(',')]
            if fontes:
                    dic_es["Fontes"] = [fonte for fonte in fontes.split(',')]
                    dic_en["Fontes"] = [fonte for fonte in fontes.split(',')]
                    dic_pt["Fontes"] = [fonte for fonte in fontes.split(',')]
            conceitos_en[d_id] = dic_en
            conceitos_es[d_id] = dic_es      
            conceitos_pt[d_id] = dic_pt              
            
            file_en = open("dicionarios/doc_conc_en_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')
            file_es = open("dicionarios/doc_conc_es_V_GMS_outros_relacionados.json", 'w',encoding='UTF-8')
            file_pt = open("dicionarios/doc_conc_pt_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')

            json.dump(conceitos_en, file_en, indent=4, ensure_ascii=False)
            json.dump(conceitos_es, file_es, indent=4, ensure_ascii=False)
            json.dump(conceitos_pt, file_pt, indent=4, ensure_ascii=False)

            file_pt.close()
            file_en.close()
            file_es.close()
            chaves_trad = {chave : GoogleTranslator(source="pt", target="en").translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Nota', 'Categoria gramatical', 'não disponível']}
        return redirect(url_for("consultar_Conceitos",lang="en", id_conc = d_id, warning = "Sucess!", ch_tr = chaves_trad ))
    else:
        return render_template('conceitos.html', lang="en", warning = "Concept not specified! Insert failed!", conceitos = conceitos_en)


@app.route("/apagar_entrada", methods=["POST"])
def removeConc():
    id_conc = request.form["rc"]
    fic_en = trocar_ficheiro("en")
    if id_conc in fic_en:
        fic_es = trocar_ficheiro("es")
        fic_pt = trocar_ficheiro("pt")
        del fic_en[id_conc]
        del fic_es[id_conc]
        del fic_pt[id_conc]

        file_en = open("dicionarios/doc_conc_en_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')
        file_es = open("dicionarios/doc_conc_es_V_GMS_outros_relacionados.json", 'w',encoding='UTF-8')
        file_pt = open("dicionarios/doc_conc_pt_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')

        json.dump(fic_en, file_en, indent=4, ensure_ascii=False)
        json.dump(fic_es, file_es, indent=4, ensure_ascii=False)
        json.dump(fic_pt, file_pt, indent=4, ensure_ascii=False)

        file_pt.close()
        file_en.close()
        file_es.close()
        warn = "Entry removed"
        print("Done")
    else:
        warn = "There is no entry with that key!"
    conceitos = trocar_ficheiro("en")
    return render_template("conceitos.html", lang="en", warning = warn, conceitos=conceitos)




@app.route("/table")
def table():
    file = open("dicionarios/doc_conc_en_V_GMS_outros_semRepetidos.json", 'r', encoding='UTF-8')
    conceitos = json.load(file)
    return render_template("table.html", conceitos=conceitos)

@app.route("/pesquisa_detalhada", methods=['GET', 'POST'])

def pesquisa_detalhada():
    if request.method == 'POST':
        option = request.form['options']
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
            else:
                conceitosen = trocar_ficheiro('en')
                conceitoses = trocar_ficheiro('es')
                conceitospt = trocar_ficheiro('pt')
                conceitos = {'es': conceitoses, 'en': conceitosen, 'pt': conceitospt}

            matches = {'en': {}, 'es': {}, 'pt': {}}

            if option == 'or':
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
            else: # AND
                
                matchesT = {'en': {}, 'es': {}, 'pt': {}}
                if selected_sources:
                    for idioma in conceitos:
                        for indice in conceitos[idioma]:
                            if 'Fontes' in conceitos[idioma][indice]:
                                count = 0
                                for source in selected_sources:
                                    if source in conceitos[idioma][indice]['Fontes']:
                                        count +=1
                                if count == len(selected_sources):
                                    matches[idioma][indice] = conceitos[idioma][indice]

                if termo:
                    matchesT = {'en': {}, 'es': {}, 'pt': {}}
                    for idioma in conceitos:
                        for indice in conceitos[idioma]:
                            if conceitos[idioma][indice]['Termo']:
                                if termo.lower() in conceitos[idioma][indice]['Termo'].lower():
                                    matchesT[idioma][indice] = conceitos[idioma][indice]
                            if indice in matches[idioma] and indice not in matchesT[idioma]:
                                print("OHNAOOO", indice)
                                del matches[idioma][indice]

                                    

                if descricao:
                    matchesT = {'en': {}, 'es': {}, 'pt': {}}
                    for idioma in conceitos:
                        for indice in conceitos[idioma]:
                            if 'Definicao' in conceitos[idioma][indice]:
                                if descricao.lower() in conceitos[idioma][indice]['Definicao'].lower():
                                    matchesT[idioma][indice] = conceitos[idioma][indice]

                            if indice in matches[idioma] and indice not in matchesT[idioma]:
                                del matches[idioma][indice]

                if sinonimos:
                    matchesT = {'en': {}, 'es': {}, 'pt': {}}
                    for idioma in conceitos:
                        for indice in conceitos[idioma]:
                            if 'Sinonimos' in conceitos[idioma][indice]:
                                s = ' '.join(conceitos[idioma][indice]['Sinonimos'])
                                if sinonimos.lower() in s.lower():
                                    matchesT[idioma][indice] = conceitos[idioma][indice]

                            if indice in matches[idioma] and indice not in matchesT[idioma]:
                                del matches[idioma][indice]

                if selected_language and not selected_sources and not termo and not relacionados and not sinonimos and not descricao:
                    matches = conceitos
                return render_template("pesquisaDetalhada.html", pesquisa = True, matches = matches)
        else:
            return render_template("pesquisaDetalhada.html", pesquisa = False)
    else:
        return render_template("pesquisaDetalhada.html")






app.run(host="localhost", port=4002, debug=True)


