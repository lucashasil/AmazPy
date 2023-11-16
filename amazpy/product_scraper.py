import requests
from bs4 import BeautifulSoup

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
