#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 13:05:57 2018

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
import requests
import json
import re
import pandas as pd
import slugify
#output = unicodedata.normalize('NFD', my_unicode).encode('ascii', 'ignore')

html_doc="https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"

def query(html_doc):
    res = requests.get(html_doc) 
    html_doc_test =  res.text
    doc = BeautifulSoup(html_doc_test, "html.parser")
    doc1 = doc.find('tr').findNext('td')    
    city = []
    region =[]
    for i in range(0,10):
        doc1 = doc1.findNext('tr')
        textcity = doc1.findNext('td').findNext('td').text.strip()
        textregion = doc1.findNext('td').findNext('td').findNext('td').text.strip()
        doc1 = doc1.findNext('td').findNext('td')
        city.append(re.sub('[^a-zA-Z-áéíóú]+', '', textcity))
        region.append(re.sub('[^a-zA-Z-áéíóú]+', '', textregion))
    return city, region

 
def distance(city):
    dist={}
    Ville=pd.DataFrame(index = city, columns = city)
    for i in range(len(city)):
        for j in range(i+1,len(city)):
            html_dist = "https://www.bonnesroutes.com/distance/?from="+str(city[i])+"&to="+str(city[j])    
            res = requests.get(html_dist)
            html_doc_test =  res.text
            doc = BeautifulSoup(html_doc_test, "html.parser")
            d = doc.find("div",id="total_distance").findNext("div")
            dist[city[i],city[j]] = d.text
            Ville.iloc[i,j] =  d.text
            Ville.iloc[j,i] =  d.text
            Ville.iloc[i,i] = 0
     
    return dist, Ville
def main():
    city, region = query(html_doc)
    print ("Les 10 villes les plus peuplés sont : ")
    print (city)
    print ("La matrice des distances entre les villes est : ")
    dist, Ville = distance(city)
    print(Ville)

if __name__ == '__main__':
    main()