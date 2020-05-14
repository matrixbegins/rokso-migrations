import mysql.connector
from mysql.connector import Error


class ConnectionManager:
    def __init__(self, config):
        try:
            self.connection = mysql.connector.connect(**config)
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_info)

        except Error as e:
            print("Error while connecting to MySQL \n", e)
            raise e


    def get_connection(self):
        return self.connection

    def close_connection(self):
        if (self.connection.is_connected()):
            self.connection.close()

