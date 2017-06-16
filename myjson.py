# coding:utf-8

import requests
import json

url='https://www.toutiao.com/stream/widget/local_weather/city/'
datas=requests.get(url).text
# print(datas)
result=json.loads(datas)
city=result['data']
print(city['上海']['上海'])
for c in city:
    print(c)

