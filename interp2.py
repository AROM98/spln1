#! python3

from getopt import getopt
import re
import sys
import types
import json
from pprint import pprint

from soupsieve import match

 ######### GRUPO 4 ############

with open("sample.json") as f:
    data = json.load(f)

domain = []
trads = []
etc = []
idTriple = []


dicPalavras = {}
dicTraducoes = {}
dicInformacao = {}
dicDominios = {}



for i in range(len(data)):
    #adiciono o nome em galego a traduções
    data[i]['traducoes']['gl'] = [data[i]['termo']]

    #Palavras-ID
    '''
            aqui preciso tratar as palavras que ficam no dic,
            remover espaços a mais, substituir caracteres com acentos por caracteres sem acentos
            e dar lower da palavra
            '''
    for listPalavra in data[i]['traducoes'].values():
        for palavra in listPalavra:
            dicPalavras[palavra] = data[i]['id']


    #ID-Traduções
    dicTraducoes[data[i]['id']] = data[i]['traducoes']

    #ID-Dominio
    '''
    preciso no parse tratar dos domínios que não estão separados
    '''
    dicDominios[data[i]['id']] = data[i]['dominio']
    
    
    #ID-informação detalhada
    '''
    tratar casos de ser [] FALAPE
    '''
    aux = []
    aux.append(data[i]['dominio'])
    aux.append(data[i]['traducoes'])
    if(len(data[i]['etc'])!=0):
        aux.append(data[i]['etc'])

    dicInformacao[data[i]['id']]=aux


#lang: devolve termo na língua correspondente
def getTraducao(palavra, flagTraducao):
    id = -1
    traducoes = []
    try:
        id = dicPalavras[palavra]
        traducoes = dicTraducoes[id]
        if(flagTraducao == ''):
            '''
            Por prints mais bonitos
            '''
            pprint(traducoes)
        else:
            tradu=  traducoes[flagTraducao]#obtém a tradução desejada, passada pela flag
            listPrint = 'Tradução de ' + palavra + ' para ' + flagTraducao +':'
            for i in range(len(tradu)):
                listPrint += '\n--'+ str(tradu[i]) +'\n'

            print(listPrint)
    except Exception as e:
        print("Palavra não existe:", e)


#verbose: devolve informação detalhada
def getInfoDetalhada(palavra):
    id = -1
    infodetalhada = ''
    try:
        id = dicPalavras[palavra]
        infodetalhada = dicInformacao[id]
        print(infodetalhada)
    except Exception as e:
        print("Palavra não existe")
    


#domínio: devolve termos do domínio
def getDominio(palavra):
    id = -1
    dominio = ''
    try:
        id = dicPalavras[palavra]
        dominio = dicDominios[id]
        print(dominio)
    except Exception as e:
        print("Palavra não existe")
   



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
        print("###############")
        print(count)
        print(dicTraducoes[i])
        print('Dominio da Palavra:')
        print(dicDominios[i])
        count += 1


    #print(results)



ops,args = getopt(sys.argv[1:],"l:vdp:h", ["lang", "verbose", "dominio", "prefixo", "help"])
ops = dict(ops)


if '-l' in ops:
    if(ops['-l']=='pt'):
        getTraducao(sys.argv[3],'pt')
    elif(ops['-l']=='es'):
        getTraducao(sys.argv[3],'es')
    elif(ops['-l']=='en'):
        getTraducao(sys.argv[3],'en')
    elif(ops['-l']=='gl'):
        getTraducao(sys.argv[3],'gl')
    else: 
        getTraducao(sys.argv[2],'')
elif '-v' in ops:
    print('função verbose')
    getInfoDetalhada(sys.argv[2])
elif '-d' in ops:
    print('função dominio')
    getDominio(sys.argv[2])
elif '-p' in ops:
    print('funcao prefixo')
    getFromPrefixo(sys.argv[2])
elif '-h' in ops:
    print('''
        HELP MENU
        
        Opções disponiveis:

        -l Palavra : Caso não for indicado lingua, imprime todas.

        -l [pt, es, en, gl] Palavra : A palavra é traduzida para a lingua indicada pela flag.
                                      pt = Portugues, es = Espanhol, en = ingles, gl = galego.

        -v Palavra : Modo verbose, devolve informação detalhada sobre a palavra.

        -d Palavra : Devolve o dominio no qual a palavra se insere.

        -p Prefixo : Devolve informação de uma ou mais palavras com o prefixo indicado.

        -h : Menu de Ajuda.
        
        SPLN@2022
        ''')
else:
    print('erro: opção escolhida não existe')

#getTraducao(sys.argv[1],'es')
#getInfoDetalhada(sys.argv[1])
#getDominio(sys.argv[1])
#getFromPrefixo(sys.argv[1])
