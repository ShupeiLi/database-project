#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random
import string
import time
from sqlalchemy import create_engine


# In[11]:


def id_generator(length): 
    return "".join(str(random.randint(0,9)) for i in range(length))

def date_generator():
    a1=(2015,1,1,0,0,0,0,0,0)         #设置开始日期时间元组（2015-01-01 00：00：00）
    a2=(2021,12,31,23,59,59,0,0,0)    #设置结束日期时间元组（2021-12-31 23：59：59）
    start=time.mktime(a1)    #生成开始时间戳
    end=time.mktime(a2)      #生成结束时间戳
    t=random.randint(start,end)    #在开始和结束时间戳中随机取出一个
    date_touple=time.localtime(t)  #将时间戳生成时间元组
    date=time.strftime("%Y-%m-%d",date_touple)  #将时间元组转成格式化字符串（2021-05-21）
    return date


# In[15]:


type = ["food","clothes","daily use","digital","office supplies","sports"]
username_list = [] # 等待合并
n = 500
order_info = {"ono":[id_generator(10) for i in range(n)],
              "otime":[date_generator() for i in range(n)],
              "ovalue":[round(random.random()*1000, 2) for i in range(n)],
              "username":["18307100100" for i in range(n)],
              "sellername":["seller1" for i in range(n)],
              "otype":[type[random.randint(0,5)] for i in range(n)],
              "onum":[random.randint(0,10) for i in range(n)]}
order_info = pd.DataFrame(order_info)
# Save in MySQL
#connection_string = "mysql+pymysql://%s:%s@%s:%s/%s"%('root', '123456', 'localhost', 3306, "safe")
#engine = create_engine(connection_string, echo = False)
#records_df.to_sql(con = engine, name = 'order_information', if_exists='replace', index = True)

order_info.to_csv("order_info.csv")


# In[ ]:




