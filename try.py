# url='http://quotes.toscrape.com/page/1/'
# # response.url.split("/")会返回一个列表
# # [-2]会对返回的列表进行索引，选取倒数第二项
# print(url.split("/")[-2])

# import datetime
# delta = datetime.timedelta(days=3)
# if datetime.date(2017,7,20)>datetime.date(2017,7,19):
#     print(datetime.date(2017,7,18)-datetime.timedelta(days=9))

# import pymysql
# import tushare as ts
# daima='sz'
# conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
# sql='DROP TABLE IF EXISTS `%s`;CREATE TABLE `gushi`.`%s` (`id` INT NOT NULL AUTO_INCREMENT,`date` DATE NOT NULL,`open` FLOAT NOT NULL,`close` FLOAT NOT NULL,`high` FLOAT NOT NULL,`low` FLOAT NOT NULL,`volume` FLOAT NOT NULL,PRIMARY KEY (`id`));'
# sql_1='INSERT INTO `gushi`.`%s` (`date`, `open`, `close`, `high`, `low`, `volume`) VALUES (%s,%s,%s,%s,%s,%s);'
# hist_data=ts.get_k_data(daima,start='2015-1-1')
# cur=conn.cursor()
# cur.execute(sql,(daima,daima))
# conn.commit()#提交事务
# for datas,row in hist_data.iterrows():
#     # print(row)
#     cur=conn.cursor()
#     cur.execute(sql_1,(daima,row[0],row[1],row[2],row[3],row[4],row[5]))
#     conn.commit()


import tushare as ts

hist_data=ts.get_k_data('000001',start='2015-10-10')
print(hist_data)

