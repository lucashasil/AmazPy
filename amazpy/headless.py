from amazpy.product_database import ProductDatabase
from amazpy.product_scraper import ProductScraper
from datetime import datetime
import json
import xlsxwriter
import re

class Headless:
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        db = ProductDatabase()
        with open('urls.json') as user_file:
            file_contents = user_file.read()

        parsed_json = json.loads(file_contents)
        urls = parsed_json['product_urls']

        entries  = []
        worksheets = []
        workbook = xlsxwriter.Workbook('amazpy.xlsx')
        for url in urls:
            scraper = ProductScraper()
            info = scraper.scrape_product_info(url)
            title = info["title"]
            price = info["price"]
            db.insert_record(datetime.now().strftime("%m/%d/%Y, %H:%M"), price, title, url)
            url_entries = db.select_records(url)
            entries.append(url_entries)
            special_characters = r'[\[\]:*?/\\]'
            title = re.sub(special_characters, '', title)[:30]
            worksheet = workbook.add_worksheet(title)
            worksheets.append(worksheet)

            for entry_index, entry in enumerate(entries):
                worksheet = worksheets[entry_index]
                for sub_entry in entry:
                    worksheet.write_row('A' + str(entry.index(sub_entry) + 1), sub_entry)
        workbook.close()


