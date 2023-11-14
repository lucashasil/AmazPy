import requests

import tkinter as tk

import sqlite3

from bs4 import BeautifulSoup

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
    cur.execute("CREATE TABLE IF NOT EXISTS product(id INTEGER PRIMARY KEY, title TEXT, price TEXT, url TEXT)")
    cur.execute("INSERT INTO product VALUES(NULL, ?, ?, ?)", (title, combined_price, url))
    con.commit()

    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()
    new_rows = []
    for i in range(1,len(rows)+1):
        cols = []
        for j in range(4):
            e = tk.Entry(app, relief=tk.GROOVE)
            e.grid(row=i, column=j, sticky=tk.NSEW)
            e.insert(tk.END, rows[i-1][j])
            cols.append(e)
        new_rows.append(cols)

app = App()
app.geometry("600x400")
product_url = tk.StringVar()

url_label = tk.Label(app, text="Product URL")
url_entry = tk.Entry(app, textvariable=product_url)
sub_btn=tk.Button(app ,text = 'Submit', command = submit)

url_label.grid(row=0,column=0)
url_entry.grid(row=0,column=1)
sub_btn.grid(row=0,column=2)

app.mainloop()

