#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 21:05:59 2018

@author: karine
"""
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re
from matplotlib import rc
import matplotlib.pyplot as plt
import seaborn as sns
import collections
import sklearn 
from sklearn import linear_model
import statsmodels.api as sm
import requests
import json

from operator import itemgetter
from multiprocessing import Pool


html_doc="https://gist.github.com/paulmillr/2657075"


def get_contributor_list(html_doc):
    list_contrib=[]
    res= requests.get(html_doc) 
    html_doc =  res.text
    doc= BeautifulSoup(html_doc, "html.parser")
    table=doc.find('th')
    for i in range(1,5):
        contributor=table.findNext('tr').findNext('a').text.split()
        table=table.findNext('tr').findNext('a')
        list_contrib.append(contributor)
    df = pd.DataFrame({'Contributors':list_contrib})
    return df, list_contrib


def get_repository(list_contrib):
    token="e77f75ebc67dc1c0d161ed8a4d540bfa76de943c"
    token="7f976f25b1724cfef8e92f05c852264a298bea81"
    user="karinep"
    nbstar={}
    meanstar={}
    for name in list_contrib:
        path= 'https://api.github.com/users/' + name + '/repos'
        rest = requests.get(path,auth=(user, token))
        repository = json.loads(rest.content)
        star=0.
        for rep in repository:
            star=star+rep["stargazers_count"]  
        nbstar[name]=star
        meanstar[name]=star/(len(repository)+1)
    sorted(meanstar.values())
    sortednbstar=sorted(meanstar.items(), key=itemgetter(1))
    Sortednbstarmean=pd.DataFrame(sortednbstar,columns=["Contributors", "Mean_Star"])
    return Sortednbstarmean

def main():
    Pool(5)
    df, list_contrib=get_contributor_list(html_doc)
    print(df)
    Sortednbstarmean=get_repository(list_contrib)
    print (Sortednbstarmean)

if __name__ == '__main__':
    main()
