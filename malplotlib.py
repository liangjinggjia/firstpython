#
# import  numpy as  np
# x = range(6)
# plt.plot(x, [xi**2 for xi in x])
# plt.show()

from matplotlib.pylab import date2num
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
import tushare as ts
import datetime


hist_data=ts.get_k_data('002405',start='2015-05-18')
# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
data_list = []
time_list = []
money_list = []
for dates,row in hist_data.iterrows():
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(row[0],'%Y-%m-%d')
    t = date2num(date_time)
    open,close,high,low = row[1:5]
    datas = (t,open,high,low,close)
    data_list.append(datas)
    time_list.append(t)
    money_list.append(row[5])

# 创建子图
fig, ax1 = plt.subplots()
# fig, ax1 = plt.subplots(facecolor=(0.5, 0.5, 0.5))
fig.subplots_adjust(bottom=0.2)
# 设置X轴刻度为日期时间
ax1.xaxis_date()
mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
# alldays = DayLocator()              # minor ticks on the days
# weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
# dayFormatter = DateFormatter('%d')      # e.g., 12
# ax.xaxis.set_major_locator(mondays)
# ax.xaxis.set_minor_locator(alldays)
# ax.xaxis.set_major_formatter(weekFormatter)
plt.xticks(rotation=45)
plt.yticks()
plt.title("股票代码：002405K线图")
plt.xlabel("时间")
plt.ylabel("股价（元）")
mpf.candlestick_ohlc(ax1,data_list,width=0.5,colorup='r',colordown='green',alpha=1)
ax2=ax1.twinx()
ax2.bar(time_list,money_list)
# 显示网格
plt.grid()
#用来正常显示中文标签
plt.rcParams['font.sans-serif']=['SimHei']
plt.show()