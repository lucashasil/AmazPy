import requests
import sys
from bs4 import BeautifulSoup


class ProductScraper:
    def __init__(self):
        """This class represents a web scraper which will be used to perform
        the actual scraping of product information from Amazon.
        """
        self.base_url = "https://amazon.com"
        self.headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0)"
                " Gecko/20100101 Firefox/119.0"
            ),
        }
        self.cookies = None

    def scrape_product_info(self, url: str) -> dict[str, str]:
        """Scrape relevant product information for a given product URL listing.

        Args:
            url (str): the URL of the product listing to scrape

        Returns:
            dict[str, str]: a dictionary containing the title and price of the product
        """

        # An initial request is made directly to the base URL of the relevant Amazon
        # site (e.g. amazon.com, amazon.com.au, etc.) in order to retrieve the necessary
        # cookies for the subsequent request to the product URL.
        try:
            response = requests.get(self.base_url, headers=self.headers)
            self.cookies = response.cookies
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit("There was an issue performing initial cookie request...")

        try:
            r2 = requests.get(url, headers=self.headers, cookies=self.cookies)
            soup = BeautifulSoup(r2.content, features="html.parser")
            product_title = soup.find("span", id="productTitle").text.strip()

            whole_span = soup.find("span", class_="a-price-whole")
            fraction_span = soup.find("span", class_="a-price-fraction")

            whole_text = whole_span.text if whole_span else ""
            fraction_text = fraction_span.text if fraction_span else ""
            combined_price = whole_text + fraction_text

            return {"title": product_title, "price": combined_price}
        except requests.exceptions.RequestException as e:
            print(
                "There was an issue fetching product information from Amazon, please"
                " wait for the next retry or restart..."
            )
            raise e
