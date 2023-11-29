"""The non-GUI runtime for AmazPy."""
import json
import re
import time
from datetime import datetime
from typing import Any

import xlsxwriter
from requests.exceptions import RequestException

from amazpy.email import Email
from amazpy.product_database import ProductDatabase
from amazpy.product_scraper import ProductScraper


class Headless:
    def __init__(self, email_credentials: str, scrape_interval: int = 3600):
        """A class representing the headless invocation of the application.

        Args:
            email_credentials (str): a string representing the user's email
            credentials in <email>:<app_password> format
        """

        self.email_credentials = email_credentials
        self.db = ProductDatabase()

        # Perform a scrape as soon as the application is started
        self.scrape()

        # Continually scrape every hour, this will block the main thread
        # but that is fine as we have nothing else to do (unlike the GUI)
        while True:
            time.sleep(scrape_interval)
            self.scrape()

    def construct_email_message(self, entries: list[Any]) -> str:
        """Construct the email notification message that will be sent to the user.

        Args:
            entries (list[Any]): a list of multiple product entries fetched from the database

        Returns:
            str: a string representing the email message
        """

        # Construct the body of the notification email by iterating over the list of entries
        message = ""
        for entry in entries:
            if self.should_send_alert(entry):
                message += self.process_entry_region(entry[-1])
        # We need to encode the string as UTF-8 to make it valid for sending as an email
        return message.encode("utf-8")

    def process_entry_region(self, sub_entry: Any) -> str:
        """Determine the correct regional information to use for a given product entry.

        Args:
            sub_entry (Any): the actual row in the product entry that we are processing

        Returns:
            str: a string containing the correctly formatted product information for notification
        """

        # Extract the region from the product URL, this will be one of:
        # com, com.au, co.uk, or ca
        region_pattern = re.compile(r"https:\/\/www\.amazon\.(com\.au|com|co\.uk|ca)")
        match = re.search(region_pattern, sub_entry[4])

        # Store a mapping of region to currency code and symbol
        currency_mapping = {
            "com": ("USD", "$"),
            "com.au": ("AUD", "$"),
            "co.uk": ("GBP", "£"),
            "ca": ("CAD", "$"),
        }

        # If we have a match, we can use it to determine the
        # correct currency code and symbol for the entry
        if match and match.group(1) in currency_mapping:
            currency_code, currency_symbol = currency_mapping[match.group(1)]
            return (
                f"{sub_entry[3]} - {sub_entry[4]}\n ==="
                f" {currency_symbol}{sub_entry[2]} {currency_code} ===\n\n"
            )

        # Handle the case where match_group is not in the mapping
        return ""

    def should_send_alert(self, sub_entries: list[Any]) -> bool:
        """Determine whether or not an email alert should be sent for a
        given list of product entries

        Args:
            sub_entries (list[Any]): a list of entries for a SINGLE product to be checked

        Returns:
            bool: a boolean representing whether or not an alert should be sent
        """

        # Early return if we don't have enough entries to do anything meaningful
        if sub_entries is None or len(sub_entries) == 0:
            return False

        average_price = None

        # Calculate the average price for the list of entries which will be used
        # to determine if we should send an alert. An important note here is that we
        # exclude the latest entry from the average calculation.
        excl_list = sub_entries[:-1]
        running_price = 0.0
        for entry in excl_list:
            # Price is the third column of a retrieved row
            running_price += float(entry[2])
            average_price = running_price / len(excl_list)

        # If the latest entry is at least 30% below the average price, send an alert
        try:
            return float(sub_entries[-1][2]) <= average_price * 0.7
        except TypeError:
            print(
                "There was an issue calculating the average price for most recent"
                " scrape, skipping..."
            )
            return False

    def scrape(self):
        """Scrape product information from Amazon and save it to the database."""
        # Open URLs file
        with open("urls.json", "r", encoding="utf-8") as user_file:
            file_contents = user_file.read()

        # Parse JSON data
        urls = json.loads(file_contents)["product_urls"]

        # Process each URL to get them in a 'cleansed' format
        pattern = re.compile(
            r"https:\/\/www\.amazon\.(com\.au|com|co\.uk|ca)\/.*?\/(dp\/[A-Z0-9]+)\/?.*"
        )

        # Cleanse each URL in the input list
        for i, url in enumerate(urls):
            url = re.sub(pattern, r"https://www.amazon.\1/\2", url)
            urls[i] = url

        # Entries is a list of lists, where each list contains the entries for a single URL
        entries = []

        # Create Excel workbook
        workbook = xlsxwriter.Workbook("amazpy.xlsx")

        # Process each URL
        for url in urls:
            # Scrape product information
            try:
                scraper = ProductScraper()
                info = scraper.scrape_product_info(url)
                title = info["title"]
                price = info["price"]

                # Price could not be scraped, so return early
                if price == "":
                    print(
                        "This product might not currently be available or you may be"
                        " using an incorrect store region."
                    )
                    return

                date = datetime.now().strftime("%m/%d/%Y, %H:%M")

                # Save product information to database
                self.db.insert_record(date, price, title, url)

                # Retrieve product information from database for a SINGLE URL/listing
                url_entries = self.db.select_records(url)
                entries.append(url_entries)

                # Create worksheet with sanitized title, xlsx worksheets cannot
                # be longer than 31 characters
                special_characters = r"[\[\]:*?/\\]"
                title = re.sub(special_characters, "", title)[:30]

                # We want to create a new worksheet for each URL/listing
                worksheet = workbook.add_worksheet(title)

                # Write product information to worksheet
                for entry in entries:
                    for sub_entry in entry:
                        worksheet.write_row(
                            "A" + str(entry.index(sub_entry) + 1), sub_entry[1:]
                        )
            except RequestException:
                print(
                    "There was an issue fetching product information from Amazon,"
                    " please wait for the next retry or restart..."
                )

        # Close Excel workbook once finished to avoid memory leaks
        workbook.close()

        # Send email with price drop notification if necessary
        email_message = self.construct_email_message(entries)
        # Make sure we check that the email body is non-empty before we try to construct one
        if email_message != b"":
            Email(self.email_credentials, email_message)

        print("successfully finished scraping, waiting for next run...")
