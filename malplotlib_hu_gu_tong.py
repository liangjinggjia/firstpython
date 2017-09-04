from matplotlib.pylab import date2num
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import tushare as ts
import datetime,pymysql
from matplotlib.dates import DateFormatter

def get_gu_piao_tu(gu_piao,start,money_list,cur,conn):
    hist_data=ts.get_k_data(gu_piao,start=start)
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

def get_one(gu_piao,start):
    sql='SELECT mai_chu_er,mai_ru_er,date,shou_pan_jia FROM shang_zheng_gushi.shang_gutong where dai_ma=%s and date>=%s;'
    cur.execute(sql,(gu_piao,start))
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
    start='2015-01-01'
    gu_piao='600276'
    try:
        conn=pymysql.connect(host='localhost',user='root',password='java',db='shang_zheng_gushi',port=3306,charset='utf8')
        cur=conn.cursor()
        money_list=get_one(gu_piao,start)
        get_gu_piao_tu(gu_piao,start,money_list,cur,conn)
        cur.close()  # 释放游标
        conn.close()  # 释放资源
    except Exception as e:
        print(e)
# 601318	中国平安
# 600519	贵州茅台
# 600036	招商银行
# 600104	上汽集团
# 600276	恒瑞医药
# 600585	海螺水泥
# 601166	兴业银行
# 600887	伊利股份
# 601668	中国建筑
# 601901	方正证券
# 600690	青岛海尔
# 600030	中信证券
# 600009	上海机场
# 601939	建设银行
# 600016	民生银行
# 600900	长江电力
# 601398	工商银行
# 600019	宝钢股份
# 600000	浦发银行
# 600066	宇通客车
# 601336	新华保险
# 601988	中国银行
# 600048	保利地产
# 601288	农业银行
# 600309	万华化学
# 601888	中国国旅
# 601601	中国太保
# 600028	中国石化
# 603589	口子窖
# 601006	大秦铁路
# 600004	白云机场
# 600660	福耀玻璃
# 600741	华域汽车
# 601688	华泰证券
# 600196	复星医药
# 601989	中国重工
# 600031	三一重工
# 601628	中国人寿
# 601328	交通银行
# 600406	国电南瑞
# 601800	中国交建
# 600837	海通证券