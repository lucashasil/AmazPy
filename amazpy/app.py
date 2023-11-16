import tkinter as tk
import threading
from tkinter import ttk
from datetime import datetime
from amazpy.product_scraper import ProductScraper
from amazpy.product_database import ProductDatabase

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

        # Use a threaded timer to periodically fetch new data for the listing
        # This will run every hour
        threading.Timer(60 * 60, self.submit).start()

    def update_listbox(self, rows):
        for row in self.listBox.get_children():
            self.listBox.delete(row)

        for row in rows:
            self.listBox.insert("", "end", values=(row[1], row[2], row[3]))