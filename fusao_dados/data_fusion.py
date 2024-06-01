import json
from deep_translator import GoogleTranslator

#file = open("conceitos_rel_sin_trad.json")
file = open("novo.json")
file2 = open("medicina.json")



# Traduções
""" 
i=0
for elem in conceitos:
    pt = GoogleTranslator(source="en", target="pt").translate(elem)
    es = GoogleTranslator(source="en", target="es").translate(elem)
    print(i)
    i+=1
    conceitos[elem]["Traduções"] = {"pt": pt + " * ", "es": es + " * ", "en": elem}

new_file = open("novo.json", "w")
json.dump(conceitos, new_file, indent=4, ensure_ascii=False) # indent para human readable 4 é arbitrario

new_file.close()"""

conceitos = json.load(file)   # novo
conceitos2 = json.load(file2) # medicina
file.close()
file2.close()

next_id = 5394   # adicionar os de web scrapping no fim
n_interseta = []
for elem in conceitos:  # 
    for id in conceitos2:
        if "r_" not in id:
            if elem == conceitos2[id]["Traduções"]['en']:
                conceitos2[id]["definição"] = conceitos[elem]["definicao"]
                conceitos2[id]["fonte(s)"].extend(doc for doc in conceitos[elem]["fonte(s)"])
                if "relacionado" in elem:
                    conceitos2[id]["relacionado"] = conceitos[elem]["relacionado"]
                if "sinonimos" in conceitos[elem]:
                    conceitos2[id]["SIN"] = conceitos[elem]["sinonimos"]
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
#print(repetidos)
