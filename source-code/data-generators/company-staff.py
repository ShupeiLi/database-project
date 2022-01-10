# -*- coding: utf-8 -*-

import mysql.connector
import random


class CompanyStaffGenerator():
    """
    Generate company-staff information.
    """
    
    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ShupeiLi',  # !!!remember to change the password
            database='safe'
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
    
    def generator_relations(self):
        """
        Generate relations: Company - Delivery Staff
        """
        values = []
        companys = self.select_user_type(2)
        delivery_staffs = self.select_user_type(4)
        
        for i in range(len(delivery_staffs)):
            company = random.choice(companys)[0]
            values.append((delivery_staffs[i][0], company))
            
        return values
    
    def insert_values_relations(self):
        """
        Insert values into dashboard_companystaff.
        """
        val = self.generator_relations()
        sql = """
              INSERT INTO 
              dashboard_companystaff(pno_id, tno_id) 
              VALUES (%s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()

    
if __name__ == '__main__':
    relation_gen = CompanyStaffGenerator()
    relation_gen.insert_values_relations()