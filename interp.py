#! python3

import getopt
import re
import sys

 ######### GRUPO 4 ############

#from black import mask_cell

ops,args = getopt(sys.argv[1:],"l:vdp:", ["lang", "verbose", "domminio", "prefixo"])
ops = dict(ops)


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
    if m:
        print(m.groups())
    else:
        print(c[0].strip())
    info = re.sub(r'\b(en|pt|es|ls)\b', r'@@@\1', c[1])
    info = re.sub(r'((?:SIN|Nota|VAR|)\.-)', r'€€€\1', info)

    domain =  re.split(r'\s[2,]|\t',   clean(re.findall(r'[^@€]*', info)[0].strip()))
    trads = [(x[0],info_split(clean(x[1]))) for x in re.findall(r'@@@(\w+)([^@€]*)', info)]
    etc = [(x[0],info_split(clean(x[1]))) for x in re.findall(r'€€€(\w+)\.-([^@€]*)', info)]

    for elem in domain:
        domainf = re.split(r'\s{2,}', elem)
    
    print("&&&&&&",domainf)
    print("@",trads)
    print("€", etc)

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
for entry in re.split(r'<b>', content)[1:]:
    processEntry(entry)

