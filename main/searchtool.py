import pygtrie
import os

def gettrie():
    path=os.path.dirname(os.path.realpath(__file__))
    forg = open(path+'/../ORGNAME.txt', encoding='utf-8')
    names = []
    line=forg.readline()
    line=forg.readline()
    while line:
        names.append(line[1:-2])
        line=forg.readline()
    forg.close()

    fperson = open(path+'/../PERSONNAME.txt', encoding='utf-8')
    line=fperson.readline()
    line=fperson.readline()
    while line:
        names.append(line[1:-2])
        line=fperson.readline()
    fperson.close()

    trie = pygtrie.StringTrie()
    for name in names:
        namelist = list(name)
        prefix = '/'.join(namelist)
        trie[prefix]=name
    return trie

def getname():
    path=os.path.dirname(os.path.realpath(__file__))
    forg = open(path+'/../ORGNAME.txt', encoding='utf-8')
    names = []
    line=forg.readline()
    line=forg.readline()
    while line:
        names.append(line[1:-2])
        line=forg.readline()
    forg.close()

    fperson = open(path+'/../PERSONNAME.txt', encoding='utf-8')
    line=fperson.readline()
    line=fperson.readline()
    while line:
        names.append(line[1:-2])
        line=fperson.readline()
    fperson.close()
    return names

def getorgname():
    path=os.path.dirname(os.path.realpath(__file__))
    forg = open(path+'/../ORGNAME.txt', encoding='utf-8')
    names = []
    line=forg.readline()
    line=forg.readline()
    while line:
        names.append(line[1:-2])
        line=forg.readline()
    forg.close()

    return names
