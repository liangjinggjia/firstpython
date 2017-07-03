#encoding:utf-8

import requests,re,math,gridfs,time,os
from bs4 import BeautifulSoup
from pymongo import MongoClient




def get_html(url,num_tries=2):
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Referer": "https://movie.douban.com/top250"
    }
    try:
        r=requests.get(url,headers=headers,timeout=30)
        print(r.encoding)
        r.encoding='gbk'
        #失败请求(非200响应)抛出异常
        r.raise_for_status()
        if 500<=r.status_code<600:
            if num_tries>0:
                return get_html(url,num_tries-1)
        return BeautifulSoup(r.content,'lxml')
    except requests.RequestException as e:
        print('get_html出现问题',e)
def get_content(page_no):
    url= 'https://movie.douban.com/top250?start={0}&filter='.format((page_no-1)*25)
    print('第{0}页'.format(page_no),url)
    soup=get_html(url)
    movies=soup.find('ol',class_='grid_view').find_all('li')
    for m in movies:

        try:
            bd=m.select('.info .bd p')
            img_url=m.find('img')['src']
            name=m.select('.info .hd a .title')[0].text
            try:
                year=re.findall(r'\d{4}',str(bd))[0]
            except:
                year='none'
                #两次则这选出导演
            director=re.findall(r'(.*)\s{3}',str(re.findall(r'导演:(.*)',str(bd))[0]))[0]
            #两次正则选出类型
            beforeintroduce=re.findall(r'/\s(.*)\s*</p>',str(bd))[0]
            # $表示匹配最后一项符合要求的
            introduce=re.findall(r'[^/]+$',str(beforeintroduce))[0]
            # print("片名：{}\t{}\n{}\n{} \n \n ".format(name,year,director,introduce) )

            if db.douban250.find_one({'name':name})==None:
                _img_id=fs.put(requests.get(img_url).content)
                return db.douban250.save(dict(name=name,year=year,director=director,introduce=introduce,imgid=_img_id,time=time.time()))
            print(name+'已存在')

            if(not os.path.exists(r'douban250img/{}.png'.format(name))):
                with open('douban250img/'+name+'.png','wb+') as f:
                    f.write(requests.get(img_url).content)
        except:
            print('在{0}页出问题'.format(page_no))


def get_page_no(soup):
    print(soup)
    page_len=len(soup.select('.item > .info'))
    allno=250
    page_no=math.ceil(allno/page_len)
    print(page_len,page_no)
    return page_no

def save_img_to_disk(img_id,name):
    img=fs.find_one({'_id':img_id})
    tp_file = open('d:/img/' + name + '.jpg', "wb+")
    tp_file.write(img.read())
    tp_file.close()

def mongodb_delete(name):
    """
    根据name删除信息
    例如：mongodb_delete('桃花扇')
    :param name 电影名
    """
    record = db.douban250.find_one({"name": name})
    print(record)
    _id = record.get("_id")
    _imgid = record.get("imgid")
    print(_imgid)
    db.douban250.remove({"_id": _id})
    fs.delete(_imgid)

# __name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。
# 这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
if __name__=='__main__':
    client=MongoClient()
    db=client.douban250
    fs=gridfs.GridFS(db,'images')
    url='https://movie.douban.com/top250'
    soup=get_html(url)
    # print(type(soup))
    page_no=get_page_no(soup)
    if not os.path.exists(r'douban250img'):
        os.makedirs(r'douban250img')
    for i in range(1,page_no+1):
        get_content(i)


    # movies=db.douban250.find()
    # for m in movies:
    #     print(m['name'])
    #     save_img_to_disk(m['imgid'],m['name'])

    client.close()



