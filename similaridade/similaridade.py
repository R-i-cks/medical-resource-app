from gensim.models import Word2Vec
from gensim.utils import tokenize
import json
import numpy as np
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
stopPT = set(stopwords.words('portuguese'))
stopES = set(stopwords.words('spanish'))
stopEN = set(stopwords.words('english'))

with open('../fusao_dados/doc_conc_es.json', 'r', encoding='UTF-8') as f1, \
     open('../fusao_dados/doc_conc_en.json', 'r', encoding='UTF-8') as f2, \
     open('../fusao_dados/doc_conc_pt.json', 'r', encoding='UTF-8') as f3:

    es = json.load(f1)
    en = json.load(f2)
    pt = json.load(f3)


modelEN = Word2Vec.load("modeloEN.w2v")
modelES = Word2Vec.load("modeloES.w2v")
modelPT = Word2Vec.load("modeloPT.w2v")

def get_mean_vector(text, model, stop_words):
    tokens = list(tokenize(text, lower=True))
    vectors = [model.wv[token] for token in tokens if token not in stop_words and token in model.wv]
    if not vectors:  # If vectors list is empty
        return np.zeros(model.vector_size)
    mean = np.mean(vectors, axis=0)
    return mean


def cosine(v1, v2):
    return np.dot(v1,v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def adicionaRelacionados(dicionario, idioma):
    if idioma == 'pt':
        model = modelPT
        stopwords = stopPT
    elif idioma == 'en':
        stopwords = stopEN
        model = modelEN
    elif idioma == 'es':
        stopwords = stopES
        model = modelES
    
    for indice in list(dicionario.keys()):
        print(indice, idioma)
        sims = []
        query = get_mean_vector(dicionario[indice]['Termo'].replace('*', ''), model, stopwords)
        for indicej in dicionario:
            termo =  get_mean_vector(dicionario[indicej]['Termo'].replace('*', ''), model, stopwords)
            sim = cosine(query,termo)
            sims.append((dicionario[indicej]['Termo'],sim))
        sorted_sims = sorted(sims,key=lambda x : x[1], reverse=True)
        dicionario[indice]['Relacionado'] = [termo for termo, sim in sorted_sims[:5]]

    return (dicionario)

en = adicionaRelacionados(en, 'en')
es = adicionaRelacionados(es, 'es')
pt = adicionaRelacionados(pt, 'pt')

with open("doc_conc_es_novo.json", "w", encoding='UTF-8') as f_out_es, \
     open("doc_conc_en_novo.json", "w", encoding='UTF-8') as f_out_en, \
     open("doc_conc_pt_novo.json", "w", encoding='UTF-8') as f_out_pt:

    json.dump(es, f_out_es, indent=4, ensure_ascii=False)
    json.dump(en, f_out_en, indent=4, ensure_ascii=False)
    json.dump(pt, f_out_pt, indent=4, ensure_ascii=False)
