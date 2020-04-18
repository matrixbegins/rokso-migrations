import mysql.connector
from mysql.connector import Error
from .connectionManager import ConnectionManager
from time import time


class DBManager:
    def __init__(self, config):
        self.config = config

    def execute_query(self, sql):
        connection = ConnectionManager(self.config).get_connection()
        try:
            cursor = connection.cursor()
            print("\nExecuting ", sql )
            tic = time()
            cursor.execute(sql)
            toc = time()
            print(">> Time taken: {}secs ".format(round(toc - tic, 4)) )
            return cursor.fetchall()

        except Error as e:
            print("There was an error executing sql:: " + sql, e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()

