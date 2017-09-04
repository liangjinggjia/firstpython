import requests,re,pymysql
from bs4 import BeautifulSoup

def get_year_date(code,year,conn):
    url='http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&' \
        'code={0}&topline=10&year={1}&month=&rt=0.3555676164531325'.format(code,year)
    print(url)
    r=requests.get(url,timeout=30)
    print(r.encoding)
    soup=BeautifulSoup(r.content,'lxml')
    num=len(soup.select('.box'))
    for i in range(0,num):
        s=soup.select('.box')[i]
        a=s.select('.t .left')[0]
        before_ji_du=re.findall(r'\d季度',s.text)[0]
        ji_du=re.sub('季度','',before_ji_du)
        time=str(year)+'-'+ji_du
        b=s.select('tbody tr')
        x=[]
        y=[]
        for c in b:
            d=c.select('td')
            print(d[0].text,d[1].text,d[2].text)
            d_c=[d[0].text,d[1].text,d[2].text]
            x.append(d_c)
        for e in b:
            f=e.select('td[class=tor]')
            f_c=[f[-3].text,f[-2].text,f[-1].text]
            print(f[-3].text,f[-2].text,f[-1].text)
            y.append(f_c)

        sql="INSERT INTO `fund`.`'{0}'` (`pai_ming`, `dai_ma`, `name`, `bi_li`, `gu_shu_wan_gu`, `shi_zhi_wan_yuan`, `time`) VALUES (%s ,%s, %s, %s, %s, %s, %s);\n".format(code)


        for i in range(0,len(x)):
            cur=conn.cursor()
            cur.execute(sql,(int(x[i][0]),x[i][1],x[i][2],y[i][-3],y[i][-2],y[i][-1],time))
            conn.commit()

if __name__ == '__main__':
    code='{:06}'.format(519606)
    year=2017
    conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
    # 判断是否存在该表
    sql='''select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='fund' and TABLE_NAME="%s";'''
    cur=conn.cursor()
    cur.execute(sql,code)
    if_exists=cur.fetchall()
    print(len(if_exists))
    #该表不存在
    if len(if_exists)==0:
        cur=conn.cursor()
        sql_1="create table if not exists `fund`.`'{0}'` (`id` INT NOT NULL AUTO_INCREMENT,`pai_ming` INT NULL,`dai_ma` VARCHAR(45) NOT NULL,`name` VARCHAR(45) NOT NULL,`bi_li` VARCHAR(45) NOT NULL,`gu_shu_wan_gu`  VARCHAR(45) NOT NULL,`shi_zhi_wan_yuan`  VARCHAR(45) NOT NULL,`time` VARCHAR(45) NOT NULL,PRIMARY KEY (`id`));".format(code)
        print(sql_1)
        cur.execute(sql_1)
        conn.commit()
    get_year_date(code,year,conn)

