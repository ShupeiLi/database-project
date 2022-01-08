# -*- coding: utf-8 -*-

import mysql.connector
import random
import datetime
import time
from faker import Faker


def encrypt(ono):
    """
    ono -> dno
    """
    dno = ""
    encrypt_dict = {"1":"5", "2":"3", "3":"7", "4":"9", "5":"0", 
                    "6":"1", "7":"8", "8":"2", "9":"4", "0":"6"}
    for i in range(len(ono)):
        dno = dno + encrypt_dict[ono[i]]
    return dno


def decrypt(dno):
    """
    dno -> ono
    """
    ono = ""
    decrypt_dict = {"1":"6", "2":"8", "3":"2", "4":"9", "5":"1",
                    "6":"0", "7":"3", "8":"7", "9":"4", "0":"5"}
    for i in range(len(dno)):
        ono = ono + decrypt_dict[dno[i]]
    return ono


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
        Select orders that haven't been submiited by sellers.
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
        
        order_list = []
        for i in range(len(order_index)):
            ono = order_index[i][0]
            if ono in delivery_order_map:
                continue
            else:
                order_list.append(order_index[i])
        
        return order_list
    
    def select_company(self):
        """
        Select companys.
        """
        cursor = self.db.cursor()
        cursor.execute("""
                       SELECT username
                       FROM register_newuser
                       WHERE utype = 'company'
                       """)
        records = cursor.fetchall()
        cursor.close()
        return records
    
    def select_unchecked(self):
        """
        Select unchecked delivery orders and corresponding product orders.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM dashboard_deliveryinformation
               WHERE is_checked = False
               """)
        unchecked_records = cursor.fetchall()
        cursor.execute("""
               SELECT ono, otime
               FROM dashboard_orderinformation
               """)
        product_orders = cursor.fetchall()
        cursor.close()
        
        binding = []
        for i in range(len(unchecked_records)):
            index = decrypt(unchecked_records[i][0])
            for j in range(len(product_orders)):
                if index == product_orders[j][0]:
                    binding.append([unchecked_records[i], product_orders[j]])
        
        return binding
    
    def simulate_order_submit(self):
        """
        Simulation: Sellers submit delivery orders.
        """
        values = []
        dtrans_choices = ["plane", "train", "truck"]
        order_list = random.sample(self.select_order(), self.n)
        companys = self.select_company()
        
        if len(order_list) == 0:
            print("所有订单已提交")
        else:
            for i in range(self.n):
                order = order_list[i]
                dno = encrypt(order[0])
                sno = order[1]
                dtrans = random.choice(dtrans_choices)
                tno = random.choice(companys)[0]
                one_value = (dno, sno, tno, dtrans, False, order[0])
                values.append(one_value)
                
            sql = """
                  INSERT INTO 
                  dashboard_deliveryinformation(dno, sno_id, tno_id, dtrans, is_checked, order_information_id) 
                  VALUES (%s, %s, %s, %s, %s, %s)
                  """
                  
            cursor = self.db.cursor()
            cursor.executemany(sql, values)
            self.db.commit()
            cursor.close()
            
    def simulate_order_confirm(self):
        """
        Simulation: Companys confirm delivery orders.
        """
        fake = Faker()
        cursor = self.db.cursor()
        binding = self.select_unchecked()
        updates = []
        
        if len(binding) == 0:
            print("所有订单已确认")
        else:
            for i in range(len(binding)):
                dvalue = round(random.uniform(0, 99), 2)
                start = binding[i][1][1]
                dsetime_future = fake.date_between(start_date=start, end_date='+30d')
                dsetime_stamp = random.randint(int(round(datetime.datetime.fromtimestamp(time.mktime(start.timetuple())).timestamp())), int(round(datetime.datetime.fromtimestamp(time.mktime(dsetime_future.timetuple())).timestamp())))
                dsetime = datetime.datetime.fromtimestamp(dsetime_stamp)
                dsetime_str = dsetime.strftime('%Y-%m-%d')
                dretime_future = fake.date_between(start_date=dsetime, end_date='+60d')
                dretime_stamp = random.randint(int(round(datetime.datetime.fromtimestamp(time.mktime(dsetime.timetuple())).timestamp())), int(round(datetime.datetime.fromtimestamp(time.mktime(dretime_future.timetuple())).timestamp())))
                dretime_str = datetime.datetime.fromtimestamp(dretime_stamp).strftime('%Y-%m-%d')
                container = list(binding[i][0])
                cursor.execute("""
                           UPDATE dashboard_deliveryinformation
                           SET dvalue = {}, dsetime = '{}', dretime = '{}', is_checked = {}
                           WHERE dno = '{}';
                           """.format(dvalue, dsetime_str, dretime_str, True, container[0]))
                self.db.commit()
                container[1] = dvalue
                container[3] = dsetime_str
                container[4] = dretime_str
                container[5] = True
                updates.append(tuple(container))
    
            cursor.close()
    

if __name__ == '__main__':
    model = DeliveryGenerator(50)
    
    # 模拟商家提交订单
    #model.simulate_order_submit()
    
    # 模拟公司确认订单
    model.simulate_order_confirm()
