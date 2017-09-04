import requests,re

url='http://hqdata.jrj.com.cn/sgt/top10_sz_1year.js'
html=requests.get(url).text
# print(html)
data=re.findall(r'"Data":[\s\S]*};',html)
# print(data)
s=re.sub(r'"Data":','',data[0])
t=re.sub('\};','',s)
print(t[1])