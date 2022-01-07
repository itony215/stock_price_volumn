import pandas as pd
import numpy as np
import requests
import datetime
from io import StringIO
from bs4 import BeautifulSoup
from IPython.display import display, clear_output
from urllib.request import urlopen
import sched
import time
import os.path as path
import json
company_list = pd.read_csv('/home/pitaya/Documents/stock/history/全部上市公司.csv', encoding="utf_8_sig")
for idx, i in enumerate(company_list['公司代號']):
    print(str(idx+1)+"/"+str(len(company_list['公司代號'])))
    try:
        #print(i)
        r = requests.get("https://concords.moneydj.com/Z/ZC/ZCW/ZCWG/ZCWG_"+str(i)+"_30.djhtm")
        data = r.text.split("GetBcdData('", 1)[-1].split("')")[0]
        data = data.split(' ')
        lst = eval(data[0])
        lst2 = eval(data[1])
        df = pd.DataFrame(lst2,lst, columns = ['ma30'])
        r_new = requests.get("https://concords.moneydj.com/Z/ZC/ZCW/ZCWG/ZCWG_"+str(i)+"_1.djhtm")
        data_new = r_new.text.split("GetBcdData('", 1)[-1].split("')")[0]
        data_new = data_new.split(' ')
        lst_new = eval(data_new[0])
        lst2_new = eval(data_new[1])
        tonow = datetime.datetime.now()
        col_name = df.columns.tolist()
        col_name.insert(col_name.index('ma30')+1,str(tonow.month)+"/"+str(tonow.day))
        df.reindex(columns=col_name)
        if(type(lst_new) == tuple):
            for idx, val in enumerate(lst_new):
                #print(idx, val)
                df.loc[val,str(tonow.month)+"/"+str(tonow.day)]= f'{float(lst2_new[idx]):g}'
                #df.loc[val,"1/5"]= f'{float(lst2_new[idx]):g}'
        else:
            df.loc[lst_new,str(tonow.month)+"/"+str(tonow.day)]= f'{float(lst2_new):g}'
            #df.loc[lst_new,"1/5"]= f'{float(lst2_new):g}'
            
        if path.exists("./price_volumn/"+str(i)+".csv"):
            df2 = pd.read_csv("/home/pitaya/Documents/stock/price_volumn/"+str(i)+".csv", header=0, index_col = 0)
            df2_split = df2.iloc[:,1:]
            #df2_split = df2.columns.get_loc("1/6")
            #print(df2_split)
            df = pd.concat([df, df2_split], axis=1, sort=False)
        df.to_csv("/home/pitaya/Documents/stock/price_volumn/"+str(i)+".csv")
    except:
        print("error", i)
        df.to_csv("/home/pitaya/Documents/stock/price_volumn/"+str(i)+".csv")