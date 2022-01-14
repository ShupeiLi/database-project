# -*- coding: utf-8 -*-

import mysql.connector
import random
import datetime


class OrderGenerator():
    """
    Generate order information.
    
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
        
    def select_user_type(self, utype):
        """
        Select users with the specified user type from MySQL.
        
        Args:
            utype: {0: 'buyer', 1: 'seller', 2: 'company', 3: 'platform', 4: 'delivery'}
        """
        cursor = self.db.cursor()
        utype_dict = {0: 'buyer', 1: 'seller', 2: 'company', 3: 'platform', 4: 'delivery'}
        selected_utype = utype_dict[utype]
        cursor.execute("""
                       SELECT username
                       FROM register_newuser
                       WHERE utype = '{}'
                       """.format(selected_utype))
        records = cursor.fetchall()
        cursor.close()
        return records
        
    def random_date_order(self):
        """
        Generate otime.
        """
        return random.randint(int(datetime.datetime(2020, 11, 3).timestamp()), int(datetime.datetime(2021, 12, 19).timestamp()))

    def check_valid(self, val):
        """
        Check the validity of the ono.
        
        Args:
            val: Tuple-like.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM dashboard_orderinformation
               WHERE ono = '{}'
               """.format(val[0]))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return False
        else:
            return True
        
    def generator_order(self):
        """
        Generate orders.
        """
        values = []
        i = 0
        buyers = self.select_user_type(0)
        sellers = self.select_user_type(1)
        platforms = self.select_user_type(3)
        types = ["food", "clothes", "daily use", "digital", "office supplies", "sports"]
        
        while i < self.n:
            ono = str(random.randint(100000, 999999))
            uno = random.choice(buyers)[0]
            sno = random.choice(sellers)[0]
            platform_name = random.choice(platforms)[0]
            otime = datetime.datetime.fromtimestamp(self.random_date_order()).strftime('%Y-%m-%d')
            ovalue = round(random.uniform(0, 999), 2)
            onum = random.randint(1, 100)
            otype = random.choice(types)
            one_value = (ono, otime, ovalue, uno, sno, platform_name, otype, onum)
            if self.check_valid(one_value):
                values.append(one_value)
                i += 1

        return values           

    def insert_values_order(self):
        """
        Insert values into dashboard_orderinformation.
        """
        val = self.generator_order()
        sql = """
              INSERT INTO 
              dashboard_orderinformation(ono, otime, ovalue, username_id, sellername_id, platformname_id, otype, onum) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()
    
        
if __name__ == '__main__':
    order_gen = OrderGenerator(400)
    order_gen.insert_values_order()