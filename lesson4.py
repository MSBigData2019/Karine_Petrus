#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:39:23 2018

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

#Attention il faut utiliser API ...

#Utilisation REGEX 

#Utilisation Pandas
# Where pour remplacer une valeur par une autre
#API_KEY = open("api_key.txt", "r").read()

#url_template = "https://www.open-medicaments.fr/api/v1/interactions?ids=paracetamol"
#for i in range(67445776:67445779):

#Format long to wide.. meld/ pivot
#pivot crée un index
#Groupby
#aggregatiop, transform
#apply
html_doc="https://medicaments.api.gouv.fr/api/medicaments?nom=paracetamol"#+str(i)
#hapi="https://www.open-medicaments.fr/api/v1/interactions?ids=paracetamol"
def query_page():
    res = requests.get(html_doc)
    if res.status_code == 200:
        html_doc1 =  res.text
        repository = json.loads(rest.content)
    return soup


#url=
req=request.get(html_doc).jsonre
soup.find("div",class_="container-header-medicament")
