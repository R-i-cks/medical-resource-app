import json
from deep_translator import GoogleTranslator

#file = open("conceitos_rel_sin_trad.json")
""" 

file = open("novo.json") 
file2 = open("medicina.json")



# Traduções

i=0
for elem in conceitos:
    pt = GoogleTranslator(source="en", target="pt").translate(elem)
    es = GoogleTranslator(source="en", target="es").translate(elem)
    print(i)
    i+=1
    conceitos[elem]["Traduções"] = {"pt": pt + " * ", "es": es + " * ", "en": elem}

new_file = open("novo.json", "w")
json.dump(conceitos, new_file, indent=4, ensure_ascii=False) # indent para human readable 4 é arbitrario

new_file.close()

conceitos = json.load(file)   # novo em en
conceitos2 = json.load(file2) # medicina
file.close()
file2.close()

next_id = 5394   # adicionar os de web scrapping no fim
n_interseta = []
for elem in conceitos:  # 
    for id in conceitos2:
        if "r_" not in id:
            # No trabalho anterior estava em espanhol
            if elem == conceitos2[id]["Traduções"]['en']:
                conceitos2[id]["definição"] = conceitos[elem]["definicao"]
                conceitos2[id]["fonte(s)"].extend(doc for doc in conceitos[elem]["fonte(s)"])
                if "relacionado" in elem:
                    conceitos2[id]["relacionado"] = conceitos[elem]["relacionado"]
                if "sinonimos" in conceitos[elem]:
                    conceitos2[id]["sinonimos"] = conceitos[elem]["sinonimos"]
                #print(elem)


                #print(conceitos2[id]["Traduções"]['en'])
                #print("---------------")
            else:
                n_interseta.append(elem)

for termo in list(set(n_interseta)):
    conceitos2[next_id] = conceitos[termo]
    conceitos2[next_id]["Termo"] = termo
    next_id+=1

for next_id in conceitos2:
    if "r_" not in str(next_id):
        conceitos2[next_id]["Fontes"] = conceitos2[next_id]["fonte(s)"]
        del conceitos2[next_id]["fonte(s)"]
#print(conceitos2)

f_out = open("doc_conc.json","w")
json.dump(conceitos2,f_out,indent=4, ensure_ascii=False)
f_out.close()
"""
ii=0
file_in = open("doc_conc_temp.json", 'r') 

fich_conj = json.load(file_in)
dic_es = {}
dic_en = {}
dic_pt = {}



def index_termo(dic, termo):
    for index, entrada in dic.items():
        if "r_" not in index:
            if entrada["Termo"] == termo:
                return index
    return None

