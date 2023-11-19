from amazpy.product_database import ProductDatabase
from amazpy.product_scraper import ProductScraper
from amazpy.email import Email
from datetime import datetime
from typing import Any
import json
import xlsxwriter
import re
import time


class Headless:
    def __init__(self, email_credentials: str):
        self.email_credentials = email_credentials
        self.db = ProductDatabase()
        self.scrape()

        # Continually scrape every hour, this will block the main thread
        # but that is fine as we have nothing else to do (unlike the GUI)
        while True:
            time.sleep(60 * 60)
            self.scrape()

    def construct_email_message(self, entries: list[Any]) -> str:
        message = ""
        for entry in entries:
            if self.should_send_alert(entry):
                message += (f"{entry[-1][3]} - {entry[-1][4]}\n === ${entry[-1][2]} ===\n\n")
        # We need to encode the string as UTF-8 to make it valid for sending as an email
        return message.encode("utf-8")

    def should_send_alert(self, entries: list[Any]) -> bool:
        average_price = None

        # Calculate the average price for the list of entries which will be used
        # to determine if we should send an alert. An important note here is that we
        # exclude the latest entry from the average calculation.
        excl_list = entries[:-1]
        running_price = 0.0
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

        # Entries is a list of lists, where each list contains the entries for a single URL
        entries = []

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

            # Retrieve product information from database for a SINGLE URL/listing
            url_entries = self.db.select_records(url)
            entries.append(url_entries)

            # Create worksheet with sanitized title, xlsx worksheets cannot be longer than 31 characters
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

        # Close Excel workbook
        workbook.close()

        # Send email with price drop notification if necessary
        Email(self.email_credentials, self.construct_email_message(entries))

        print("successfully finished scraping, waiting for next run...")
