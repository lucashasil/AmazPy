import requests

import tkinter as tk
from tkinter import ttk

import sqlite3

from bs4 import BeautifulSoup

from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()

def submit() :
    base_url = "https://amazon.com"
    url = product_url.get()

    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"
    }

    response = requests.get(base_url, headers=headers)
    cookies = response.cookies

    r2 = requests.get(url, headers=headers, cookies=cookies)

    soup = BeautifulSoup(r2.content, features="html.parser")

    title = soup.find(id='productTitle').text.strip()

    whole_span = soup.find('span', class_='a-price-whole')
    fraction_span = soup.find('span', class_='a-price-fraction')

    whole_text = whole_span.text if whole_span else ''
    fraction_text = fraction_span.text if fraction_span else ''

    combined_price = whole_text + fraction_text

    con = sqlite3.connect("amazpy.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, date TEXT, price TEXT, url TEXT)")
    cur.execute("INSERT INTO product VALUES(NULL, ?, ?, ?)", (datetime.now().strftime("%m/%d/%Y, %H:%M"), combined_price, url))
    con.commit()

    cur.execute("SELECT * FROM product WHERE url=?", (url, ))
    rows = cur.fetchall()

    label = tk.Label(app, text="Product Price History", font=("Arial", 26)).grid(row=1, columnspan=4)
    cols = ('Date', 'Price', 'URL')
    listBox = ttk.Treeview(app, columns=cols, show='headings')
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=2,column=0,columnspan=6)

    for row in rows:
        listBox.insert("", "end", values=(row[1], row[2], row[3]))

app = App()
app.geometry("1000x600")
product_url = tk.StringVar()

url_label = tk.Label(app, text="Product URL").grid(row=0,column=0)
url_entry = tk.Entry(app, textvariable=product_url).grid(row=0,column=1)
sub_btn=tk.Button(app ,text = 'Submit', command = submit).grid(row=0,column=2)

app.mainloop()

