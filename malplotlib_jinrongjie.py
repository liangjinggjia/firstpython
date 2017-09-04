from matplotlib.pylab import date2num
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import tushare as ts
import datetime,pymysql
from matplotlib.dates import DateFormatter

def get_gu_piao_tu(gu_piao,money_list,cur,conn):
    hist_data=ts.get_k_data(gu_piao,start='2016-10-05')
    # 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
    k_data_list = []
    k_time_list = []
    k_money_list = []
    for dates,row in hist_data.iterrows():
        # 将时间转换为数字
        date_time = datetime.datetime.strptime(row[0],'%Y-%m-%d')
        t = date2num(date_time)
        open,close,high,low = row[1:5]
        datas = (t,open,high,low,close)
        k_data_list.append(datas)
        k_time_list.append(t)
        k_money_list.append(row[5])

    # 创建子图
    ax1=plt.subplot2grid((4,1),(0,0),rowspan=3)
    ax2=plt.subplot2grid((4,1),(3,0))
    # 设置X轴刻度为日期时间
    ax1.xaxis_date()
    #设置时间标签显示格式
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    # 显示网格
    ax1.grid()
    ax1.set_title("股票代码：%sK线图" %gu_piao)
    ax1.set_xlabel("时间")
    ax1.set_ylabel("股价（元）")
    mpf.candlestick_ohlc(ax1,k_data_list,width=0.5,colorup='r',colordown='green',alpha=1)

    money_in_time=[]
    money_in_height=[]
    money_in_s=[]
    money_out_time=[]
    money_out_height=[]
    money_out_s=[]
    for i in money_list:
        if i[2]>0:
            money_in_time.append(i[0])
            money_in_height.append(i[1])
            money_in_s.append(i[2])
        else:
            money_out_time.append(i[0])
            money_out_height.append(i[1])
            money_out_s.append(-i[2])

    ax3=ax1.twinx()
    ax3.set_ylabel("成交量（元）")
    ax3.bar(money_in_time,money_in_s,color='orange',alpha=.5,label='in')
    ax3.bar(money_out_time,money_out_s,color='k',alpha=.3,label='out')
    ax3.legend()

    ax2.xaxis_date()
    ax2.bar(k_time_list,k_money_list)
    ax4=ax2.twinx()
    ax4.set_ylabel("成交量（元）")
    ax4.bar(money_out_time,money_out_s,color='k',alpha=1)
    ax4.bar(money_in_time,money_in_s,color='orange',alpha=.5)

    #用来正常显示中文标签
    plt.rcParams['font.sans-serif']=['SimHei']
    #用来正常显示负号
    plt.rcParams['axes.unicode_minus']=False
    plt.show()

def get_one(gu_piao):
    sql='SELECT mai_chu_er,mai_ru_er,date,shou_pan_jia FROM gushi.shen_money where dai_ma=%s;'
    cur.execute(sql,(gu_piao))
    result=cur.fetchall()
    money_data_list=[]
    for i in result:
        t = date2num(i[2])
        jin_er_du=i[1]-i[0]
        shou_pan_jia=i[3]
        money_data_list.append((t,shou_pan_jia,jin_er_du))
    return money_data_list

if __name__ == '__main__':
    money_in_list=[]
    money_out_list=[]
    # 002415海康 000651格力 000333美的
    gu_piao='000651'
    try:
        conn=pymysql.connect(host='localhost',user='root',password='java',db='gushi',port=3306,charset='utf8')
        cur=conn.cursor()
        money_list=get_one(gu_piao)
        get_gu_piao_tu(gu_piao,money_list,cur,conn)
        cur.close()  # 释放游标
        conn.close()  # 释放资源
    except Exception as e:
        print(e)
# 139	000333	美的集团	2017-07-20
# 137	000858	五粮液	2017-07-20
# 136	000651	格力电器	2017-07-20
# 136	002415	海康威视	2017-07-20
# 76	002304	洋河股份	2017-07-12
# 54	000725	京东方Ａ	2017-07-18
# 50	000538	云南白药	2017-07-19
# 34	002008	大族激光	2017-07-13
# 33	000423	东阿阿胶	2017-07-19
# 32	002508	老板电器	2017-07-14
# 31	000001	平安银行	2017-07-20
# 29	001979	招商蛇口	2017-07-13
# 28	002236	大华股份	2017-07-20
# 27	002027	分众传媒	2017-07-07
# 22	002241	歌尔股份	2017-07-20
# 22	000568	泸州老窖	2017-07-12
# 15	000002	万科Ａ	2017-07-20
# 15	002230	科大讯飞	2017-07-20
# 14	300433	蓝思科技	2017-07-20