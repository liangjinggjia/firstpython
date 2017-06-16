url='http://quotes.toscrape.com/page/1/'
# response.url.split("/")会返回一个列表
# [-2]会对返回的列表进行索引，选取倒数第二项
print(url.split("/")[-2])
