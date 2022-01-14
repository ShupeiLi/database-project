# -*- coding: utf-8 -*-

import pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine

df = pd.read_csv(r'.\worldcities.csv')
ref = pd.read_csv(r'.\china_city_list.csv', encoding="gbk", encoding_errors="ignore")
data = df.loc[df['country'] == 'China']

df_joined_lst = []
for i in tqdm(range(ref.shape[0])):
    city = ref.iloc[i, 2]
    province = ref.iloc[i, 4]
    for j in range(data.shape[0]):
        city_data = data.iloc[j, 0]
        province_data = data.iloc[j, 7]
        if city == city_data and province == province_data:
            df_joined_lst.append((ref.iloc[i, 1], ref.iloc[i, 3], data.iloc[j, 2], data.iloc[j, 3]))

df_joined = pd.DataFrame(df_joined_lst, columns = ["dloc", "dpro", "dlat", "dlng"]).drop_duplicates(subset=["dloc"])
            
# Save in MySQL
connection_string = "mysql+pymysql://%s:%s@%s:%s/%s"%('root', 'ShupeiLi', 'localhost', 3306, "safe") #!!! Change passowrd
engine = create_engine(connection_string, echo = False)
df_joined.to_sql(con = engine, name = 'dashboard_geographictransformation', if_exists='append', index = False)