# -*- coding: utf-8 -*-

import pandas as pd
import re
from tqdm import tqdm
from datetime import datetime
from sqlalchemy import create_engine

path = r"D:\复旦\大四上\数据库与企业管理\project\database-project\source-code\covid19\covid19article.xlsx"

# Preprocess
df = pd.read_excel(path)
records = []

for i in tqdm(range(df.shape[0])):
    string = df.iloc[i, 0]
    string = string.split("\n")[0]
    date = re.findall("\d+月\d+日", string)[0]
    reports_raw = re.findall("\w+\d+例", string)
    stops = ["新疆生产建设兵团", "境外输入", "本土病例", "新增疑似", "死亡", "含"]
    reports = []
    for item in reports_raw:
        check = 0
        for stop in stops:
            if stop not in item:
                check += 1
        if check == len(stops):
            reports.append(item.replace("其中", ""))
    date = re.findall("\d+", date)
    if i <= 352:
        date = datetime.strptime("2021" + date[0] + date[1], '%Y%m%d')
    else:
        date = datetime.strptime("2020" + date[0] + date[1], '%Y%m%d')
    for item in reports:
        number = re.findall("\d+", item)[0]
        place = item.split(number)[0]
        records.append([date, place, int(number)])
        
records_df = pd.DataFrame(records, columns = ["date", "place", "number"])
#records_df.to_csv(r"D:\Document\大学资料\大四上课件\数据库与企业数据管理\项目\database-project\source-code\covid19\covid19.csv", index = False)

# Save in MySQL
connection_string = "mysql+pymysql://%s:%s@%s:%s/%s"%('root', '123456', 'localhost', 3306, "safe")
engine = create_engine(connection_string, echo = False)
records_df.to_sql(con = engine, name = 'pathvisualization_pandemicinformation', if_exists='replace', index = True)
