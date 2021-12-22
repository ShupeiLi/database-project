# -*- coding: utf-8 -*-

import mysql.connector
import random
from datetime import datetime
import time
import string
from phone_gen import PhoneNumber
from faker import Faker


class UserGenerator():
    """
    Generate user information.
    
    Args:
        n: number of accounts.
        utype: {0: 'buyer', 1: 'seller', 2: 'company', 3: 'platform', 4: 'delivery'}
    """
    
    def __init__(self, n, utype):
        self.n = n
        utype_dict = {0: 'buyer', 1: 'seller', 2: 'company', 3: 'platform', 4: 'delivery'}
        self.utype = utype_dict[utype]
        self.db = mysql.connector.connect(
                    host = 'localhost',
                    user = 'root',
                    password = 'ShupeiLi',
                    database = 'safe'
                    )
    
    def insert_values(self):
        """
        Insert values into register_newuser.
        """
        val = self.generator()
        sql = """
              INSERT INTO 
              register_newuser(registerdate, username, password, utype, email, tel, companyname, address, is_active, is_staff, is_superuser, last_login) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()
        
    def check_valid(self, val):
        """
        Check the validity of the values.
        
        Args:
            val: Tuple-like.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM register_newuser
               WHERE
                   email = '{}'
               OR username = '{}'
               """.format(val[4], val[1]))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return False
        else:
            return True
        
    def random_char(self, y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
        
    def generator(self):
        """
        Generate accounts.
        """
        values = []
        phone = PhoneNumber('CN')
        fake = Faker()
        i = 0
        
        while i < self.n:
            one_value = []
            date = datetime.fromtimestamp(random.randint(1200000000, int(time.time()))).strftime('%Y-%m-%d')
            name = fake.name()
            one_value.append(date)
            one_value.append(name)
            one_value.append("123")
            one_value.append(self.utype)
            one_value.append(self.random_char(7)+"@gmail.com")
            one_value.append(phone.get_number(full=True))
            if self.utype == 'company' or self.utype == 'platform':
                one_value.append(name + " Company")
            else:
                one_value.append("Individual")
            one_value.append(fake.address())
            one_value.append(True)
            one_value.append(False)
            one_value.append(False)
            one_value.append(date)
            one_value = tuple(one_value)
            if self.check_valid(one_value):
                values.append(one_value)
                i += 1
        
        return values
    
    
if __name__ == '__main__':
    user_gen = UserGenerator(5, 1)
    user_gen.insert_values()