import json
from deep_translator import GoogleTranslator

# Abrir arquivos JSON
with open('doc_conc_es.json', 'r', encoding='UTF-8') as f1, \
     open('doc_conc_en.json', 'r', encoding='UTF-8') as f2, \
     open('doc_conc_pt.json', 'r', encoding='UTF-8') as f3, \
     open('conceitosGMS.json', 'r', encoding='UTF-8') as f4:

    es = json.load(f1)
    en = json.load(f2)
    pt = json.load(f3)
    gms = json.load(f4)

dicionario = {}
indice_global = 7905

def adicionaTermo(info, termo, dicionario, idioma, indice_global):
    if termo.lower() in (entry['Termo'].replace('*', '').strip().lower() for entry in dicionario.values()):
        print('estava', termo)
        for indice, entry in dicionario.items():
            if termo.lower() in entry['Termo'].replace('*', '').strip().lower():
                if 'Descrição' in info:
                    descricao = info['Descrição'] if idioma == 'pt' else GoogleTranslator(source="pt", target=idioma).translate(info['Descrição'])
                    if 'Definicao' in entry:
                        entry['Definicao'] += f' {descricao} *'
                    else:
                        entry['Definicao'] = f'{descricao} *'
                    entry['Fontes'] = entry.get('Fontes', []) + ['Glossário do Ministério da Saúde']
                if 'Categoria' in info:
                    categorias = info['Categoria']
                    if idioma != 'pt':
                        categorias = [GoogleTranslator(source="pt", target=idioma).translate(c) for c in categorias]
                    entry['Categoria'] = entry.get('Categoria', []) + [f'{cat} *' for cat in categorias]
                break
    else:
        print('nao estava', termo)
        dicionario[str(indice_global)] = {'Termo': f'{termo} *'}
        if 'Descrição' in info:
            descricao = info['Descrição'] if idioma == 'pt' else GoogleTranslator(source="pt", target=idioma).translate(info['Descrição'])
            dicionario[str(indice_global)]['Definicao'] = f'{descricao} *'
            dicionario[str(indice_global)]['Fontes'] = ['Glossário do Ministério da Saúde']
        if 'Categoria' in info:
            categorias = info['Categoria']
            if idioma != 'pt':
                categorias = [GoogleTranslator(source="pt", target=idioma).translate(c) for c in categorias]
            dicionario[str(indice_global)]['Categoria'] = [f'{cat} *' for cat in categorias]
        indice_global += 1
    
    return dicionario, indice_global



for termo in gms:
    
    print('GMS', termo)

    termoen = GoogleTranslator(source="pt", target="en").translate(termo)
    termoes = GoogleTranslator(source="pt", target="es").translate(termo)

    pt, indice_global = adicionaTermo(gms[termo], termo, pt, 'pt', indice_global)
    en, indice_global = adicionaTermo(gms[termo], termoen, en, 'en', indice_global)
    es, indice_global = adicionaTermo(gms[termo], termoes, es, 'es', indice_global)


with open("doc_conc_es.json", "w", encoding='UTF-8') as f_out_es, \
     open("doc_conc_en.json", "w", encoding='UTF-8') as f_out_en, \
     open("doc_conc_pt.json", "w", encoding='UTF-8') as f_out_pt:

    json.dump(es, f_out_es, indent=4, ensure_ascii=False)
    json.dump(en, f_out_en, indent=4, ensure_ascii=False)
    json.dump(pt, f_out_pt, indent=4, ensure_ascii=False)
