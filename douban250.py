#encoding:utf-8

import requests,re,math,os
from bs4 import BeautifulSoup





def get_html(url):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://movie.douban.com/top250"
    }
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding='gbk'
        return BeautifulSoup(r.content,'lxml')
    except:
        return 'get_html出现问题'

def get_content(pageno):
    url= 'https://movie.douban.com/top250?start={0}&filter='.format((pageno-1)*25)
    print('第{0}页'.format(pageno),url)
    soup=get_html(url)
    movies=soup.find('ol',class_='grid_view').find_all('li')
    for m in movies:

        # try:
            bd=m.select('.info .bd p')
            img_url=m.find('img')['src']
            name=m.select('.info .hd a .title')[0].text
            try:
                year=re.findall(r'\d{4}',str(bd))[0]
            except:
                year='none'
                #两次则这选出导演
            s=re.findall(r'导演:(.*)',str(bd))
            director=re.findall(r'(.*)\s{3}',str(re.findall(r'导演:(.*)',str(bd))[0]))[0]
            #两次正则选出类型
            beforeintroduce=re.findall(r'/\s(.*)\s*</p>',str(bd))[0]
            # $表示匹配最后一项符合要求的
            introduce=re.findall(r'[^/]+$',str(beforeintroduce))[0]
            print("片名：{}\t{}\n{}\n{} \n \n ".format(name,year,director,introduce) )

            # if(os.path.exists(r'douban250img/{}.png'.format(name))!=True):
            #     with open('douban250img/'+name+'.png','wb+') as f:
            #         f.write(requests.get(img_url).content)
        # except:
        #     print('在{0}页出问题'.format(pageno))


def get_pageno(soup):
    pagelen=len(soup.select('.item > .info'))
    allno=250
    pageno=math.ceil(allno/pagelen)
    print(pagelen,pageno)
    return pageno

# __name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。
# 这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
if __name__=='__main__':
    url='https://movie.douban.com/top250'
    soup=get_html(url)
    # print(type(soup))
    pageno=get_pageno(soup)
    for i in range(1,pageno+1):
        get_content(i)



