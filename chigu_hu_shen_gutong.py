import requests,re,pymysql,datetime



def select_trade_date(start):
    shen_conn=pymysql.connect(host='localhost',user='root',password='java',db='shen_zheng_gushi',port=3306,charset='utf8')
    cur=shen_conn.cursor()
    sql="SELECT date FROM shen_zheng_gushi.`'sh'` where date >=%s;"
    # date_list=cur.execute(sql)错误的pymysql
    cur.execute(sql,(start))
    date_list=cur.fetchall()
    cur.close()  # 释放游标
    shen_conn.close()  # 释放资源
    print(type(date_list))
    return date_list

def download_chigu(date_list):
    chigu_conn=pymysql.connect(host='localhost',user='root',password='java',db='chigu',port=3306,charset='utf8')
    for date in date_list:
        url='http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTHDSTA' \
            '&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&' \
            'sr=3&p=1&ps=50&js=var%20CVpoDFaQ={}&' \
            'filter=(MARKET%20in%20(%27001%27,%27003%27))' \
            '(HDDATE=^{}^)&rt=50055021'.format('pages:(tp),data:(x)',date[0].strftime('%Y-%m-%d'))
        r=requests.get(url=url)
        # print(r.text)
        a_page=re.findall('pages:\d*',r.text)
        page=int(re.sub('pages:','',a_page[0]))
        print(page)
        for i in range(1,page+1):
            url_1='http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTHDSTA' \
                '&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDPRICE&' \
                'sr=3&p={}&ps=50&js=var%20CVpoDFaQ={}&' \
                'filter=(MARKET%20in%20(%27001%27,%27003%27))' \
                '(HDDATE=^{}^)&rt=50055021'.format(i,'pages:(tp),data:(x)',date[0].strftime('%Y-%m-%d'))
            print(url_1)
            d=requests.get(url_1)
            # print(d.text)
            a_data=re.findall(r'data:[\s\S]*}]',d.text)
            # print(a_data[0])
            b_data=re.sub('data:','',a_data[0])
            # print(b_data)
            data=eval(b_data)
            # print(data[0])
            for g in data:
                for k,v in g.items():
                    if v=='-':
                        # print(k,v)
                        g[k]=0
                t=(g['HDDATE'],g['SCODE'],g['SNAME'],int(g['SHAREHOLDSUM']),g['SHARESRATE'],g['CLOSEPRICE'],g['ZDF'],int(g['SHAREHOLDPRICE']),int(g['SHAREHOLDPRICEONE']),int(g['SHAREHOLDPRICEFIVE']),int(g['SHAREHOLDPRICETEN']))
                print(t)
                sql='INSERT INTO `chigu`.`shang_zheng` (`date`, `dai_ma`, `name`, `chi_gu_shu`, `chi_gu_bi_percent`, `shou_pan_jia`, `zhang_die_fu_percent`, `chi_gu_shizhi`, `one_change`, `five_change`, `ten_change`) ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
                sql_1='INSERT INTO `chigu`.`shen_zheng` (`date`, `dai_ma`, `name`, `chi_gu_shu`, `chi_gu_bi_percent`, `shou_pan_jia`, `zhang_die_fu_percent`, `chi_gu_shizhi`, `one_change`, `five_change`, `ten_change`) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
                cur=chigu_conn.cursor()
                if t[1][0]=='6':
                    cur.execute(sql,(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10]))
                else:
                    cur.execute(sql_1,(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9],t[10]))
                chigu_conn.commit()
                cur.close()
    chigu_conn.close()

def select_start_date_from_shen_gutong():
    shen_conn=pymysql.connect(host='localhost',user='root',password='java',db='shen_zheng_gushi',port=3306,charset='utf8')
    cur=shen_conn.cursor()
    sql='SELECT max(date) FROM chigu.shen_zheng;'
    cur.execute(sql)
    start_date=cur.fetchall()[0][0]+datetime.timedelta(days=1)
    cur.close()
    shen_conn.close()
    return start_date

# 先更新shen_gutong_and_hu_gutong的数据再运本程序(需用shen_gutong数据)
if __name__ == '__main__':
    start_date=select_start_date_from_shen_gutong().strftime('%Y-%m_%d')
    print(start_date)
    date_list=select_trade_date(start_date)
    download_chigu(date_list)


# date
# dai_ma
# name
# chi_gu_shu
# chi_gu_bi_percent
# shou_pan_jia
# zhang_die_fu_percent
# chi_gu_shizhi
# one_change
# five_change
# ten_change
