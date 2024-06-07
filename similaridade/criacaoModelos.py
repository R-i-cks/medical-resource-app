from gensim.models import Word2Vec
from gensim.utils import tokenize
import json
import numpy as np
from nltk.corpus import stopwords
import nltk
import re
"""
# --------------- ELIMINAR O QUE NAO FAZ SENTIDO ------------------------

with open('similaridade/Livro-de-Resumos-2024.xml', 'r', encoding='UTF-8') as f1:
    texto = f1.read()


texto = re.sub(r'<(image|fontspec|page).+?>', r'', texto)
texto = re.sub(r'.+height=\"14\" font=\"4\".+', r'', texto)
texto = re.sub(r'.+Código:.+', r'@@@@@', texto)
texto = re.sub(r'.+(P á g i n ).+', r'', texto)
texto = re.sub(r'(\n)+', r'\n', texto)
texto = re.sub(r'<.+?>', r'', texto)

with open('similaridade/Livro-de-Resumos-2024_novo.xml', 'w', encoding='UTF-8') as f1:
    f1.write(texto)

"""
# --------------- CRIAR MODELO ------------------------


nltk.download('stopwords')
stopwords = set(stopwords.words('portuguese'))


def getTokens(texto):    
    tokens = []
    frases = texto.split('. ')
    for frase in frases:
        f = list(tokenize(frase, lower=True))
        tokens.append(f)

    return tokens



with open('similaridade/Livro-de-Resumos-2024.xml', 'r', encoding='UTF-8') as f1:
    texto = f1.read()


tokens = getTokens(texto)
modelo = Word2Vec(tokens, min_count=1, vector_size=300, epochs=20)

modelo.save("modelo.w2v")


