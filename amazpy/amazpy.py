import requests
import tkinter as tk
from tkinter import ttk
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

class ProductScraper:
    def __init__(self):
        self.base_url = "https://amazon.com"
        self.headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"
        }
        self.cookies = None

    def scrape_product_price(self, url):
        response = requests.get(self.base_url, headers=self.headers)
        self.cookies = response.cookies

        r2 = requests.get(url, headers=self.headers, cookies=self.cookies)
        soup = BeautifulSoup(r2.content, features="html.parser")

        whole_span = soup.find('span', class_='a-price-whole')
        fraction_span = soup.find('span', class_='a-price-fraction')

        whole_text = whole_span.text if whole_span else ''
        fraction_text = fraction_span.text if fraction_span else ''
        combined_price = whole_text + fraction_text

        return combined_price

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

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.product_url = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        url_label = tk.Label(self, text="Product URL")
        url_label.grid(row=0, column=0, sticky='nsew')

        url_entry = tk.Entry(self, textvariable=self.product_url)
        url_entry.grid(row=0, column=1, sticky='nsew')

        sub_btn = tk.Button(self, text='Submit', command=self.submit)
        sub_btn.grid(row=0, column=2, sticky='nsew')

        self.label = tk.Label(self, text="Product Price History", font=("Arial", 26))
        self.label.grid(row=1, columnspan=3, sticky='nsew')

        cols = ('Date', 'Price', 'URL')
        self.listBox = ttk.Treeview(self, columns=cols, show='headings')

        for i in range(len(cols)):
            self.listBox.heading(i, text=cols[i])

        self.listBox.grid(row=2, column=0, columnspan=3, sticky='nsew')

    def submit(self):
        url = self.product_url.get()
        scraper = ProductScraper()
        price = scraper.scrape_product_price(url)

        db = ProductDatabase()
        date = datetime.now().strftime("%m/%d/%Y, %H:%M")
        db.insert_record(date, price, url)

        rows = db.select_records(url)
        self.update_listbox(rows)

    def update_listbox(self, rows):
        for row in self.listBox.get_children():
            self.listBox.delete(row)

        for row in rows:
            self.listBox.insert("", "end", values=(row[1], row[2], row[3]))

if __name__ == "__main__":
    app = App()
    app.mainloop()
