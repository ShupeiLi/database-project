import mysql.connector
import random


class SellerRateGenerator():
    """
    Generate seller's rate scores.
    """

    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ShupeiLi', # !!! Change password
            database='safe'
        )

    def insert_values(self):
        """
        Insert values into dashboard_rateseller.
        """
        val = self.generator()
        sql = """
              INSERT INTO 
              dashboard_rateseller(sellername_id, quality, price, look, delivery, service) 
              VALUES (%s, %s, %s, %s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()

    def get_name(self):
        """
        Get all seller names from register_newuser.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT username
               FROM register_newuser
               WHERE
                   utype = 'seller'
               """)
        records = cursor.fetchall()
        cursor.close()
        return records

    def check_exist(self, val):
        """
        Check the existence of the users.

        Args:
            val: str.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM dashboard_rateseller
               WHERE
                   sellername_id = '{}'
               """.format(val))
        records = cursor.fetchall()
        cursor.close()
        if len(records) > 0:
            return False
        else:
            return True

    def generator(self):
        """
        Generate rate scores.
        """
        values = []
        names = self.get_name()
        i = 0
        while i < len(names):
            one_value = [names[i][0]]
            for j in range(5):
                one_value.append(round(random.random()*5, 1))
            one_value = tuple(one_value)
            if self.check_exist(one_value[0]):
                values.append(one_value)
            i += 1

        return values


if __name__ == '__main__':
    rate_gen = SellerRateGenerator()
    rate_gen.insert_values()
