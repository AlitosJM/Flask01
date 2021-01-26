from flask import Flask
from flask_mysqldb import MySQL


class DataBase:

    def __init__(self, myapp, article_id):
        self.article_id = article_id
        self.mysql = MySQL(myapp)

    def __enter__(self):
        self.cursor = self.mysql.connection.cursor()
        self.cursor.execute("SELECT * FROM Articles WHERE id = %s", (self.article_id,))
        self._article = self.cursor.fetchall()

    @property
    def query(self):
        return self._article

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        # del DataBase.mysql
