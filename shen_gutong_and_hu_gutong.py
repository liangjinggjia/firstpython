import requests,pymysql,datetime
from bs4 import BeautifulSoup
import tushare as ts

def get_data_fron_dongdang_caifu(date_list,sh_or_sz):
    shang_conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
    if sh_or_sz==1:
        biao=2
    else:
        biao=3
    for a in date_list:
        date=a[0].strftime('%Y-%m-%d')
        url='http://data.eastmoney.com/hsgt/top10/{0}.html'.format(date)
        print(url)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "http://data.eastmoney.com/hsgt/top10.html"
        }
        r=requests.get(url,headers=headers)
        soup=BeautifulSoup(r.content,'lxml')
        shang_gutong_table=soup.select('.contentBox')[biao].select('tbody tr')
        for gu_piao in shang_gutong_table:
            d=gu_piao.select('td')
            if d[0].text!='暂无数据':
                shen=[]
                for i in range(0,10):
                    if i in (5,6,7,8,9):
                        if i==5:
                            e=d[i].text[0:-1]
                            shen.append(e)
                        else:
                            if '亿' in d[i].text:
                                e=int(float(d[i].text[0:-1])*(10**8))
                                shen.append(e)
                            if '万' in d[i].text:
                                e=int(float(d[i].text[0:-1])*(10**4))
                                shen.append(e)
                            if d[i].text=='0':
                                shen.append('0')
                            if d[i].text=='-':
                                shen.append('0')
                            if '亿' not in d[i].text and '万' not in d[i].text and d[i].text!='0' and d[i].text!='-':
                                shen.append(d[i].text)
                    else:
                         shen.append(d[i].text)
                print(shen)
                insert_shang_gutong(date,shen,shang_conn)
    shang_conn.close()  # 释放资源

def insert_shang_gutong(date,shen,conn):
    sql='INSERT INTO `shang_zheng_gushi`.`shang_gutong` (`date`, `pai_ming`, `dai_ma`, `name`, `shou_pan_jia`, `zhang_die_fu_percent`,  `jing_er`, `mai_ru_er`, `mai_chu_er`,  `chengjiao_er`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    print(sql)
    cur=conn.cursor()
    cur.execute(sql,(date,shen[0],shen[1],shen[2],shen[4],shen[5],shen[6],shen[7],shen[8],shen[9]))
    conn.commit()#提交事务
    cur.close()  # 释放游标

def select_trade_date(start):
    shang_conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
    cur=shang_conn.cursor()
    sql="SELECT date FROM shang_zheng_gushi.`'sh'` where date >=%s;"
    # date_list=cur.execute(sql)错误的pymysql
    cur.execute(sql,(start))
    date_list=cur.fetchall()
    cur.close()  # 释放游标
    shang_conn.close()  # 释放资源
    print(type(date_list))
    return date_list

def download_dapan(start,conn):
    for a in ('sh','sz'):
        sql='create table if not exists `shang_zheng_gushi`.`%s`(`id` INT NOT NULL AUTO_INCREMENT,`date` DATE NOT NULL,`open` FLOAT NOT NULL,`close` FLOAT NOT NULL,`high` FLOAT NOT NULL,`low` FLOAT NOT NULL,`volume` FLOAT NOT NULL,PRIMARY KEY (`id`));'
        cur=conn.cursor()
        cur.execute(sql,(a))
        conn.commit()#提交事务
        sql_1="INSERT INTO `shang_zheng_gushi`.`%s` (`date`, `open`, `close`, `high`, `low`, `volume`) VALUES (%s,%s,%s,%s,%s,%s);"
        hist_data=ts.get_k_data(a,start=start)
        for datas,row in hist_data.iterrows():
            cur=conn.cursor()
            cur.execute(sql_1,(a,row[0],row[1],row[2],row[3],row[4],row[5]))
            conn.commit()
        cur.close()
    conn.close()

def select_start_date_from_shang_zhenggushi(shang_conn):
    sql='SELECT max(date) FROM shang_zheng_gushi.shang_gutong;'
    cur=shang_conn.cursor()
    cur.execute(sql)
    start_date=cur.fetchall()[0][0]+datetime.timedelta(days=1)
    cur.close()
    return start_date

if __name__ == '__main__':

#下载沪股通或者深股通资金到对各自应的数据库中的表(不含对应的股票)
    shang_conn=pymysql.connect(host='localhost',user='root',password='java',db='shang_zheng_gushi',port=3306,charset='utf8')
    start=select_start_date_from_shang_zhenggushi(shang_conn).strftime('%Y-%m-%d')
#执行完后，要注释下面
    download_dapan(start,shang_conn)
    date_list=select_trade_date(start)
    print(date_list)
    # 参数1：沪股通        0：深股通
    # 选沪股通还要全选shang_替换为shang_，选深股通反之
    get_data_fron_dongdang_caifu(date_list,1)