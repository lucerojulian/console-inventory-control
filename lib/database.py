import sqlite3


class Database(object):
    __DB_LOCATION = "database.s3db"

    def __init__(self):
        self.__connection = sqlite3.connect(Database.__DB_LOCATION)
        self.cur = self.__connection.cursor()

    def close(self):
        self.__connection.close()

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()

    def execute(self, sql_query, *params):
        self.cur.execute(sql_query, params)

    def commit(self):
        self.__connection.commit()
