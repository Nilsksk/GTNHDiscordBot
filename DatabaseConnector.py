import mariadb
import sys
import os
from tabulate import tabulate


class DatabaseConnector:
    def __init__(self):
        self.db_connection = None
        self.cursor = None
        self.db_user_name = os.getenv('DB_USER_NAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_host = os.getenv('DB_HOST')
        self.db_port = int(os.getenv('DB_PORT'))
        self.db_name = os.getenv('DB_NAME')

    def connect(self):
        try:
            self.db_connection = mariadb.connect(
                user=self.db_user_name,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name

            )
        except mariadb.Error as err:
            print("Error connecting to MariaDB Platform: {}".format(err))
            sys.exit(1)

    def get_cursor(self):
        if self.db_connection:
            if not self.cursor:
                self.cursor = self.db_connection.cursor()
                return self.cursor
            else:
                return self.cursor

    def execute_query(self, query, cursor):
        cursor.execute(query)
        if self.cursor.rowcount != 0:
            data_nested_list = []
            for data in self.cursor:
                data_nested_list.append([data[0], data[1], data[2], data[3]])

            data_pretty = tabulate(data_nested_list)
            return data_pretty
        else:
            print("Now Database entry found for provided query!")
            return None
