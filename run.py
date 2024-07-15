from flask import Flask, render_template, redirect, url_for, request
import json
from deep_translator import GoogleTranslator
import os
import re
#from transformers import pipeline
#from gensim.models import Word2Vec
#from gensim.utils import tokenize
import numpy as np
#from nltk.corpus import stopwords
#import nltk


#nltk.download('stopwords')
#stop_words = set(stopwords.words('portuguese'))

#model = Word2Vec.load("similaridade/modelo.w2v")

""" 

def get_mean_vector(text):
    tokens = list(tokenize(text, lower=True))
    vectors = [model.wv[token] for token in tokens if token not in stop_words and token in model.wv]
    if not vectors: 
        return np.zeros(model.vector_size)
    mean = np.mean(vectors, axis=0)
    return mean


def cosine(v1, v2):
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0  
    return np.dot(v1, v2) / (norm_v1 * norm_v2)


def splitTemas(texto):
    paragraphs = texto.split('@@@@@')
    return [p for p in paragraphs if p.strip()]


def getTemasRelevantes(pergunta, temas):
    sims = []
    query = get_mean_vector(pergunta)
    for tema in temas:
        vetor = get_mean_vector(tema)
        sim = cosine(query,vetor)
        sims.append((tema,sim))
    sorted_sims = sorted(sims,key=lambda x : x[1], reverse=True)
    relevantes = [tema for tema, sim in sorted_sims[:5]]
    return ' '.join(relevantes)

"""

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

