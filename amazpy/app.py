"""The GUI runtime for AmazPy."""
import re
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from typing import Any

import sv_ttk
from requests.exceptions import RequestException

from amazpy.product_database import ProductDatabase
from amazpy.product_scraper import ProductScraper


class App(tk.Tk):
    def __init__(self):
        """A class representing the GUI runtime of the application. Inherits from Tkinter.
        """
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.product_url = tk.StringVar()
        self.create_widgets()

        self.title("AmazPy")
        sv_ttk.set_theme("dark")

    def create_widgets(self) -> None:
        """Create the Tkinter widgets for the GUI itself."""
        url_label = ttk.Label(self, text="Product URL:", width=25)
        url_label.configure(anchor="center")
        url_label.grid(row=0, column=0, sticky="nsew")

        url_entry = ttk.Entry(self, textvariable=self.product_url, width=50)
        url_entry.grid(row=0, column=1, sticky="nsew")

        sub_btn = ttk.Button(self, text="Submit", command=self.scrape, width=20)
        sub_btn.grid(row=0, column=2, sticky="nsew")

        self.label = ttk.Label(self, text="Product Price History", font=("Arial", 26))
        self.label.configure(anchor="center")
        self.label.grid(row=1, columnspan=3, sticky="nsew")

        cols = ("Date", "Price", "Title", "URL")
        self.list_box = ttk.Treeview(self, columns=cols, show="headings")
        self.list_box.tag_configure("gray", background="#3C3C3C")
        self.list_box.tag_configure("highlight", background="#FFD465")

        for (i , col) in enumerate(cols):
            self.list_box.heading(i, text=col)

        self.list_box.grid(row=2, column=0, columnspan=3, sticky="nsew")

    def get_average_price(self, rows: list[Any]) -> float:
        """Get the average price for a list of entries for a single product.

        Args:
            rows (list[Any]): a list of rows for a single product entry

        Returns:
            float: a float representing the average price for the product
        """

        total = 0.0
        for row in rows:
            # Price is the third column of a retrieved row
            total += float(row[2])
        return total / len(rows)

    def scrape(self) -> None:
        """Perform the actual scraping of product information from Amazon."""

        url = self.product_url.get()

        # Process URL into a 'cleansed' format
        pattern = re.compile(
            r"https:\/\/www\.amazon\.(com\.au|com|co\.uk|ca)\/.*?\/(dp\/[A-Z0-9]+)\/?.*"
        )
        url = re.sub(pattern, r"https://www.amazon.\1/\2", url)

        try:
            scraper = ProductScraper()
            info = scraper.scrape_product_info(url)
            title = info["title"]
            price = info["price"]

            # Price could not be scraped, so return early
            if price == "":
                print(
                    "This product might not currently be available or you may be using"
                    " an incorrect store region."
                )
                return

            db = ProductDatabase()
            date = datetime.now().strftime("%m/%d/%Y, %H:%M")
            db.insert_record(date, price, title, url)

            rows: list[Any] = db.select_records(url)
            self.update_list_box(rows)
        except RequestException:
            print(
                "There was an issue fetching product information from Amazon, please"
                " wait for the next retry or restart..."
            )

        # A threaded timer is used here to avoid blocking the main (GUI) thread
        # to avoid the GUI from freezing when performing rescrapes. Compare this to
        # the sleep used in the headless variant, where we need to block the main thread
        # to avoid concurrent database writes/reads across a single connection and multiple threads.
        # Rescrape every hour.
        threading.Timer(60 * 60, self.scrape).start()

    def update_list_box(self, rows: list[Any]) -> None:
        """Update the list_box (treeview) for the Tkinter GUI with the latest product information.

        Args:
            rows (list[Any]): a list of rows for a single product entry
        """

        average_price = self.get_average_price(rows)
        # Highlight a row as significantly discounted if it is at least 30% below the average
        highlight_price = average_price * 0.7

        for row in self.list_box.get_children():
            self.list_box.delete(row)

        for i, row in enumerate(rows):
            if float(row[2]) <= highlight_price:
                self.list_box.insert(
                    "",
                    "end",
                    values=(row[1], row[2], row[3], row[4]),
                    tags="highlight",
                )
            elif i % 2 == 0:
                self.list_box.insert(
                    "",
                    "end",
                    values=(row[1], row[2], row[3], row[4]),
                    tags="gray",
                )
            else:
                self.list_box.insert("", "end", values=(row[1], row[2], row[3], row[4]))
