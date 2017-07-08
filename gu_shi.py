import tushare as ts

d=ts.get_k_data('002405',start='2010-05-18')
d.to_excel('C:/Users/zhou/Desktop/gushi/000977.xlsx')