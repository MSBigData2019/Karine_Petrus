#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 10:01:13 2018

@author: karine
"""


import unittest
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
html_doc="https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options="
html_="https://www.lacentrale.fr"
def query_page(html_doc):
    res = requests.get(html_doc)
    if res.status_code == 200:
        html_doc1 =  res.text
        soup = BeautifulSoup(html_doc1,"html.parser")
    return soup

field=["fieldYear","fieldPrice","fieldMileage"]

def createDataFrame(soup):
    a=soup.find('div',class_='resultListContainer')
    price=a.find_all("div",class_="fieldPrice")
    ListePrice=[]
    ListePrice=list(a.find_all("div",class_="fieldPrice"))
    Price=pd.DataFrame(list(map(lambda x: re.sub("\s+","",x.text), ListePrice)))
    ListeKmage=[]
    ListeKmage=list(a.find_all("div",class_="fieldMileage"))
    Kmage=pd.DataFrame(list(map(lambda x: re.sub("\s+","",x.text), ListeKmage)))
    ListeYear=[]
    ListeYear=list(a.find_all("div",class_="fieldYear"))
    Year=pd.DataFrame(list(map(lambda x: re.sub("\s+","",x.text), ListeYear)))
    d = {'Year': Year, 'Kmage': Kmage, 'Price': Price}
    all_links = list(map(lambda x :html_+x.attrs['href'] , soup.find_all("a", class_= "linkAd ann")))
    #print (Price)
    #r = np.array([Year, Kmage, Price])
   # d=pd.concat([Year, Kmage, Price], columns=['Year','Kmage','Price'])
    #d = pd.DataFrame(ar, columns = ['Year', 'Kmage', 'Price'])
    return d, all_links, Price, Kmage, Year
def main():
    html_doc="https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options="
    links2=[]
    Year_2=[]
    Price_2=[]
    dfinal=pd.DataFrame({'Year': [], 'Kmage': [], 'Price': []})
    soup=query_page(html_doc)
    d, all_links, Price, Kmage, Year=createDataFrame(soup)
    dfinal=d
   #html_2="https://www.lacentrale.fr/listing?makesModelsCommercialNames=RENAULT%3AZOE&options="
    #soup=query_page(html_2)
    #d, all_links, Price, Kmage, Year=createDataFrame(soup)
    links2.extend(all_links)
    Year_2.append(Year)
    Price_2.append(Price)
 #       dfinal=pd.concat([dfinal,d], columns=['Year','Kmage','Price'])
    print(dfinal)
    #print(df2)
if __name__ == '__main__':
    main() 
#rest = requests.get(path,auth=(user, token))
#phoneNumber1