"""Handles the logic for reading and writing from/to the SQLite database."""
import sqlite3
import sys
from typing import Any


class ProductDatabase:
    def __init__(self) -> None:
        """This class represents the SQLite database connection that
        is solely used for storing and retrieving product information.
        """
        db_name = "amazpy.db"

        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            self.create_table()
        except Exception as e:
            print(e)
            sys.exit("There was an issue initializing the database...")

    def create_table(self) -> None:
        """Create a new product table in the database if it does not already exist."""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, date"
            " TEXT, title TEXT, price TEXT, url TEXT)"
        )
        self.connection.commit()

    def insert_record(self, date: str, price: str, title: str, url: str) -> None:
        """Insert a new product record into the database.

        Args:
            date (str): the datetime string for this record
            price (str): a string representation of the price in Dollars.Cents format
            title (str): the title of the product listing
            url (str): the full URL of the product listing
        """
        self.cursor.execute(
            "INSERT INTO product VALUES(NULL, ?, ?, ?, ?)",
            (date, price, title, url),
        )
        self.connection.commit()

    def select_records(self, url: str) -> list[Any]:
        """Return all records from the database for a given URL.

        Args:
            url (str): the URL of the product listing

        Returns:
            list[Any]: a list of tuples representing the rows of the database
        """
        self.cursor.execute("SELECT * FROM product WHERE url=?", (url,))
        return self.cursor.fetchall()
