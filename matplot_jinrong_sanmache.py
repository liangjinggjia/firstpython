import tushare as ts
import matplotlib.pyplot as plt

yin_hang=ts.get_k_data('399905',index=True)
print(yin_hang)