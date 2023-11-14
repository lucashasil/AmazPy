import requests
from bs4 import BeautifulSoup

base_url = "https://amazon.com"
url = "https://www.amazon.com/dp/B074PVTPBW"

headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"
}

response = requests.get(base_url, headers=headers)
cookies = response.cookies

r2 = requests.get(url, headers=headers, cookies=cookies)

soup = BeautifulSoup(r2.content, features="html.parser")

pick = soup.find('span', attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})

whole_span = soup.find('span', class_='a-price-whole')
fraction_span = soup.find('span', class_='a-price-fraction')

whole_text = whole_span.text if whole_span else ''
fraction_text = fraction_span.text if fraction_span else ''

combined_price = whole_text + fraction_text

