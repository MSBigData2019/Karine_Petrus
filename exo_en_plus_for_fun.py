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
rc('font', **{'family': 'sans-serif', 'sans-serif': ['Computer Modern Roman']})
params = {'axes.labelsize': 12,
          'font.size': 12,
          'legend.fontsize': 12,
          'text.usetex': True,
          'figure.figsize': (8, 6)}
plt.rcParams.update(params)
plt.close("all")

sns.set_context("poster")
sns.set_palette("colorblind")
sns.set_style("white")
sns.axes_style()
website_prefix = "http://www.logic-immo.com/"
suffix="/vente-immobilier-orsay-91400,gif-sur-yvette-91190,23229_2,12350_2/options/groupprptypesids=1,2,6,7,12,15"
url = website_prefix + suffix
res = requests.post(url)
if res.status_code == 200:
    html_doc =  res.text
    soup = BeautifulSoup(html_doc,"html.parser")
price=[]
area=[]
p1=soup.find_all("p",class_="offer-price")

a1=soup.find_all("h3",class_="offer-attributes")
for i in range(len(p1)):
    p3=re.findall("\d\d\d\s*\d\d\d",p1[i].text.strip())
    p3St=' '.join(p3)
    p3St=p3St.replace(" ","")
    #p3=int(p3St)
    price.append(p3St)
    a2=re.findall("\d\d\d*",a1[i].text.strip())
    a2St=' '.join(a2)
    area.append(a2St)
p2=soup.find("span",class_="offer-price")
for pages in range(2,8):
    suffix="/vente-immobilier-orsay-91400,gif-sur-yvette-91190,23229_2,12350_2/options/groupprptypesids=1,2,6,7,12,15/page="+str(pages)
    url = website_prefix + suffix
    res = requests.post(url)
    if res.status_code == 200:
        html_doc =  res.text
        soup = BeautifulSoup(html_doc,"html.parser")
        p1=soup.find_all("p",class_="offer-price")
        a1=soup.find_all("h3",class_="offer-attributes")
        for i in range(len(p1)):
            p3=re.findall("\d\d\d\s*\d\d\d",p1[i].text.strip())
            p3St=' '.join(p3)
            p3St=p3St.replace(" ","")
            #p3=int(p3St)
            price.append(p3St)
            a2=re.findall("\d\d\d*",a1[i].text.strip())
            a2St=' '.join(a2)
            area.append(a2St)
dipr={}
for i in range(len(price)):
    try:
        dipr[float(area[i])]=float(price[i])
    except ValueError:
        print ("error")
print (price, area)
plt.clf()
#print sorted(dipr.iteritems())
#diprsor=sorted(dipr.iteritems())
#od = collections.OrderedDict(sorted(dipr.items()))
diprs=sorted(dipr.items())

plt.plot(dipr.keys(),dipr.values(),'o')
plt.xticks(fontsize=12, rotation=90)
plt.yticks(fontsize=12, rotation=0)
area=pd.DataFrame(list(dipr.keys()))
price=pd.DataFrame(list(dipr.values()))
sm_linmod = sm.OLS(area, price).fit()
skl_linmod = linear_model.LinearRegression()
skl_linmod.fit(area, price)
X_to_predict = np.linspace(0, 150.0, num=200).reshape(200, 1)
X_to_predict = pd.DataFrame(X_to_predict, columns=['speed'])

plt.plot(X_to_predict, skl_linmod.predict(X_to_predict),
         linewidth=3, label="OLS-sklearn-no-intercept")
plt.xlabel("Superficie (m2)")
plt.ylabel("Prix (euros)")
#plt.plot([0, np.mean(area)], [np.mean(price), np.mean(area)], color='red',
#         linewidth=1.5, linestyle="--")
plt.legend(numpoints=1, loc=2)  # numpoints = 1 for nicer display

#plt.yticks(np.arange(0, 400000, step=100000))
#plt.xticks(np.arange(0, 100, step=50))

#
#for elements in range(len(price))
#def _handle_request_result_and_build_soup(request_result):
#  if request_result.status_code == 200:
#    html_doc =  request_result.text
#    soup = BeautifulSoup(html_doc,"html.parser")
#    return soup


#return soup
#def _convert_string_to_int(string):
#  if "K" in string:
#    string = string.strip()[:-1]
#    return float(string.replace(',','.'))*1000
#  else:
#    return int(string.strip())

#def get_all_links_for_query(query):
#
#  url = website_prefix + 
#  res = requests.post(url, data = {'q': query })
#  soup = _handle_request_result_and_build_soup(res)
#  specific_class = "c-article-flux__title"
#  all_links = map(lambda x : x.attrs['href'] , soup.find_all("a", class_= specific_class))
#
#  return all_links
#
#def get_share_count_for_page(page_url):
#  res = requests.get(page_url)
#  soup = _handle_request_result_and_build_soup(res)
#  specific_class = "c-sharebox__stats-number"
#  share_count_text = soup.find("span", class_= specific_class).text
#  return  _convert_string_to_int(share_count_text)
#
#def get_popularity_for_people(people):
#  query = people
#  url_people = get_all_links_for_query(query)
#  results_people = []
#  for url in url_people:
#      results_people.append(get_share_count_for_page(website_prefix + url))
#  return sum(results_people)


#class Lesson1Tests(unittest.TestCase):
#    def testShareCount(self):
#        self.assertEqual(get_share_count_for_page("http://www.purepeople.com/article/brigitte-macron-decroche-une-jolie-couv-a-l-etranger_a306389/1") , 86)
#
#    def testConvertStringInt(self):
#        self.assertEqual(_convert_string_to_int("\n                            86\n                    ") , 86)
#        self.assertEqual(_convert_string_to_int("5,84K") , 5840)
#        self.assertEqual(_convert_string_to_int("\n                            1,6K\n                   ") , 1600)
#macron = get_popularity_for_people('macron')
#melenchon = get_popularity_for_people('melenchon')
#
#def main():
#    #unittest.main()
#    macron = get_popularity_for_people('macron')
#    melenchon = get_popularity_for_people('melenchon')
#    print macron, melenchon
#if __name__ == '__main__':
#    main()
