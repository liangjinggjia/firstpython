# coding=utf-8
from urllib.request import urlopen as dl

url = "http://www.mzsites.com/"
html=dl(url).read().decode('utf8')
print(html)