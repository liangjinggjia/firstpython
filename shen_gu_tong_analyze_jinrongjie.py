# coding:utf-8
import pymysql,datetime
import tushare as ts


def select_shengutong_daima(conn):
    sql='select  distinct dai_ma,name from gushi.shen_money order by dai_ma desc;'
    cur=conn.cursor()
    cur.execute(sql)
    gupiao_list=cur.fetchall()
    return gupiao_list

def download_gupiao(gupiao_list,conn):
    sql='DROP TABLE IF EXISTS `%s`;CREATE TABLE `gushi`.`%s` (`id` INT NOT NULL AUTO_INCREMENT,`date` DATE NOT NULL,`open` FLOAT NOT NULL,`close` FLOAT NOT NULL,`high` FLOAT NOT NULL,`low` FLOAT NOT NULL,`volume` FLOAT NOT NULL,PRIMARY KEY (`id`));'
    sql_1='INSERT INTO `gushi`.`%s` (`date`, `open`, `close`, `high`, `low`, `volume`) VALUES (%s,%s,%s,%s,%s,%s);'
    cur=conn.cursor()

    for gupiao in gupiao_list:
            hist_data=ts.get_k_data(gupiao[0],start='2015-01-01')
            cur.execute(sql,(gupiao[0],gupiao[0]))
            conn.commit()#提交事务
            for datas,row in hist_data.iterrows():
                # print(row)
                cur.execute(sql_1,(gupiao[0],row[0],row[1],row[2],row[3],row[4],row[5]))
                conn.commit()
    cur.close()  # 释放游标

def download_gupiao_houxu(gupiao_list,start_day,conn):
    cur=conn.cursor()
    for gupiao in gupiao_list:

        # 判断是否存在该表
        sql='''select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='gushi' and TABLE_NAME="%s";'''

        cur.execute(sql,gupiao[0])
        if_exists=cur.fetchall()
        # 该表存在
        if len(if_exists)>0:
            sql_1='INSERT INTO `gushi`.`%s` (`date`, `open`, `close`, `high`, `low`, `volume`) VALUES (%s,%s,%s,%s,%s,%s);'
            hist_data=ts.get_k_data(gupiao[0],start=start_day)
            for datas,row in hist_data.iterrows():
                # print(row)
                cur=conn.cursor()
                cur.execute(sql_1,(gupiao[0],row[0],row[1],row[2],row[3],row[4],row[5]))
                conn.commit()
        # 该表不存在
        else:
            # 不存在该表就新建
            sql_2='create table if not exists `gushi`.`%s`(`id` INT NOT NULL AUTO_INCREMENT,`date` DATE NOT NULL,`open` FLOAT NOT NULL,`close` FLOAT NOT NULL,`high` FLOAT NOT NULL,`low` FLOAT NOT NULL,`volume` FLOAT NOT NULL,PRIMARY KEY (`id`));'
            ur=conn.cursor()
            cur.execute(sql_2,(gupiao[0]))
            conn.commit()#提交事务
            sql_3='INSERT INTO `gushi`.`%s` (`date`, `open`, `close`, `high`, `low`, `volume`) VALUES (%s,%s,%s,%s,%s,%s);'
            hist_data=ts.get_k_data(gupiao[0],start='2015-01-01')
            for datas,row in hist_data.iterrows():
                print('不应该出现，说明该股票新出现在深股通中')
                print(row)
                cur=conn.cursor()
                cur.execute(sql_3,(gupiao[0],row[0],row[1],row[2],row[3],row[4],row[5]))
                conn.commit()
    cur.close()  # 释放游标
def select_jiaoyi_day(conn):
    sql="SELECT date FROM gushi.`'sh'`;"
    cur=conn.cursor()
    cur.execute(sql)
    jiaoyi_day=cur.fetchall()
    cur.close()  # 释放游标
    return jiaoyi_day


def select_gupiao_money(gupiao_daima,quchu_day,conn):
    sql='SELECT date,mai_ru_er,mai_chu_er,mai_ru_bi,mai_chu_bi,zhang_die_fu,name FROM gushi.shen_money where dai_ma=%s;'
    cur=conn.cursor()
    cur.execute(sql,gupiao_daima[0])
    gupiao_money=cur.fetchall()
    gupiao_money=list(gupiao_money)
    # 倒序删除
    for i in range(len(gupiao_money)-1,-1,-1):
        if gupiao_money[i][0]>quchu_day:
            del gupiao_money[i]
    cur.close()  # 释放游标
    return gupiao_money

