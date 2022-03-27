#! python3

import getopt
import re
import sys
import types
from pprint import pprint

 ######### GRUPO 4 ############

#from black import mask_cell
with open("medicina.xml") as f:
    content = f.read()

# remover elementos vazios
content = re.sub(r"<(\w+)>\s+</\1>","",content)

# remover páginas desnecessárias
content = re.sub(r".*<page number=\"20\" [^>]*>","",content,flags=re.S,count=1)
content = re.sub(r"<page number=\"544\".*","",content,flags=re.S,count=1)

content = re.sub(r'<text top=\"862\"[^>]*>.*?</text>',"",content)

content = re.sub(r"<text[^>]*>(.*?)</text>",r"\1",content,flags=re.S)

content = re.sub(r"<page[^>]*>","",content)
content = re.sub(r"</page>","",content)
content = re.sub(r"<fontspec[^>]*>","",content)

content = re.sub(r"\n[ \t]*\n","\n",content)
content = re.sub(r"V\nocabulario","",content)

def clean(dirty_text):
    return re.sub(r'\n|</?i>', "", dirty_text).strip()

def info_split(info):
    return re.split(r'\s*;\s*', info)

def processEntry(entry : str):
    c = re.split(r'</b>',entry,maxsplit=1)
    m = re.fullmatch("\s*(\d+)\s*(.*?)\s*(\w+)", c[0])
    idTriple =  ''
    if m:
        idTriple = m.groups()
    else:
        idTriple = c[0].strip()
    info = re.sub(r'\b(en|pt|es|ls)\b', r'@@@\1', c[1])
    info = re.sub(r'((?:SIN|Nota|VAR|)\.-)', r'€€€\1', info)

    domain =  re.split(r'\s[2,]|\t',   clean(re.findall(r'[^@€]*', info)[0].strip()))
    trads = [(x[0],info_split(clean(x[1]))) for x in re.findall(r'@@@(\w+)([^@€]*)', info)]
    etc = [(x[0],info_split(clean(x[1]))) for x in re.findall(r'€€€(\w+)\.-([^@€]*)', info)]

    for elem in domain:
        domainf = re.split(r'\s{2,}', elem)



    return [domainf,trads,etc,idTriple]

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

domain = []
trads = []
etc = []
idTriple = []
for entry in re.split(r'<b>', content)[1:]:
    aux = processEntry(entry)
    domain.append(aux[0])
    trads.append(aux[1])
    etc.append(aux[2])
    idTriple.append(aux[3])

#print(len(domain))
#print(len(trads))
#print(len(etc))
#print(len(idTriple))


dicPalavras = {}
dicTraducoes = {}
dicInformacao = {}
dicDominios = {}

for i in range(len(domain)):
    if(domain[i][0] == 'Vid' or domain[i][0] == ''):
        continue
    #print(domain[i])
    if(type(idTriple[i])==type('')):
        continue

    #print(idTriple[i])
    #print(domain[i])
    #print(trads[i])
    #print(etc[i])

    tuplo = ('gl',[idTriple[i][1]]) #crio tuplo com 'gl' e o nome galego
    trads[i].append(tuplo) #adiciono o nome em galego a trads


    #####Preencher estruturas apartir daqui######

    #ID-Traduções
    dicTraducoes[int(idTriple[i][0])] = trads[i]

    #Palavras-ID
    for j in range(len(trads[i])):  # [('es',['nome1']), ('en',['nome2', 'nome3'])] -> ('en',['nome2', 'nome3'])
        for k in range(len(trads[i][j][1])): #('en',['nome2', 'nome3']) -> 'nome2'
            '''
            aqui preciso tratar as palavras que ficam no dic,
            remover espaços a mais, substituir caracteres com acentos por caracteres sem acentos
            e dar lower da palavra
            '''
            dicPalavras[trads[i][j][1][k]] = int(idTriple[i][0])

    #ID-informação detalhada
    '''
    tratar casos de ser [] FALAPE
    '''
    aux = []
    aux.append(domain[i])
    aux.append(trads[i])
    aux.append(etc[i])

    dicInformacao[int(idTriple[i][0])] = aux



    #ID-Domínio
    '''
    preciso no parse tratar dos domínios que não estão separados
    '''
    dicDominios[int(idTriple[i][0])] = domain[i]

#print(dicTraducoes)
#print(dicPalavras)

#lang: devolve termo na língua correspondente
def getTraducao(palavra, flagTraducao):
    id = -1
    traducoes = []
    try:
        id = dicPalavras[palavra]
        traducoes = dicTraducoes[id]
    except Exception as e:
        print("Palavra não existe")


    if(flagTraducao == ''):
        '''
        Por prints mais bonitos
        '''
        pprint(traducoes)
    else:
        tradu= list(filter(lambda a: a[0]==flagTraducao, traducoes))[0] #obtém a tradução desejada, passada pela flag
        listPrint = 'Tradução de ' + palavra + ' para ' + flagTraducao +':'
        for i in range(len(tradu[1])):
            listPrint += '\n--'+ str(tradu[1][i]) +'\n'

        print(listPrint)


#verbose: devolve informação detalhada
def getInfoDetalhada(palavra):
    id = -1
    infodetalhada = ''
    try:
        id = dicPalavras[palavra]
        infodetalhada = dicInformacao[id]
    except Exception as e:
        print("Palavra não existe")
    print(infodetalhada)


#domínio: devolve termos do domínio
def getDominio(palavra):
    id = -1
    dominio = ''
    try:
        id = dicPalavras[palavra]
        dominio = dicDominios[id]
    except Exception as e:
        print("Palavra não existe")
    print(dominio)



#preﬁxo: devolve termos que começam com preﬁxo.
def getFromPrefixo(palavra):
    results = []

    #lista de IDs das palavras que têm o prefixo
    resultUntreated = [dicPalavras[key] for key in dicPalavras.keys() if key.startswith(palavra)]

    #remover ID's repetidos
    [results.append(x) for x in resultUntreated if x not in results]


    '''
    Não sei bem o que posso devolver
    '''
    print('Matchs:')
    count = 1
    for i in results:
        print(count)
        print(dicTraducoes[i])
        print('Dominio da Palavra:')
        print(dicDominios[i])
        count += 1


    #print(results)

#getTraducao(sys.argv[1],'es')
#getInfoDetalhada(sys.argv[1])
#getDominio(sys.argv[1])
getFromPrefixo(sys.argv[1])
