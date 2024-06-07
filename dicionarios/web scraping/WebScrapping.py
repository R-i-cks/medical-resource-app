import json
from bs4 import BeautifulSoup
import requests

# -------------------------- HONOR HEALTH --------------------------------

"""
dicionario = {}

url = "https://www.honorhealth.com/patients-visitors/average-pricing/medical-glossary"
pag = requests.get(url)
html = pag.text
soup = BeautifulSoup(html, 'html.parser')
tabelas = soup.find_all('table')

for tabela in tabelas:
    termos = tabela.find_all('tr')
    for t in termos:
        termo = t.find_all('td')
        conceito = termo[0].text
        definicao = termo[1].text
        dicionario[conceito.strip()] = {'definicao' : definicao.strip(), 'fonte(s)' : ['Honor Health']}


# -------------------------- HEALTH CAREERS --------------------------------


url = "https://www.healthcareers.nhs.uk/glossary"
pag = requests.get(url)
html = pag.text
soup = BeautifulSoup(html, 'html.parser')
listas = soup.find_all('dl')

for l in listas:
    termos = l.find_all('dt')
    definicoes = l.find_all('dd')
    for i in range(len(termos)):
        if termos[i].text.strip() not in dicionario:
            dicionario[termos[i].text.strip()] =  {'definicao' : definicoes[i].text.strip(),'fonte(s)' : ['Health Careers']}
        else:
            dicionario[termos[i].text.strip()]['definicao'] += f' {definicoes[i].text.strip()}'
            if 'Health Careers' not in dicionario[termos[i].text.strip()]['fonte(s)']:
                dicionario[termos[i].text.strip()]['fonte(s)'].append('Health Careers') 


# -------------------------- HARVARD MEDICAL SCHOOL --------------------------------

links_harvard = ['https://www.health.harvard.edu/a-through-c', 
                 'https://www.health.harvard.edu/d-through-i',
                 'https://www.health.harvard.edu/j-through-p',
                 'https://www.health.harvard.edu/q-through-z']


for url in links_harvard:
    pag = requests.get(url)
    html = pag.text
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('div', class_="content-repository-content prose max-w-md-lg mx-auto flow-root getShouldDisplayAdsAttribute")        
    paragrafos = tabela.find_all('p')

    for p in paragrafos:
        if '<strong>' in str(p) and 'class' not in str(p):
            info = p.text.split(': ')
            termo = info[0]
            significado = ""
            for i in range(1,len(info)):
                significado += info[i]
            
            if termo.strip() not in dicionario:
                dicionario[termo.strip()] =  {'definicao' : significado.strip(),'fonte(s)' : ['Harvard Medical School']}
            else:
                dicionario[termo.strip()]['definicao'] += f' {significado.strip()}'
                if 'Harvard Medical School' not in dicionario[termo.strip()]['fonte(s)']:
                    dicionario[termo.strip()]['fonte(s)'].append('Harvard Medical School')

# -------------------------- Great Ormond Street Hospital (GOSH) --------------------------------

url='https://www.gosh.nhs.uk/conditions-and-treatments/health-dictionary/health-dictionary-'
letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n','o','p','q','r','s', 't', 'u','v','x','y', 'z']
links_GOSH = [f'{url + letra}' for letra in letras]

for url in links_GOSH:
    pag = requests.get(url)
    html = pag.text
    soup = BeautifulSoup(html, 'html.parser')
    coluna = soup.find('div', class_="wrapper column-layout")     
    tabela = coluna.find('section')        
    termos = tabela.find_all('h3', class_="sf-heading")
    definicoes = tabela.find_all('div', class_="rich-text")
    for i in range(0, len(termos)):
        if termos[i].text.strip() not in dicionario:
            dicionario[termos[i].text.strip()] =  {'definicao' : definicoes[i].p.text.strip(),'fonte(s)' : ['Great Ormond Street Hospital (GOSH)']}
        else:
            dicionario[termos[i].text.strip()]['definicao'] += f' {definicoes[i].p.text.strip()}'
            if 'Harvard Medical School' not in dicionario[termos[i].text.strip()]['fonte(s)']:
                dicionario[termos[i].text.strip()]['fonte(s)'].append('Great Ormond Street Hospital (GOSH)')


file_out= open(r"conceitos.json","w",encoding='utf-8')
json.dump(dicionario,file_out,ensure_ascii=False,indent=4)
file_out.close()

# -------------------------- ADICIONAR RELACIONADOS --------------------------------


f = open("conceitos.json","r",encoding='utf-8')
dicionario = json.load(f)
print(len(dicionario))

chaves = [x.lower() for x in dicionario]
stopwords = ['no', ]
for termo in dicionario:
    for palavra in dicionario[termo]['definicao'].split(" "):
        if palavra.lower() in chaves:
            if 'relacionado' in dicionario[termo]:
                if palavra not in dicionario[termo]['relacionado'] and palavra != termo and palavra.lower() not in ['no', 'will']:
                    dicionario[termo]['relacionado'].append(palavra)
            else:
                if palavra != termo and palavra.lower() not in ['no', 'will']:
                    dicionario[termo]['relacionado'] = [palavra]

file_out= open(r"conceitos_e_relacoes.json","w",encoding='utf-8')
json.dump(dicionario,file_out,ensure_ascii=False,indent=4)
file_out.close()



# -------------------------- ADICIONAR SINONIMOS DO THESAURUS --------------------------------


f = open("conceitos_e_relacoes.json","r",encoding='utf-8')
dicionario = json.load(f)
print(len(dicionario))

url = "https://www.thesaurus.com/browse/"

for p in dicionario:
    novo_url = url+p
    try:

        pag = requests.get(novo_url)
        html = pag.text
        soup = BeautifulSoup(html, 'html.parser')
        s = soup.find('div', class_="flol7HNuPRe9VfZ0KeMZ")
        if s:
            sinonimos = s.find_all('li')
            for sinonimo in sinonimos:
                print(p, sinonimo.text)
                if 'sinonimos' in dicionario[p]:
                    dicionario[p]['sinonimos'].append(sinonimo.text)
                else:
                    dicionario[p]['sinonimos'] = [sinonimo.text]
    except:
        print('nao conseguiu')
    print(list(dicionario.keys()).index(p)/len(dicionario)*100)


file_out= open(r"conceitos_relacoes_e_sinonimos.json","w",encoding='utf-8')
json.dump(dicionario,file_out,ensure_ascii=False,indent=4)
file_out.close()

"""
