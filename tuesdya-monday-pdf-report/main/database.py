#!/usr/bin/python

import mysql.connector
import base64


class MySQLDatabase:

    def __init__(self):
        self.host = '192.168.254.31'
        self.user = 'monitor'
        self.password = base64.b64decode('cEBzc3dvcmQ=')
        self.database = 'project_monitor_release_temp'
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user, password=self.password, host=self.host, database=self.database)
            self.mycursor = self.connection.cursor()
        except Exception as error:
            print "Error database:", error

    def select(self, sql_query):
        self.mycursor.execute(sql_query)
        return self.mycursor.fetchall()

    def insert(self, table, list_data):
        query = "INSERT INTO %s " % table
        query += "VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"
        try:
            self.mycursor.executemany(query, list_data)
        except:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()
        # self.connection.commit()

    def execute_sql(self, sql):
        try:
            self.mycursor.execute(sql)
        except:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()

    def foreign_key_func(self, func='enable', **kwargs):
        option = {
            'disable': '0',
            'enable': '1',
        }
        try:
            sql = "SET FOREIGN_KEY_CHECKS={func};".format(func=option[func])
        except Exception as error:
            print "Error database:", error
        self.mycursor.execute(sql)
        self.connection.commit()

    def execute_insert(self, table, list_data):
        query = "INSERT INTO %s " % table
        query += "VALUES (" + ",".join(["%s"] * len(list_data[0])) + ")"
        try:
            self.mycursor.executemany(query, list_data)
        except:
            self.connection.rollback()
            raise

    def close_connection(self):
        self.mycursor.close()
        self.connection.disconnect()


# db = MySQLDatabase()
# svc_sql = "SELECT `service_nam3e` FROM SERVICES WHERE `service_id`='{isvc}';"
# db.mycursor.execute(svc_sql.format(isvc=3))
# output = db.mycursor.fetchone()[0]
# print output

# if __name__ == '__main__':
#     hello = MySQLDatabase()
#     sql = "INSERT IGNORE INTO `PROBES` VALUES ('AB5LDCTUTJFUAH8P', 'updatename', '192.168.51.102', 'a0:99:9b:04:6c:ed', 'Idle', NOW(), NOW()) ON DUPLICATE KEY UPDATE `ip_address`='10.10.10.10', `last_updated`=NOW();"
#     hello.execute_sql(sql)
#     # hello.foreign_key_func()
#     # hello.insert('DESTINATIONS', [('NULL', 1, 'www.gh.comwqeqeqewqewqsfdsfssfdsfsdffsjieurfojfiosjfikdjkkxdfserfewsfefrfrgwww.gh.comwqeqeqewqewqsfdsfssfdsfsdffsjieurfojfiosjfikdjkkxdfserfewsfefrfrgwww.gh.comwqeqeqewqewqsfdsfssfdsfsdffsjieurfojfiosjfikdjkkxdfserfewsfefrfrg', 12356789, 'hello girl')])
#     # print int(hello.select("SELECT count(`result_id`) FROM TESTRESULTS")[0][0])