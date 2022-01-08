# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import mysql.connector
import random

df = pd.read_csv(r'D:\复旦\大四上\数据库与企业管理\project\database-project\source-code\data-generators\worldcities.csv')
data = df.loc[df['country'] == 'China']


class GeographicGenerator:
    """
    Generate Geographic information.
    """

    def __init__(self,n):
        self.n = n
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='safe'
        )

    def insert_values(self):
        """
        Insert values into register_newuser.
        """
        val = self.generator()
        sql = """
              INSERT INTO 
              pathvisualization_geographicinformation(dno, dloc, dupdate) 
              VALUES (%s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()

    def get_dno(self):
        """
        Select companys.
        """
        cursor = self.db.cursor()
        cursor.execute("""
                       SELECT dno, cast(dsetime as datetime)
                       FROM dashboard_deliveryinformation
                       WHERE
                         is_checked=True
                       """)
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_last_position(self, val):
        """
                Select companys.
                """
        cursor = self.db.cursor()
        cursor.execute("""
                       SELECT *
                       FROM pathvisualization_geographicinformation
                       WHERE dno={} order by cast(dupdate as datetime) desc
                       """.format(val))
        records = cursor.fetchall()
        cursor.close()
        return records

    def generator(self):
        """
        Generate positions.
        """
        values = []
        dno_info = self.get_dno()
        # 默认之前是没有记录的
        for i in range(len(dno_info)):
            dnum = dno_info[i][0]
            start_time = dno_info[i][1]
            print(type(start_time))
            x = random.randint(0, len(data))
            y = random.randint(0,len(data))
            if x == y:
                y = y+1
            start_loc = [data.iloc[x]['lat'], data.iloc[x]['lng']] # list
            end_loc = [data.iloc[y]['lat'], data.iloc[y]['lng']] # list
            one_value = (dnum, ",".join([str(x) for x in start_loc]), start_time)
            values.append(one_value)
            for j in range(self.n):
                loc = [start_loc[0] + (end_loc[0]-start_loc[0]) / self.n * j + random.random() * 0.1 - 0.05, start_loc[1]+(end_loc[1]-start_loc[1]) / self.n * j + random.random() * 0.1 - 0.05]
                dloc = ",".join([str(x) for x in loc])
                start_time = start_time + datetime.timedelta(seconds=random.randint(0,59), minutes=random.randint(0,59), hours=random.randint(0,2))
                one_value = (dnum, dloc, start_time)
                values.append(one_value)
            start_time = start_time + datetime.timedelta(seconds=random.randint(0, 59), minutes=random.randint(0, 59),
                                                         hours=random.randint(0, 2))
            one_value = (dnum, ",".join([str(x) for x in end_loc]), start_time)
            values.append(one_value)
        return values


if __name__ == '__main__':
    pathGenerator = GeographicGenerator(10)
    pathGenerator.insert_values()