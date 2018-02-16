#!/usr/bin/python

from urllib.request import urlopen
import re
import pickle
import numpy as np

def GetSchemes():

    fivebipstr = urlopen('http://www.uwyo.edu/jwilliford/data/qbip5_table.html').read().decode('utf-8')
    fivebip = re.findall(r'<\d+,\d+>',fivebipstr)

    fourbipstr = urlopen('http://www.uwyo.edu/jwilliford/data/qbip4_table.html').read().decode('utf-8')
    fourbip = re.findall(r'<\d+,\d+>',fourbipstr)

    threeprimstr = urlopen('http://www.uwyo.edu/jwilliford/data/qprim3_table.html').read().decode('utf-8')
    threeprim = re.findall(r'<\d+,\d+>',threeprimstr)

    Associationschemes = {3:threeprim,4:fourbip,5:fivebip}

    pickle.dump(Associationschemes,open("schemes.p","wb"))
    return

def Schemeparams(v,m,d):
    # This function searches through Willifords tables to find the parameters of the d-class Q-poly scheme
    # with v vertices and multiplicity m. 

    base = {3:'http://www.uwyo.edu/jwilliford/data/qprim3/qpd3',
    4:'http://www.uwyo.edu/jwilliford/data/qbip4/qbd4',
    5:'http://www.uwyo.edu/jwilliford/data/qbip5/qbd5'}

    schemetxt = urlopen(base[d]+'v'+str(v)+'m'+str(m)+'.txt').read().decode('utf-8')
    
    Ptxt = re.search(r'P[\s\w]*=[\s\w\[\]\-,]*\n\n',schemetxt)
    Prows = re.findall(r'\d[\s\d\-]*\d',Ptxt[0].replace('\n',''))
    P = np.array([[int(num) for num in Prows[i].split()] for i in range(4)])
    
    Qtxt = re.search(r'Q[\s\w]*=[\s\w\[\]\-,/]*\n\n',schemetxt)
    Qrows = re.findall(r'\d[\s\d\-]*\d',Qtxt[0].replace('\n',''))
    Q = np.array([[int(num) for num in Qrows[i].split()] for i in range(4)])

    Ltxt = re.search(r'L[\s\w]*=[\s\w\[\]\-,]*\]\n\n',schemetxt)
    Lrows = re.findall(r'\d[\s\d\-]*\d',Ltxt[0].replace('\n',''))
    L = np.array([[[int(num) for num in Lrows[i].split()] for i in range(4*j,4*(j+1))] for j in range(4)])

    Lstxt = re.search(r'L\*[\s\w]*=[\s\w\[\]\-,/]*\](\n\n|$)',schemetxt)
    Lsrows = re.findall(r'\d[\s\d\-]*\d',Lstxt[0].replace('\n',''))
    Ls = np.array([[[int(num) for num in Lsrows[i].split()] for i in range(4*j,4*(j+1))] for j in range(4)])
    
    
    scheme = {'P':P,'Q':Q,'L':L,'L*':Ls}

    return scheme
