"""Contains the logic required for performing the actual
scraping of product information from Amazon.
"""
import sys

import requests
from bs4 import BeautifulSoup


class ProductScraper:
    def __init__(self, base_url: str = "https://amazon.com"):
        """This class represents a web scraper which will be used to perform
        the actual scraping of product information from Amazon.
        """

        self.base_url = base_url

        # We need to set the headers appropriately to ensure that the request
        # is not blocked by Amazon. The User-Agent corresponds to a Firefox browser
        # on MacOS
        self.headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0)"
                " Gecko/20100101 Firefox/119.0"
            ),
        }

        # Store the cookies from the initial request for future reusability
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
            response = requests.get(self.base_url, headers=self.headers, timeout=30)
            self.cookies = response.cookies
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit("There was an issue performing initial cookie request...")

        try:
            # Perform second request to scrape the actual product information using
            # the previously fetched cookies
            r2 = requests.get(
                url, headers=self.headers, cookies=self.cookies, timeout=30
            )

            # Use BeautifulSoup to parse the HTML response
            soup = BeautifulSoup(r2.content, features="html.parser")

            # Try and extract the product listing title
            product_title = soup.find("span", id="productTitle").text.strip()

            # Try and extract the product listing price, note that this is stored
            # in two different HTML elements, split by the whole price and the fraction
            # e.g. 29.99 would be two spans with values of 29 and 99 respectively
            whole_span = soup.find("span", class_="a-price-whole")
            fraction_span = soup.find("span", class_="a-price-fraction")

            # Combine the whole and fraction price values into a single string if possible
            whole_text = whole_span.text if whole_span else ""
            fraction_text = fraction_span.text if fraction_span else ""
            combined_price = whole_text + fraction_text

            # Return a dictionary containing the product title and price
            return {"title": product_title, "price": combined_price}
        except (AttributeError, requests.exceptions.RequestException) as e:
            print(
                "There was an issue fetching product information from Amazon, please"
                " wait for the next retry or restart..."
            )
            raise e
