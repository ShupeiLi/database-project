import mysql.connector
import random


class CompRateGenerator:
    """
    Generate seller's rate scores.
    """

    def __init__(self):
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ShupeiLi',
            database='safe'
        )

    def insert_values(self):
        """
        Insert values into dashboard_ratedelivcomp.
        """
        val = self.generator()
        sql = """
              INSERT INTO 
              dashboard_ratedelivcomp(compname_id, speed, package, perfection, service, timely_feedback) 
              VALUES (%s, %s, %s, %s, %s, %s)
              """
        cursor = self.db.cursor()
        cursor.executemany(sql, val)
        self.db.commit()
        cursor.close()

    def get_name(self):
        """
        Get all delivery company names from register_newuser.
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

    def check_exist(self, val):
        """
        Check the existence of the users.

        Args:
            val: str.
        """
        cursor = self.db.cursor()
        cursor.execute("""
               SELECT *
               FROM dashboard_ratedelivcomp
               WHERE
                   compname_id = '{}'
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
    rate_gen = CompRateGenerator()
    rate_gen.insert_values()
