import json
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
content = re.sub(r"<(\w+)>\s+</\1>", "", content)

# remover páginas desnecessárias
content = re.sub(
    r".*<page number=\"20\" [^>]*>", "", content, flags=re.S, count=1)
content = re.sub(r"<page number=\"544\".*", "", content, flags=re.S, count=1)

content = re.sub(r'<text top=\"862\"[^>]*>.*?</text>', "", content)

content = re.sub(r"<text[^>]*>(.*?)</text>", r"\1", content, flags=re.S)

content = re.sub(r"<page[^>]*>", "", content)
content = re.sub(r"</page>", "", content)
content = re.sub(r"<fontspec[^>]*>", "", content)

content = re.sub(r"\n[ \t]*\n", "\n", content)
content = re.sub(r"V\nocabulario", "", content)


def clean(dirty_text):
    return re.sub(r'\n|</?i>', "", dirty_text).strip()


def info_split(info):
    return re.split(r'\s*;\s*', info)


def processEntry(entry: str):
    c = re.split(r'</b>', entry, maxsplit=1)
    m = re.fullmatch("\s*(\d+)\s*(.*?)\s*(\w+)", c[0])
    idTriple = ''
    if m:
        idTriple = m.groups()
    else:
        idTriple = c[0].strip()
    info = re.sub(r'\b(en|pt|es|ls)\b', r'@@@\1', c[1])
    info = re.sub(r'((?:SIN|Nota|VAR|)\.-)', r'€€€\1', info)

    domain = re.split(r'\s[2,]|\t',   clean(
        re.findall(r'[^@€]*', info)[0].strip()))
    trads = [(x[0], info_split(clean(x[1])))
             for x in re.findall(r'@@@(\w+)([^@€]*)', info)]
    etc = [(x[0], info_split(clean(x[1])))
           for x in re.findall(r'€€€(\w+)\.-([^@€]*)', info)]

    for elem in domain:
        domainf = re.split(r'\s{2,}', elem)

    return [domainf, trads, etc, idTriple]


# to json
toJson = []
commaFlag=False
with open("sample.json", 'w') as file:
    file.write('[')
    for entry in re.split(r'<b>', content)[1:]:
        aux = processEntry(entry)

        if(aux[0][0] == 'Vid' or aux[0][0] == ''):
            continue
        # print(domain[i])
        if(type(aux[3]) == type('')):
            continue

        if commaFlag:
            file.write(',')

        # print(aux[3])
        termo = {
            "id": aux[3][0],
            "termo": aux[3][1],
            "tr": aux[3][2],
            "dominio": aux[0],
            "traducoes": dict(aux[1]),
            "etc": aux[2]
        }

     # print(termo)
        file.write(json.dumps(termo, indent=4))
        commaFlag=True
        #json.dump(toJson, file, indent=4, sort_keys=True)

    file.write(']')
file.close()


# jsonToWrite = json.dumps(, indent = 4)
# print(jsonToWrite)

    
# file.write(jsonToWrite)

'''
[
{
"id":21,
"termo": "galeno",
"tr":"f",
"Dominio" : ["cenas","cenas2"],
"traducoes": {
"en":"termo",
"es":"termo1",
"pt":"termo2",
"lt":"termo3"
},
"Extra": "cenas"
},
{
"id":24,
"termo": "galeno",
"tr":"f",
"Dominio" : ["cenas","cenas2"],
"traducoes": {
"en":"termo",
"es":"termo1",
"pt":"termo2",
"lt":"termo3"
},
"Extra": "cenas"
}
]
'''