for entrada in fich_conj:
    dic_es[entrada] = {}
    dic_en[entrada] = {}
    dic_pt[entrada] = {}
    if "r_" not in entrada:
        dic_es[entrada]["Termo"] = fich_conj[entrada]["Traduções"]["es"]
        dic_en[entrada]["Termo"] = fich_conj[entrada]["Traduções"]["en"]
        dic_pt[entrada]["Termo"] = fich_conj[entrada]["Traduções"]["pt"]

        if "Categoria gramatical" in fich_conj[entrada]: # se houver ent há area de aplicação, pois pertence ao medicina
            dic_es[entrada]["Categoria gramatical"] = fich_conj[entrada]["Categoria gramatical"] # não faz sentido equiparar

            areas_es = fich_conj[entrada]["Área(s) de aplicação"]
            dic_es[entrada]["Área(s) de aplicação"] = areas_es
            dic_en[entrada]["Área(s) de aplicação"] = [str(GoogleTranslator(source="es", target="en").translate(area)) + ' * ' for area in areas_es]
            dic_pt[entrada]["Área(s) de aplicação"] = [str(GoogleTranslator(source="es", target="pt").translate(area)) + ' * ' for area in areas_es]

        dic_es[entrada]["Fontes"] = fich_conj[entrada]["Fontes"]
        dic_en[entrada]["Fontes"] = fich_conj[entrada]["Fontes"]
        dic_pt[entrada]["Fontes"] = fich_conj[entrada]["Fontes"]

        if "SIN" in fich_conj[entrada]:

            Sin_es = fich_conj[entrada]["SIN"]
            print(Sin_es)
            dic_es[entrada]["Sinonimos"] = [Sin_es]
            dic_en[entrada]["Sinonimos"] = [str(GoogleTranslator(source="es", target="en").translate(Sin_es)) + ' * ']
            dic_pt[entrada]["Sinonimos"] = [str(GoogleTranslator(source="es", target="pt").translate(Sin_es)) + ' * ' ]

        if "sinonimos" in fich_conj[entrada]:

            Sin_en = fich_conj[entrada]["sinonimos"]
            print(Sin_en)
            if "Sinonimos" in dic_es[entrada]:
                dic_es[entrada]["Sinonimos"].extend([str(GoogleTranslator(source="en", target="es").translate(sin)) + ' * ' for sin in Sin_en])
            else:
                dic_es[entrada]["Sinonimos"] = [str(GoogleTranslator(source="en", target="es").translate(sin)) + ' * ' for sin in Sin_en]

            if "Sinonimos" in dic_pt[entrada]:
                dic_pt[entrada]["Sinonimos"].extend([str(GoogleTranslator(source="en", target="pt").translate(sin)) + ' * ' for sin in Sin_en])
            else:
                dic_pt[entrada]["Sinonimos"] = [str(GoogleTranslator(source="en", target="pt").translate(sin)) + ' * ' for sin in Sin_en]

            if "Sinonimos" in dic_en[entrada]:
                dic_en[entrada]["Sinonimos"].extend(Sin_en)
            else:
                dic_en[entrada]["Sinonimos"] = Sin_en
        
        if "definição" in fich_conj[entrada]:

            def_en = fich_conj[entrada]["definição"]
            dic_en[entrada]["Definicao"] = def_en
            dic_es[entrada]["Definicao"] = str(GoogleTranslator(source="en", target="es").translate(def_en)) + ' * '
            dic_pt[entrada]["Definicao"] = str(GoogleTranslator(source="en", target="pt").translate(def_en)) + ' * '

        if "VAR" in fich_conj[entrada]:
            dic_es[entrada]["Variante"] = fich_conj[entrada]["VAR"] # não faz sentido traduzir
    
    
    else: # entradas remissivas

        entrada_rem = fich_conj[entrada]
        chave = list(entrada_rem.keys())[0]
        ref = list(entrada_rem.values())
        ref = ref[0].replace("Vid.- ","")

        
        index_ref = index_termo(fich_conj,ref)

        dic_es[entrada]["Termo"] = chave
        try:
            dic_en[entrada]["Termo"] = GoogleTranslator(source="es", target="en").translate(chave) + ' * '
        except:
            dic_en[entrada]["Termo"] = chave
        try:
            dic_pt[entrada]["Termo"] = GoogleTranslator(source="es", target="pt").translate(chave) + ' * '
        except:
            dic_pt[entrada]["Termo"] = chave

        dic_es[entrada]["Index_Remissivo"] = index_ref
        dic_en[entrada]["Index_Remissivo"] = index_ref
        dic_pt[entrada]["Index_Remissivo"] = index_ref

    if (len(list(dic_en.keys())) % 100) == 0:                   # a cada 100 gravar

        f_out_es = open("doc_conc_es.json","w")  #es
        f_out_en = open("doc_conc_en.json","w") #en
        f_out_pt = open("doc_conc_pt.json","w")

        json.dump(dic_es,f_out_es,indent=4, ensure_ascii=False)
        json.dump(dic_en,f_out_en,indent=4, ensure_ascii=False)
        json.dump(dic_pt,f_out_pt,indent=4, ensure_ascii=False)

        f_out_es.close()
        f_out_en.close()
        f_out_pt.close()

        f_out_temp = open("doc_conc_temp.json","w")
        valores_faltam = {key: value for key, value in fich_conj.items() if key not in dic_es}
        json.dump(valores_faltam,f_out_temp,indent=4, ensure_ascii=False)
        f_out_temp.close()
    print(ii)
    ii+=1
f_out_es = open("doc_conc_es.json","w")  #es
f_out_en = open("doc_conc_en.json","w") #en
f_out_pt = open("doc_conc_pt.json","w")

json.dump(dic_es,f_out_es,indent=4, ensure_ascii=False)
json.dump(dic_en,f_out_en,indent=4, ensure_ascii=False)
json.dump(dic_pt,f_out_pt,indent=4, ensure_ascii=False)


f_out_es.close()
f_out_en.close()
f_out_pt.close()
#print(repetidos)
