# -*- coding: utf-8 -*-

import pandas as pd
import mysql.connector
import random
from datetime import datetime


class HealthGenerator:
    """
    Generate delivery staff's health status.
    """

    def __init__(self, n):
        self.n = n  # specific numbers of days needed to be generated
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='safe'
        )

    def insert_values(self):
        """
        Insert values into healthinformation.
        """
        val = self.generator()
        sql = """
              INSERT INTO 
              dashboard_healthinformation(pno_id, pcity, ptemp, pupdate) 
              VALUES (%s, %s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()

    def get_name(self):
        """
        Get all staff's names and last update dates from register_newuser.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT username
               FROM register_newuser
               WHERE
                   utype = 'delivery'
               """)
        records = cursor.fetchall()
        cursor.close()
        return records

    def check_exist(self, val):
        """
        Check the existence of the values.

        Args:
            val: Tuple-like.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM dashboard_healthinformation
               WHERE
                   pno_id = '{}' AND pupdate = '{}'
               """.format(val[0], val[3]))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return False
        else:
            return True

    def get_latest_update(self, pno_id):
        """
        Check the existence of the values.

        Args:
            val: Tuple-like.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT pupdate
               FROM dashboard_healthinformation
               WHERE
                   pno_id = '{}'
               """.format(pno_id))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return records
        else:
            return False

    def generator(self):
        """
        Generate staff health information.
        pcity 今日途经城市
        ptemp 配送人员体温
        pupdate 更新健康信息时间

        是否需要随机产生多条呢？
        """

        # !!! 记得改表格存储地址
        table = pd.read_csv("china_city_list.csv")
        loc = table["City_Admaster"].tolist()
        values = []
        names = self.get_name()
        num = self.n
        i = 0
        while i < len(names):
            name = names[i][0]
            location = [loc[random.randint(0, len(loc)-1)] for x in range(num)]
            temperature = [round(random.random()*8, 1)+35 for x in range(num)]
            latest_date = self.get_latest_update(name)
            date = [latest_date+datetime.timedelta(days=x+1) for x in range(num)]
            for j in range(num):
                one_value = [name, location[j], temperature[j], date[j]]
                one_value = tuple(one_value)
                values.append(one_value)
            i += 1
        return values


if __name__ == '__main__':
    health = HealthGenerator(14)
    health.insert_values()
