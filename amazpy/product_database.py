
import sqlite3
from types import Any

class ProductDatabase:
    def __init__(self, db_name: str = "amazpy.db") -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, date TEXT, price TEXT, url TEXT)")
        self.connection.commit()

    def insert_record(self, date, price, url) -> None:
        self.cursor.execute("INSERT INTO product VALUES(NULL, ?, ?, ?)", (date, price, url))
        self.connection.commit()

    def select_records(self, url) -> list[Any]:
        self.cursor.execute("SELECT * FROM product WHERE url=?", (url, ))
        return self.cursor.fetchall()
