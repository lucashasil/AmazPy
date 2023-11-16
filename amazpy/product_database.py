
import sqlite3

class ProductDatabase:
    def __init__(self, db_name="amazpy.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, date TEXT, price TEXT, url TEXT)")
        self.connection.commit()

    def insert_record(self, date, price, url):
        self.cursor.execute("INSERT INTO product VALUES(NULL, ?, ?, ?)", (date, price, url))
        self.connection.commit()

    def select_records(self, url):
        self.cursor.execute("SELECT * FROM product WHERE url=?", (url, ))
        return self.cursor.fetchall()
