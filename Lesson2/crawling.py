#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 20:03:22 2018

@author: karine
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:24:44 2018

@author: karine
"""

# coding: utf-8
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
import re


listcompany=["airbus","lvmh","danone","capgemini"]
website_prefix ="https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&sortBy=&dateRange=&search="
website_prefix_finance = "https://www.reuters.com/finance/stocks/financial-highlights/"

def get_shortname_for_query(company):
    url=website_prefix + company
    res = requests.get(url)
    if res.status_code == 200:
        html_doc =  res.text
        soup = BeautifulSoup(html_doc,"html.parser")
    company_shortname=soup.find("tr",class_="stripe").findNext("td").findNext("td").text
    return company_shortname


def get_all_data_for_query(company_shortname):
    suffix=company_shortname
    url=website_prefix_finance + suffix
    #url=website_prefix
    res = requests.get(url)
    if res.status_code == 200:
        html_doc =  res.text
        soup = BeautifulSoup(html_doc,"html.parser")
    return soup

def get_quarter_endingDecember(soup):        
        endingDecember=soup.find("tr",class_="stripe")
        estimates_=endingDecember.findNext("td").findNext("td")
        estimates=estimates_.text
        estimates_mean=estimates_.findNext("td").text
        estimates_high=estimates_.findNext("td").findNext("td").text
        estimates_low=estimates_.findNext("td").findNext("td").findNext("td").text
        return estimates, estimates_mean, estimates_high, estimates_low

def get_share_evolution_data(soup):
        shareprice=soup.find("div",class_="sectionQuoteDetail")
        sharechange=soup.find("div",class_="sectionQuote priceChange")
        priceshare=re.findall("\d\d*.\d\d",shareprice.text)
        sharechange=re.findall("\d*.\d\d",sharechange.text)
        return sharechange, priceshare

def get_share_owned(soup):   
        shareowned=soup.find("td",text="% Shares Owned:")
        shareownedt=shareowned.findNext("td").text
        return shareownedt

def dividend_data(soup): 
        dividend=soup.find("td",text="Dividend Yield")
        dividend_company=dividend.findNext("td").text
        dividend_industry=dividend.findNext("td").findNext("td").text
        dividend_sector=dividend.findNext("td").findNext("td").findNext("td").text
        return dividend_industry, dividend_sector, dividend_company


def main():
    for i, company in enumerate(listcompany):
        company_shortname=get_shortname_for_query(company)
        soup=get_all_data_for_query(company_shortname)
        estimates, estimates_mean, estimates_high, estimates_low=get_quarter_endingDecember(soup)
        sharechange, priceshare= get_share_evolution_data(soup)
        shareownedt=get_share_owned(soup)
        dividend_industry, dividend_sector, dividend_company=dividend_data(soup)
        name=company[0].upper()+company[1:]
        f=open("Perf_financieres_"+name+".txt","w")
        f.write("Performance financières de " + name+"\n"+"\n")
        f.write("Ventes (en milions) au quartier fin décembre 2018:"+"\n")
        f.write("Nombre (# of Estimates) : "+str(estimates)+"\n"+"Moyenne :" +str(estimates_mean)+ " avec pour intervalle : ["+str(estimates_high)+"  :  "+str(estimates_high)+"]"+"\n"+"\n" )
        f.write("Action"+"\n"+"Prix = "+str(priceshare[0])+ " Evolution (euros) : "+str(sharechange[0])+" Evolution (%) : " +str(sharechange[1])+"\n"+"\n")
        f.write("Shares Owned des investisseurs : "+str(shareownedt)+"\n"+"\n")
        f.write("Dividend yield"+"\n")
        f.write("Company: "+str(dividend_company)+", Secteur : "+ str(dividend_sector)+ ", Industrie : " +str(dividend_industry))
        f.close()
if __name__ == '__main__':  
    main()
  