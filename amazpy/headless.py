from amazpy.product_database import ProductDatabase
from amazpy.product_scraper import ProductScraper
from datetime import datetime
import threading
import json
import xlsxwriter
import re


class Headless:
    def __init__(self):
        self.db = ProductDatabase()
        self.scrape()

        # Use a threaded timer to periodically fetch new data for the listing
        # This will run every hour
        threading.Timer(60 * 60, self.scrape).start()

    def scrape(self):
        # Open URLs file
        with open('urls.json', 'r') as user_file:
            file_contents = user_file.read()

        # Parse JSON data
        parsed_json = json.loads(file_contents)
        urls = parsed_json['product_urls']

        # Prepare data structures
        entries = []
        worksheets = []

        # Create Excel workbook
        workbook = xlsxwriter.Workbook('amazpy.xlsx')

        # Process each URL
        for url in urls:
            # Scrape product information
            scraper = ProductScraper()
            info = scraper.scrape_product_info(url)
            title = info["title"]
            price = info["price"]

            # Save product information to database
            self.db.insert_record(datetime.now().strftime("%m/%d/%Y, %H:%M"), price, title, url)

            # Retrieve product information from database
            url_entries = self.db.select_records(url)
            entries.append(url_entries)

            # Create worksheet with sanitized title
            special_characters = r'[\[\]:*?/\\]'
            title = re.sub(special_characters, '', title)[:30]
            worksheet = workbook.add_worksheet(title)
            worksheets.append(worksheet)

            # Write product information to worksheet
            for entry in entries:
                for sub_entry in entry:
                    worksheet.write_row('A' + str(entry.index(sub_entry) + 1), sub_entry[1:])

        # Close Excel workbook
        workbook.close()

        print("successfully finished scraping, waiting for next run...")
