# coding:utf-8

import requests,re,math
from bs4 import BeautifulSoup
from multiprocessing import Pool

url='http://hz.fang.anjuke.com/loupan/all'
# http://hz.fang.anjuke.com/loupan/all/p2/

wbdata=requests.get(url).content
soup=BeautifulSoup(wbdata,'lxml')

#总页数
result=soup.select('.item-mod > .infos')
pagelen=len(result)
# print(pagelen)
allno=re.findall(r'共有<em>(.*)</em>个有关杭州新房楼盘',str(soup))[0]
# print(allno)
pageno=math.ceil(int(allno)/pagelen)
# print(pageno)

def getmessage(page):
    url='http://hz.fang.anjuke.com/loupan/all/p{0}/'.format(page)
    print('第{0}页'.format(page))
    wbdata=requests.get(url).content
    soup=BeautifulSoup(wbdata,'lxml')

    name=soup.select('.items-name')
    adress=soup.select('.address')
    price=soup.select('.favor-pos')

    # price=re.findall(r'均价<span>(.*)</span>元/m²',str(soup))

    for (n,a,p) in zip(name,adress,price):
        result={'name':n.get_text(),'adress':a.get_text(),'price':p.get_text()}
        print(result)

if __name__ == '__main__':
    pool = Pool(processes=2)
    # range(1,5)代表从1到5(不包含5)
    pool.map_async(getmessage,range(1,pageno+1))
    pool.close()
    pool.join()


