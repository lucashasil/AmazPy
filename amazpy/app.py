import tkinter as tk
import threading
from tkinter import ttk
import sv_ttk
from datetime import datetime
from amazpy.product_scraper import ProductScraper
from amazpy.product_database import ProductDatabase
from typing import Any


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.product_url = tk.StringVar()
        self.create_widgets()

        self.title("AmazPy")
        sv_ttk.set_theme("dark")

    def create_widgets(self) -> None:
        url_label = ttk.Label(self, text="Product URL:", width=25)
        url_label.configure(anchor="center")
        url_label.grid(row=0, column=0, sticky="nsew")

        url_entry = ttk.Entry(self, textvariable=self.product_url, width=50)
        url_entry.grid(row=0, column=1, sticky="nsew")

        sub_btn = ttk.Button(self, text="Submit", command=self.submit, width=20)
        sub_btn.grid(row=0, column=2, sticky="nsew")

        self.label = ttk.Label(self, text="Product Price History", font=("Arial", 26))
        self.label.configure(anchor="center")
        self.label.grid(row=1, columnspan=3, sticky="nsew")

        cols = ("Date", "Price", "Title", "URL")
        self.listBox = ttk.Treeview(self, columns=cols, show="headings")
        self.listBox.tag_configure("gray", background="#3C3C3C")
        self.listBox.tag_configure("highlight", background="#FFD465")

        for i in range(len(cols)):
            self.listBox.heading(i, text=cols[i])

        self.listBox.grid(row=2, column=0, columnspan=3, sticky="nsew")

    def get_average_price(self, rows: list[Any]) -> float:
        total = 0.0
        for row in rows:
            # Price is the third column of a retrieved row
            total += float(row[2])
        return total / len(rows)

    def submit(self) -> None:
        url = self.product_url.get()
        scraper = ProductScraper()

        info = scraper.scrape_product_info(url)
        title = info["title"]
        price = info["price"]

        db = ProductDatabase()
        date = datetime.now().strftime("%m/%d/%Y, %H:%M")
        db.insert_record(date, price, title, url)

        rows: list[Any] = db.select_records(url)
        self.update_listbox(rows)

        # Use a threaded timer to periodically fetch new data for the listing
        # This will run every hour
        threading.Timer(60 * 60, self.submit).start()

    def update_listbox(self, rows: list[Any]) -> None:
        average_price = self.get_average_price(rows)
        # Highlight a row as significantly discounted if it is at least 30% below the average
        highlight_price = average_price * 0.7

        for row in self.listBox.get_children():
            self.listBox.delete(row)

        for i, row in enumerate(rows):
            if float(row[2]) <= highlight_price:
                self.listBox.insert(
                    "", "end", values=(row[1], row[2], row[3], row[4]), tags="highlight"
                )
            elif i % 2 == 0:
                self.listBox.insert(
                    "", "end", values=(row[1], row[2], row[3], row[4]), tags="gray"
                )
            else:
                self.listBox.insert("", "end", values=(row[1], row[2], row[3], row[4]))
