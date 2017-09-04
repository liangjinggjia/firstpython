# coding:utf-8

import requests,re,pymysql,os

def get_data(cur,conn):
    url='http://hqdata.jrj.com.cn/sgt/top10_sz_1year.js'
    html=requests.get(url).text
    # print(html)
    data=re.findall(r'"Data":[\s\S]*};',html)
    # print(data)
    s=re.sub(r'"Data":\[\r\n','',data[0])
    t=re.sub('\]\};','',s)
    # print(t)
    # 通过在 *、+ 或 ? 限定符之后放置 ?，该表达式从"贪心"表达式F转换为"非贪心"表达式或者最小匹配
    # 获取的数据转由二维数组的字符形式转为一维数组的字符串形式，result这个List中
    result=re.findall(r'\[[\s\S]*?\]',t)
    # print(result)
    for r in result:
        a=re.sub('\[','',r)
        b=re.sub('\]','',a)
        c=re.sub('\"','',b)
        d=c.split(',')
        insert_data(cur,d,conn)
        # print(d)
    # for i in range(0,10):
    #     r=result[i]
    #     a=re.sub('\[','',r)
    #     b=re.sub('\]','',a)
    #     c=re.sub('\"','',b)
    #     d=c.split(',')
    #     insert_data(cur,d,conn)
    #     print(d)

def insert_data(cur,d,conn):
    sql='INSERT INTO `gushi`.`shen_money` (`date`, `dai_ma`, `name`, `shou_pan_jia`, `zhang_die_fu`, `mai_ru_er`, `mai_ru_bi`, `mai_chu_er`, `mai_chu_bi`, `chengjiao_er`, `chengjiao_bi`, `pai_ming`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
    cur.execute(sql,(d[0],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],d[11],d[1]))
    conn.commit()#提交事务



if __name__ == '__main__':
    try:
        conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
        cur=conn.cursor()
        sql='DROP TABLE IF EXISTS `gushi`.`shen_money`;\nCREATE TABLE `shen_money` (\n    `id` INT(11) NOT NULL AUTO_INCREMENT,\n    `date` DATE DEFAULT NULL,\n    `dai_ma` VARCHAR(10) DEFAULT NULL,\n    `name` VARCHAR(45) DEFAULT NULL,\n    `shou_pan_jia` FLOAT DEFAULT NULL,\n    `zhang_die_fu` FLOAT DEFAULT NULL,\n    `mai_ru_er` FLOAT DEFAULT NULL,\n    `mai_ru_bi` FLOAT DEFAULT NULL,\n    `mai_chu_er` FLOAT DEFAULT NULL,\n    `mai_chu_bi` FLOAT DEFAULT NULL,\n    `chengjiao_er` FLOAT DEFAULT NULL,\n    `chengjiao_bi` FLOAT DEFAULT NULL,\n    `pai_ming` INT(11) DEFAULT NULL,\n    PRIMARY KEY (`id`)\n)  ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=UTF8;\n'
        cur.execute(sql)
        conn.commit()
        get_data(cur,conn)
        cur.close()  # 释放游标
        conn.close()  # 释放资源
    except Exception as e:
        print(e)









