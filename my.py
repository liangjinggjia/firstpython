# coding:utf-8

# 引入相关模块
import requests
from bs4 import BeautifulSoup

url = "http://www.mzsites.com/content/category/world-report/china-news"
html=requests.get(url).content.decode('utf8')
soup=BeautifulSoup(html,'lxml')
children=soup.select('h1 a[rel="bookmark"]')

for child in children:
    # print(title)
    result={'标题':child.text,'链接':child.get('href')}
    print(result)

