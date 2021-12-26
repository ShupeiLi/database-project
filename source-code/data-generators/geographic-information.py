# -*- coding: utf-8 -*-

import mysql.connector
import random

#造出两组数据
pointArr1 = [{lng: 120.37330074071, lat: 31.498294737149}, {lng: 120.57330074071, lat: 31.498294737149},
            {lng: 120.87330074071, lat: 31.498294737149}, {lng: 121.37330074071, lat: 31.498294737149}]
pointArr2 = [{lng: 113.39505673967, lat: 22.94738905789}, {lng: 120.57330074071, lat: 31.498294737149},
            {lng: 112.830583950802, lat: 34.27474928498}, {lng: 116.46473277246, lat: 39.934649603730}]

datetime1 = ["2021-12-19 14:00:00 ", "2021-12-20 07:34:12", "2021-12-20 19:46:95", "2021-12-21 13:23:37"]
datetime2 = ["2021-11-15 19:30:00 ", "2021-11-18 20:34:54", "2021-11-21 09:43:26", "2021-11-24 13:24:49"]

#将输入的物流订单输入到变量deliverorder
deliverorder = dno

#物流订单号奇偶数
if deliverorder % 2 == 0:
    for i in range(4):
        dno = dno
        dloc = pointArr1[i]
        dupdate = datetime1[i]
else:
    for i in range(4):
        dno = dno
        dloc = pointArr2[i]
        dupdate = datetime1[i]


class GeographicGenerator():
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
                       SELECT dno
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
        Generate accounts.
        """
        values = []
        dno = self.get_dno()
        for i in len(dno):
            num = dno[i][0]
            rec = self.get_last_position(dno)
            if len(rec) > 0:
                last_date = rec[0][]
                last_pos = rec[0][]
                date = []

            else:
                date = [ for x in range(4)]
                pos = ["".format(round(random.random()*360, 6)+x, round(random.random()*360, 6)+x) for x in range(4)]




        return values


if __name__ == '__main__':
    print("")