# -*- coding: utf-8 -*-

import mysql.connector
import random


class DistributionGenerator():
    """
    Generate distribution information.
    """

    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ShupeiLi',  # !!!remember to change the password
            database='safe'
        )

    def insert_values(self):
        """
        Insert values into register_newuser.
        """
        val = self.generator()
        sql = """
              INSERT INTO 
              dashboard_distributioninformation(dpno, pno_id, dno_id, is_checked) 
              VALUES (%s, %s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()

    def get_tno(self):
        """
        Get all seller names from register_newuser.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT username
               FROM register_newuser
               WHERE
                   utype = 'company'
               """)
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_dno(self,val):
        """
        Get all dno from deliveryinformation.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT dno
               FROM dashboard_deliveryinformation
               WHERE
                 tno_id = '{}'
               """.format(val))
        records = cursor.fetchall()
        cursor.close()
        return records

    def get_pno(self, val):
        """
        Get all dno from deliveryinformation.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT pno_id
               FROM dashboard_companystaff
               WHERE
                 tno_id = '{}'
               """.format(val))
        records = cursor.fetchall()
        cursor.close()
        return records

    def check_exist(self, val):
        """
        Check the existence of the certain delivery order.

        Args:
            val: str.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM dashboard_distributioninformation
               WHERE
                   dno_id = '{}'
               """.format(val))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return False
        else:
            return True

    def select_unchecked(self):
        """
        Select unchecked delivery orders and corresponding product orders.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT dpno
               FROM dashboard_distributioninformation
               WHERE is_checked = False
               """)
        unchecked_records = cursor.fetchall()
        return unchecked_records

    def simulate_order_distribute(self):
        """
        Generate accounts.
        """
        values = []
        tno = self.get_tno()
        for i in range(len(tno)):
            comp_name = tno[i][0]
            dno = self.get_dno(comp_name)
            pno = self.get_pno(comp_name)
            for j in range(len(dno)):
                if self.check_exist(dno[j][0]):
                    # dpno, pno_id, dno_id, is_checked
                    pnos = random.sample(pno, min(5, len(pno)))
                    for k in range(len(pnos)):
                        one_pno = pnos[k][0]
                        one_value = (dno[j][0] + one_pno, one_pno, dno[j][0], 0)
                        values.append(one_value)

        if len(values) == 0:
            print("????????????????????????")
        else:
            sql = """
                INSERT INTO 
                dashboard_distributioninformation(dpno, pno_id, dno_id, is_checked) 
                VALUES (%s, %s, %s, %s)
                  """

            cursor = self.db.cursor()
            cursor.executemany(sql, values)
            self.db.commit()
            cursor.close()

    def simulate_distribution_confirm(self):
        """
        Simulation: Delivery man confirm delivery orders.
        """
        unchecked_list = self.select_unchecked()

        if len(unchecked_list) == 0:
            print("?????????????????????")
        else:
            cursor = self.db.cursor()
            sql = """
            UPDATE dashboard_distributioninformation
            set is_checked = True 
            WHERE dpno = %s
            """
            cursor.executemany(sql, unchecked_list)
            self.db.commit()


if __name__ == '__main__':
    model = DistributionGenerator()

    # ??????????????????
    model.simulate_order_distribute()

    # ????????????????????????
    model.simulate_distribution_confirm()