def zhiding_day(gupiao_daima,gupiao_money,tian_shu,print_or_not,conn):
    #在MySQL查询时日期（date类型）要用''引住，不然mysql报错，而股票代码不用（varchar类型）
    sql="SELECT id,close FROM gushi.`%s` where date=%s;"
    sql_1="SELECT close,date FROM gushi.`%s`where id=%s;"
    cur=conn.cursor()

    zhiding_day_list=[]
    for money in gupiao_money:
        try:
            cur.execute(sql,(gupiao_daima[0],money[0]))
            dang_tian=cur.fetchall()
            cur.execute(sql_1,(gupiao_daima[0],dang_tian[0][0]+tian_shu))
            one_tian=cur.fetchall()
            zhang_die_fu=(one_tian[0][0]-dang_tian[0][1])/dang_tian[0][1]
            if print_or_not==1:
                print('日期',money[0],'净量',money[1]-money[2],'当天涨跌(元)',money[5],'%s日涨跌'%tian_shu,'%.1f%%'%(zhang_die_fu*100),'总量',money[1]+money[2],'买入比',money[3],'卖出比',money[4])
            d=[money[0],money[1]-money[2],money[5],zhang_die_fu,money[1]+money[2],money[3],money[4]]
            zhiding_day_list.append(d)
        except Exception as e:
            print(e)
            print('%s股票在%s买入后没有%s天后的交易数据（停牌了）'%(gupiao_daima[0],money[0],tian_shu))
    # print(zhiding_day_list)
    cur.close()  # 释放游标
    return zhiding_day_list

def zhiding_day_del(day_list,a):
    money_in=0
    money_out=0
    in_yes=0
    out_yes=0
    for i in day_list:
        if i[1]>0:
            money_in+=1
            if i[3]>a:
                in_yes+=1

        else:
            money_out+=1
            if i[3]<-a:
                out_yes+=1

    if money_in==0:
        in_yes_rate=-1
    else:
        in_yes_rate=in_yes/money_in
    if money_out==0:
        out_yes_rate=-1
    else:
        out_yes_rate=out_yes/money_out
    # print('in次数',money_in,'out次数',money_out,'in_yes次数',in_yes,'out_yes次数',out_yes,'in_yes比',in_yes_rate,'out_yes比',out_yes_rate)
    zhiding_day_rate=[money_in,money_out,in_yes,out_yes,in_yes_rate,out_yes_rate]
    return  zhiding_day_rate

if __name__ == '__main__':
    conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
    gupiao_list=select_shengutong_daima(conn)
    gupiao_list=list(gupiao_list)
    gupiao_list.append(('sh','上证指数'))
    gupiao_list.append(('sz','深证指数'))
    # 下载深股通中全部股票数据,加上上证，深证
    # download_gupiao(gupiao_list,conn)
    # 要执行股票数据更新时，必须先看数据库数据到哪一天，然后在修改日期更新
    # download_gupiao_houxu(gupiao_list,'2017-07-27',conn)
    jiaoyi_day=select_jiaoyi_day(conn)
    print(jiaoyi_day[-2][0])
    for i in range(1,6):
        print(i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i,i)
        for gupiao_daima in gupiao_list:
            d=i+1
            quchu_day=jiaoyi_day[-d][0]
            gupiao_money=select_gupiao_money(gupiao_daima,quchu_day,conn)
            # list中每个数据包含
            # 1,0控制是否详细打印('日期',money[0],'净量',money[1]-money[2],'当天涨跌',money[5],'次日涨跌',zhang_die_fu,'总量',money[1]+money[2],'买入比',money[3],'卖出比',money[4])
            zhiding_day_list=zhiding_day(gupiao_daima,gupiao_money,i,1,conn)
            # ('in次数',money_in,'out次数',money_out,'in_yes次数',in_yes,'out_yes次数',out_yes,'in_yes比',in_yes_rate,'out_yes比',out_yes_rate)
            a=0.1 #涨跌幅多少才有效
            zhiding_day_rate=zhiding_day_del(zhiding_day_list,a)
            print()
            print('代码',gupiao_daima[0],'名字',gupiao_daima[1],'in次数',zhiding_day_rate[0],'out次数',zhiding_day_rate[1],'in_yes次数',zhiding_day_rate[2],'out_yes次数',zhiding_day_rate[3],'in_yes比',(zhiding_day_rate[4]),'out_yes比',zhiding_day_rate[5])
            # print('名字',gupiao_daima[1],'in_yes比',(zhiding_day_rate[4]),'out_yes比',zhiding_day_rate[5])
            print()
            print()
            print()
    conn.close()  # 释放资源