d =trocar_ficheiro('pt')
definicoes = ' '.join(d[indice]['Definicao'].lower() for indice in d if 'Definicao' in d[indice])


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
        if id_conc in conceitos:
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
               chaves_trad = {chave : GoogleTranslator(source="auto", target=lang).translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Categoria gramatical', 'não disponível', "Index Remissivo", "Change Entry", "Change this idiom", "Change all idioms", "Close", "Submit","Variante"]}
               chaves_trad["Nota"] = GoogleTranslator(source="pt", target=lang).translate("Observação")
               conceito = {}
               warning = GoogleTranslator("pt",lang).translate("De momento esta página não está disponível, pedimos desculpa pelo incómodo")
               render_template('conc.html', lang= lang, id_conc = id_conc, conceitos = conceitos, ch_tr = chaves_trad, warning = warning, conceito = conceito)            
    else:
        conceitos = trocar_ficheiro(lang)
        if id_conc in conceitos:
            conceito = conceitos[id_conc]
        else:
            conceito = {}
            warning = GoogleTranslator("pt",lang).translate("De momento esta página não está disponível, pedimos desculpa pelo incómodo")
            chaves_trad = {chave : GoogleTranslator(source="auto", target=lang).translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Categoria gramatical', 'não disponível', "Index Remissivo", "Change Entry", "Change this idiom", "Change all idioms", "Close", "Submit","Variante"]}
            chaves_trad["Nota"] = GoogleTranslator(source="pt", target=lang).translate("Observação")
            render_template('conc.html', lang= lang, id_conc = id_conc, conceitos = conceitos, ch_tr = chaves_trad, warning = warning, conceito = conceito)
    total = len(conceitos)
    chaves_trad = {chave : GoogleTranslator(source="auto", target=lang).translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Categoria gramatical', 'não disponível', "Index Remissivo", "Change Entry", "Change this idiom", "Change all idioms", "Close", "Submit","Variante"]}
    chaves_trad["Nota"] = GoogleTranslator(source="pt", target=lang).translate("Observação")
    print(conceito)
    return render_template('conc.html',conceito = conceito, lang= lang, id_conc = id_conc, conceitos = conceitos, ch_tr = chaves_trad, warning = warning, total = total)




@app.route('/change_language', methods=['GET'])
def change_language():
    lang = request.args.get("lang")
    id_c = request.args.get("id_conc")
    return redirect(url_for('consultar_Conceitos', id_conc=id_c, lang=lang))




@app.route("/add_entrada", methods=["POST"])
def add_entrada_nova():
    data = request.form.to_dict(flat=True)
    conc = data["conc"]
    print(data)
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
        nota = data["nota"]
        print(nota)
        relacionados = data["relacionadoAp"]

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

            if nota:
                dic_es["Nota"] = GoogleTranslator(source='auto', target='es').translate(nota)
                dic_en["Nota"] = GoogleTranslator(source='auto', target='en').translate(nota)
                dic_pt["Nota"] = GoogleTranslator(source='auto', target='pt').translate(nota)
            if index_rem:
                if index_rem in conceitos_es:
                    dic_es["Index_Remissivo"] = index_rem
                if index_rem in conceitos_en:
                    dic_en["Index_Remissivo"] = index_rem
                if index_rem in conceitos_pt:
                    dic_pt["Index_Remissivo"] = index_rem
            if areas:
                dic_es["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='es').translate(area.strip("*")) for area in areas.split(',')]
                dic_en["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='en').translate(area.strip("*")) for area in areas.split(',')]
                dic_pt["Área(s) de aplicação"] = [GoogleTranslator(source='auto', target='pt').translate(area.strip("*")) for area in areas.split(',')]
            if fontes:
                    dic_es["Fontes"] = [fonte for fonte in fontes.split(',')]
                    dic_en["Fontes"] = [fonte for fonte in fontes.split(',')]
                    dic_pt["Fontes"] = [fonte for fonte in fontes.split(',')]
            if relacionados:
                    dic_es["Relacionado"] = [relacionado for relacionado in relacionados.split(',') if relacionado in conceitos_es]
                    dic_en["Relacionado"] = [relacionado for relacionado in relacionados.split(',') if relacionado in conceitos_en]
                    dic_pt["Relacionado"] = [relacionado for relacionado in relacionados.split(',') if relacionado in conceitos_pt]
            
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
            chaves_trad = {chave : GoogleTranslator(source="auto", target="en").translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Categoria gramatical', 'não disponível', "Index Remissivo", "Change Entry", "Change this idiom", "Change all idioms", "Close", "Submit","Variante"]}
            chaves_trad["Nota"] = GoogleTranslator(source="pt", target="en").translate("Observação")
        return redirect(url_for("consultar_Conceitos",lang="en", id_conc = d_id, warning = "Sucess!", ch_tr = chaves_trad))
    else:
        return render_template('conceitos.html', lang="en", warning = "Concept not specified! Insert failed!", conceitos = conceitos_en)


@app.route("/alterar_entrada/<lang>/<id_conc>", methods=["POST"])
def alterarConc(lang,id_conc):
    data = request.form.to_dict(flat=True)
    print(data)
    chaves_trad = {chave : GoogleTranslator(source="pt", target=lang).translate(chave) for chave in ['Relacionado', 'Fontes', 'Conceito', 'Sinonimos', 'Definicao', 'Área(s) de aplicação', 'Categoria gramatical', 'não disponível', "Index Remissivo", "Change Entry", "Change this idiom", "Change all idioms", "Close", "Submit", "Variante"]}
    chaves_trad["Nota"] = GoogleTranslator(source="pt", target=lang).translate("Observação")
    if data["selectedRadio"] == "btnradio1":
        conceitos_lang = trocar_ficheiro(lang)

        if data["conc"]:
            if data["conc"] not in [conceitos_lang[id_]["Termo"] for id_ in conceitos_lang]:
                conceitos_lang[id_conc]["Termo"] = data["conc"]
            else:
                redirect(url_for("consultar_Conceitos",lang="en", id_conc = id_conc, warning = f"Term already in file!", ch_tr = chaves_trad ))
        
        if data["def"]:
            conceitos_lang[id_conc]["Definicao"] = data["def"]
        else:
            conceitos_lang[id_conc]["Definicao"] = ""
        
        if data["var"]:
            conceitos_lang[id_conc]["Variante"] = data["var"]
        else:
            conceitos_lang[id_conc]["Variante"] = ""

        if data["nota"]:
            conceitos_lang[id_conc]["Nota"] = data["nota"]
        else:
            conceitos_lang[id_conc]["Nota"] = ""

        if data["areasAp"]:
            conceitos_lang[id_conc]["Área(s) de aplicação"] = data["areasAp"].split(",")
        else:
            conceitos_lang[id_conc]["Área(s) de aplicação"] = []

        if data["fontesAp"]:
            conceitos_lang[id_conc]["Fontes"] = data["fontesAp"].split(",")
            print( id_conc)
        else:
            conceitos_lang[id_conc]["Fontes"] = []
        
        if data["SinAp"]:
             conceitos_lang[id_conc]["Sinonimos"] = data["SinAp"].split(",")
        else:
            conceitos_lang[id_conc]["Sinonimos"] = []
        
        if data["relacionadoAp"]:
            conceitos_lang[id_conc]["Relacionado"] = [elem for elem in data["relacionadoAp"].split(",") if elem in conceitos_lang]
            print( id_conc)
        else:
            conceitos_lang[id_conc]["Relacionado"] = []
        
        
        if data["index_rem"]:
            if data["index_rem"] in conceitos_lang:
                conceitos_lang[id_conc]["Index_Remissivo"]  = [elem for elem in data["index_rem"] if elem in conceitos_lang]
            else:
                conceitos_lang[id_conc]["Index_Remissivo"]  = ""
        
        if lang == "es" or lang=="en" or lang=="pt":
            file = "dicionarios/doc_conc_" + lang + "_V_GMS_outros_relacionados.json"
            file_out = open(file, 'w', encoding='UTF-8')
            json.dump(conceitos_lang, file_out, indent=4, ensure_ascii=False)
            file_out.close()

            return redirect(url_for("consultar_Conceitos",lang="en", id_conc = id_conc, warning = f"Concept changed successfully at {lang} dictionary!", ch_tr = chaves_trad ))
        else:
            return redirect(url_for("consultar_Conceitos",lang="en", id_conc = id_conc, warning = f"There is no support to add to a {lang} dictionary yet!", ch_tr = chaves_trad ))
    else:
        conceitos_en = trocar_ficheiro("en")
        conceitos_es = trocar_ficheiro("es")
        conceitos_pt = trocar_ficheiro("pt")


        if data["conc"]:
            t_en = GoogleTranslator(source=lang, target="en").translate(data["conc"])
            t_es = GoogleTranslator(source=lang, target="es").translate(data["conc"])
            t_pt = GoogleTranslator(source=lang, target="pt").translate(data["conc"])

            if t_en not in [conceitos_en[id_]["Termo"] for id_ in conceitos_en] and t_es not in [conceitos_es[id_]["Termo"] for id_ in conceitos_es] and t_pt not in [conceitos_pt[id_]["Termo"] for id_ in conceitos_pt]:

                conceitos_en[id_conc]["Termo"] = t_en
                conceitos_es[id_conc]["Termo"] = t_es
                conceitos_pt[id_conc]["Termo"] = t_pt

            else:
                redirect(url_for("consultar_Conceitos",lang="en", id_conc = id_conc, warning = f"This term already exists in at least one of the dictionaries!", ch_tr = chaves_trad ))
        
        if data["def"]:
            conceitos_en[id_conc]["Definicao"] = GoogleTranslator(source=lang, target="en").translate(data["def"])
            conceitos_es[id_conc]["Definicao"] = GoogleTranslator(source=lang, target="es").translate(data["def"])
            conceitos_pt[id_conc]["Definicao"] = GoogleTranslator(source=lang, target="pt").translate(data["def"])
        else:
            conceitos_en[id_conc]["Definicao"] = ""
            conceitos_es[id_conc]["Definicao"] = ""
            conceitos_pt[id_conc]["Definicao"] = ""

        if data["nota"]:
            conceitos_en[id_conc]["Nota"] = GoogleTranslator(source=lang, target="en").translate(data["nota"])
            conceitos_es[id_conc]["Nota"] = GoogleTranslator(source=lang, target="es").translate(data["nota"])
            conceitos_pt[id_conc]["Nota"] = GoogleTranslator(source=lang, target="pt").translate(data["nota"])
        else:
            conceitos_en[id_conc]["Nota"] = ""
            conceitos_es[id_conc]["Nota"] = ""
            conceitos_pt[id_conc]["Nota"] = ""

        if data["areasAp"]:
            conceitos_en[id_conc]["Área(s) de aplicação"] = [GoogleTranslator(source=lang, target="en").translate(elem) for elem in data["areasAp"].split(",")]
            conceitos_es[id_conc]["Área(s) de aplicação"] = [GoogleTranslator(source=lang, target="es").translate(elem) for elem in data["areasAp"].split(",")]
            conceitos_pt[id_conc]["Área(s) de aplicação"] = [GoogleTranslator(source=lang, target="pt").translate(elem) for elem in data["areasAp"].split(",")]
        else:
            conceitos_en[id_conc]["Área(s) de aplicação"] = ""
            conceitos_es[id_conc]["Área(s) de aplicação"] = ""
            conceitos_pt[id_conc]["Área(s) de aplicação"] = ""

        if data["fontesAp"]:
            conceitos_en[id_conc]["Fontes"] = [elem for elem in data["fontesAp"].split(",")]
            conceitos_es[id_conc]["Fontes"] = [elem for elem in data["fontesAp"].split(",")]
            conceitos_pt[id_conc]["Fontes"] = [elem for elem in data["fontesAp"].split(",")]
        else:
            conceitos_en[id_conc]["Fontes"] = ""
            conceitos_es[id_conc]["Fontes"] = ""
            conceitos_pt[id_conc]["Fontes"] = ""
        
        if data["SinAp"]:
            conceitos_en[id_conc]["Sinonimos"] = [GoogleTranslator(source=lang, target="en").translate(elem) for elem in data["SinAp"].split(",")]
            conceitos_es[id_conc]["Sinonimos"] = [GoogleTranslator(source=lang, target="es").translate(elem) for elem in data["SinAp"].split(",")]
            conceitos_pt[id_conc]["Sinonimos"] = [GoogleTranslator(source=lang, target="pt").translate(elem) for elem in data["SinAp"].split(",")]
        else:
            conceitos_en[id_conc]["Sinonimos"] = ""
            conceitos_es[id_conc]["Sinonimos"] = ""
            conceitos_pt[id_conc]["Sinonimos"] = ""
        
        if data["relacionadoAp"]:
            print( data["relacionadoAp"].split(","))
            conceitos_en[id_conc]["Relacionado"] = [elem for elem in data["relacionadoAp"].split(",") if elem in conceitos_en]
            conceitos_es[id_conc]["Relacionado"] = [elem for elem in data["relacionadoAp"].split(",") if elem in conceitos_es]
            conceitos_pt[id_conc]["Relacionado"] = [elem for elem in data["relacionadoAp"].split(",") if elem in conceitos_pt]
        else:
            conceitos_en[id_conc]["Relacionado"] = ""
            conceitos_es[id_conc]["Relacionado"] = ""
            conceitos_pt[id_conc]["Relacionado"] = ""
        

        if data["index_rem"]:
            if data["index_rem"] in conceitos_en and data["index_rem"] in conceitos_es and data["index_rem"] in conceitos_pt:
                conceitos_en[id_conc]["Index_Remissivo"]  = data["index_rem"]
                conceitos_es[id_conc]["Index_Remissivo"]  = data["index_rem"]
                conceitos_pt[id_conc]["Index_Remissivo"]  = data["index_rem"]
            else:
                conceitos_en[id_conc]["Index_Remissivo"]  = ""
                conceitos_es[id_conc]["Index_Remissivo"]  = ""
                conceitos_pt[id_conc]["Index_Remissivo"]  = ""


        file_en = open("dicionarios/doc_conc_en_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')
        file_es = open("dicionarios/doc_conc_es_V_GMS_outros_relacionados.json", 'w',encoding='UTF-8')
        file_pt = open("dicionarios/doc_conc_pt_V_GMS_outros_relacionados.json", 'w', encoding='UTF-8')

        json.dump(conceitos_en, file_en, indent=4, ensure_ascii=False)
        json.dump(conceitos_es, file_es, indent=4, ensure_ascii=False)
        json.dump(conceitos_pt, file_pt, indent=4, ensure_ascii=False)

        file_pt.close()
        file_en.close()
        file_es.close()
        return redirect(url_for("consultar_Conceitos",lang="en", id_conc = id_conc, warning = f"Concept changed successfully in all dictionaries!", ch_tr = chaves_trad ))



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

        # Carregar os conceitos com base no idioma selecionado
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
                                    matches[idioma][indice] = conceitos[idioma][indice]
            if termo:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if conceitos[idioma][indice]['Termo']:
                            if termo.lower() in conceitos[idioma][indice]['Termo'].lower():
                                termo_novo = re.sub(rf'({re.escape(termo.lower())})', r'<mark>\1</mark>', conceitos[idioma][indice]['Termo'].lower())
                                matches[idioma][indice] = conceitos[idioma][indice]
                                matches[idioma][indice]['Termo'] = termo_novo
            if descricao:
                print(descricao)
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if indice == "4341":
                            print(conceitos[idioma][indice]['Definicao'], descricao.lower())
                        if 'Definicao' in conceitos[idioma][indice] and descricao.lower() in conceitos[idioma][indice]['Definicao'].lower():
                            print("oiiiiiiiiiiiiiiii")
                            definicao = re.sub(rf'({re.escape(descricao.lower())})', r'<mark>\1</mark>', conceitos[idioma][indice]['Definicao'].lower())
                            if indice not in matches[idioma]:
                                matches[idioma][indice] = conceitos[idioma][indice]
                                matches[idioma][indice]['Definicao'] = definicao
                            else:
                                matches[idioma][indice]['Definicao'] = definicao
            if sinonimos:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Sinonimos' in conceitos[idioma][indice]:
                            s = ' '.join(conceitos[idioma][indice]['Sinonimos'])
                            if sinonimos.lower() in s.lower():
                                matches[idioma][indice] = conceitos[idioma][indice]
            if selected_language and not selected_sources and not termo and not relacionados and not sinonimos and not descricao:
                matches = conceitos

        elif option == 'and':
            matchesT = {'en': {}, 'es': {}, 'pt': {}}
            if selected_sources:
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Fontes' in conceitos[idioma][indice]:
                            count = 0
                            for source in selected_sources:
                                if source in conceitos[idioma][indice]['Fontes']:
                                    count += 1
                            if count == len(selected_sources):
                                matches[idioma][indice] = conceitos[idioma][indice]
            else:
                matches = conceitos
            
            if termo:
                matchesT = {'en': {}, 'es': {}, 'pt': {}}
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if conceitos[idioma][indice]['Termo']:
                            if termo.lower() in conceitos[idioma][indice]['Termo'].lower():
                                termo_novo = re.sub(rf'({re.escape(termo.lower())})', r'<mark>\1</mark>', conceitos[idioma][indice]['Termo'].lower())
                                matchesT[idioma][indice] = conceitos[idioma][indice]
                                matchesT[idioma][indice]['Termo'] = termo_novo
                    for indice in list(matches[idioma].keys()):
                        if indice not in matchesT[idioma]:
                            del matches[idioma][indice]

            if descricao:
                matchesT = {'en': {}, 'es': {}, 'pt': {}}
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Definicao' in conceitos[idioma][indice] and descricao.lower() in conceitos[idioma][indice]['Definicao'].lower():
                            definicao_nova = re.sub(rf'({re.escape(descricao.lower())})', r'<mark>\1</mark>', conceitos[idioma][indice]['Definicao'].lower())
                            matchesT[idioma][indice] = conceitos[idioma][indice]
                            matchesT[idioma][indice]['Definicao'] = definicao_nova
                    for indice in list(matches[idioma].keys()):
                        if indice not in matchesT[idioma]:
                            del matches[idioma][indice]

            if sinonimos:
                matchesT = {'en': {}, 'es': {}, 'pt': {}}
                for idioma in conceitos:
                    for indice in conceitos[idioma]:
                        if 'Sinonimos' in conceitos[idioma][indice]:
                            s = ' '.join(conceitos[idioma][indice]['Sinonimos'])
                            if sinonimos.lower() in s.lower():
                                sinonimos_novo = re.sub(rf'({re.escape(sinonimos.lower())})', r'<mark>\1</mark>', '@'.join(conceitos[idioma][indice]['Sinonimos']).lower())
                                matchesT[idioma][indice] = conceitos[idioma][indice]
                                matchesT[idioma][indice]['Sinonimos'] = sinonimos_novo.split("@")
                    for indice in list(matches[idioma].keys()):
                        if indice not in matchesT[idioma]:
                            del matches[idioma][indice]

            if selected_language and not selected_sources and not termo and not relacionados and not sinonimos and not descricao:
                matches = conceitos

        return render_template("pesquisaDetalhada.html", pesquisa=True, matches=matches)
    else:
        return render_template("pesquisaDetalhada.html", pesquisa=False)


 

@app.route("/qa", methods=['GET', 'POST'])


def qa():
    if request.method == 'POST':
        termo = request.form.get("termo")
        ms = request.form.get("mostsimilar")
        nm = request.form.get("doesnotmatch")
        if termo and False: # fechar o if
            qa_pipeline = pipeline("question-answering", model="lfcc/bert-portuguese-squad")
            f = open("similaridade/Livro-de-Resumos-2024_novo.xml", 'r', encoding='UTF-8')
            texto = f.read()
            f.close()
            temas = splitTemas(texto)
            temas_relevantes = getTemasRelevantes(termo, temas)
            temas_relevantes += definicoes
            resposta = qa_pipeline(question=termo, context=temas_relevantes)
            resposta=resposta['answer']
            rr = termo
        else:
            resposta = False
            rr = ""
        if ms:
            try : mostsimilar = model.wv.most_similar(ms)[0][0]
            except : mostsimilar = f"{ms} não está no vocabulário"

        else:
            mostsimilar = False

        if nm:
            nm = nm.split(', ')
            if len(nm)>2: 
                try : notmatch = model.wv.doesnt_match(nm)
                except : notmatch = f"Um dos termos não está no vocabulário"
                nmr = nm
            else:
                notmatch = "Insira pelo menos 3 termos"
                nmr = ""
        else:
            notmatch = False
            nmr = ""
        return render_template("qa.html", pesquisa = True, resposta=resposta, mostsimilar=mostsimilar, notmatch=notmatch, nmr=nmr, ms=ms, rr=rr, warning="The model isn´t available on this web preview, sorry")
    else:
        return render_template("qa.html", pesquisa = False, warning="The model isn´t available on this web preview, sorry")








#app.run(host="localhost", port=4002, debug=True)

if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
