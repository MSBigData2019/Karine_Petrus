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


html_doc="https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es"

def query(html_doc):
    res= requests.get(html_doc) 
    html_doc_test =  res.text
    doc= BeautifulSoup(html_doc_test, "html.parser")
    doc1=doc.find('tr').findNext('td')    
    city=[]
    for i in range(0,100):
        textcity=doc1.split()
        city.append(textcity[1])
        doc1=doc1.find("tr").findNext('tr')
    pd.DataFrame(city)
    print(city)
    print()
def main():
    query(html_doc)

if __name__ == '__main__':
    main()