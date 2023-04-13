import sqlite3


class Database(object):
    """sqlite3 database class that holds testers jobs"""
    __DB_LOCATION = "database.s3db"

    def __init__(self):
        """Initialize db class variables"""
        self.__connection = sqlite3.connect(Database.__DB_LOCATION)
        self.cur = self.__connection.cursor()

    def close(self):
        """close sqlite3 connection"""
        self.__connection.close()

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()

    def execute(self, sql_query, *params):
        """execute a row of data to current cursor"""
        self.cur.execute(sql_query, params)

    def commit(self):
        """commit changes to database"""
        self.__connection.commit()
