from amazpy.product_database import ProductDatabase
from amazpy.product_scraper import ProductScraper
from amazpy.email import Email
from datetime import datetime
from typing import Any
import threading
import json
import xlsxwriter
import re


class Headless:
    def __init__(self, email_credentials: str):
        self.email_credentials = email_credentials
        self.db = ProductDatabase()
        self.scrape()

        # Use a threaded timer to periodically fetch new data for the listing
        # This will run every hour
        threading.Timer(60 * 60, self.scrape).start()

    def should_send_alert(self, entries: list[Any]) -> bool:
        average_price = None

        # Calculate the average price for the list of entries which will be used
        # to determine if we should send an alert. An important note here is that we
        # exclude the latest entry from the average calculation.
        excl_list = entries[:-1]

        for entry in excl_list:
            # Price is the third column of a retrieved row
            running_price += float(entry[2])
            average_price = running_price / len(excl_list)

        # If the latest entry is at least 30% below the average price, send an alert
        return float(entries[-1][2]) <= average_price * 0.7

    def scrape(self):
        # Open URLs file
        with open("urls.json", "r") as user_file:
            file_contents = user_file.read()

        # Parse JSON data
        parsed_json = json.loads(file_contents)
        urls = parsed_json["product_urls"]

        # Prepare data structures
        entries = []
        worksheets = []

        # Create Excel workbook
        workbook = xlsxwriter.Workbook("amazpy.xlsx")

        # Process each URL
        for url in urls:
            # Scrape product information
            scraper = ProductScraper()
            info = scraper.scrape_product_info(url)
            title = info["title"]
            price = info["price"]

            # Save product information to database
            self.db.insert_record(
                datetime.now().strftime("%m/%d/%Y, %H:%M"), price, title, url
            )

            # Retrieve product information from database
            url_entries = self.db.select_records(url)
            entries.append(url_entries)

            # Create worksheet with sanitized title
            special_characters = r"[\[\]:*?/\\]"
            title = re.sub(special_characters, "", title)[:30]
            worksheet = workbook.add_worksheet(title)
            worksheets.append(worksheet)

            # Write product information to worksheet
            for entry in entries:
                for sub_entry in entry:
                    worksheet.write_row(
                        "A" + str(entry.index(sub_entry) + 1), sub_entry[1:]
                    )

        # Close Excel workbook
        workbook.close()

        if self.should_send_alert(entries):
            email = Email(self.email_credentials)

        print("successfully finished scraping, waiting for next run...")
