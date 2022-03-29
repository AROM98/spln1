#! python3

import getopt
import re
import sys
import types
import json
from pprint import pprint

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
            for i in range(len(tradu[1])):
                listPrint += '\n--'+ str(tradu[1][i]) +'\n'

            print(listPrint)
    except Exception as e:
        print("Palavra não existe")


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
        print(count)
        print(dicTraducoes[i])
        print('Dominio da Palavra:')
        print(dicDominios[i])
        count += 1


    #print(results)

getTraducao(sys.argv[1],'es')
#getInfoDetalhada(sys.argv[1])
#getDominio(sys.argv[1])
#getFromPrefixo(sys.argv[1])
