#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import requests
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
import seaborn as sns
#Identifier les marques de PC proposant le plus de rabais¶

def query(brand_computer):
    main_url = "https://www.darty.com/nav/extra/list?s=topa&cat=756&prix_barre=dcom_BonPlan&m="
    reduc={}
    for brand in brand_computer:
        url = main_url + brand
        res= requests.get(url) 
        html_doc =  res.text
        doc = BeautifulSoup(html_doc, "html.parser")
        print (url)    
        reduc[brand] = list(map(lambda x : x.text, doc.find_all("span",class_="striped_price")))
    return reduc

def plot_result(reduc):
    plt.figure(figsize=(18,5))
    plt.subplot(121)
    plt.title("Nombre de rabais pour les ordinateurs portables DELL")
    plt.hist(reduc['DELL'],color='r')
    plt.subplot(122)
    plt.title("Nombre de rabais pour les ordinateurs portables ACER")
    plt.hist(reduc['ACER'], color='b')

def main():
    brand_computer = ["DELL","ACER"]
    reduc = query(brand_computer)
    plot_result(reduc)

if __name__ == '__main__':
    main()
