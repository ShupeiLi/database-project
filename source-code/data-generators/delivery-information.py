# -*- coding: utf-8 -*-

import mysql.connector
import random
import datetime
import time


def decrypt(dno):
    """
    dno -> ono
    """
    dno_str = str(dno)
    ono = ""
    decrypt_dict = {"1":"6", "2":"8", "3":"2", "4":"9", "5":"1",
                    "6":"0", "7":"3", "8":"7", "9":"4", "0":"5"}
    for i in range(len(dno_str)):
        ono = ono + decrypt_dict[dno_str[i]]
    return int(ono)


class DeliveryGenerator():
    """
    Generate delivery order information.
    
    Args:
        n: number of orders.
    """
    
    def __init__(self, n):
        self.n = n
        self.db = mysql.connector.connect(
                    host = 'localhost',
                    user = 'root',
                    password = 'ShupeiLi',
                    database = 'safe'
                    )
    
    def select_order(self):
        """
        Select orders that hasn't been submiited by sellers.
        """
        cursor = self.db.cursor()
        cursor.execute("""
                       SELECT ono, sellername_id
                       FROM dashboard_orderinformation
                       """)
        order_index = cursor.fetchall()
        cursor.execute("""
               SELECT dno
               FROM dashboard_deliveryinformation
               """)
        delivery_index = cursor.fetchall()
        
        delivery_order_map = []
        for i in range(len(delivery_index)):
            delivery_order_map.append(decrypt(delivery_index[i][0]))
        
        return order_index, delivery_index
                       
                       
                       
model = DeliveryGenerator(1)               
order_index, delivery_index = model.select_order()                       
                       
                       