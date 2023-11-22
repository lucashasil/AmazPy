import pytest
from amazpy.product_scraper import ProductScraper
from requests import RequestException

test_product_url = "https://www.amazon.com/dp/B08KTZ8249"

@pytest.fixture
def product_scraper():
    return ProductScraper()

def test_scraper_headers(product_scraper):
    assert product_scraper.headers == {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0)"
            " Gecko/20100101 Firefox/119.0"
        ),
    }

def test_product_scraper_base_url(product_scraper):
    assert product_scraper.base_url == "https://amazon.com"

def test_product_scrape(product_scraper):
    product_info = product_scraper.scrape_product_info(test_product_url)

    assert product_scraper.cookies != None

    assert product_info != {}

    try:
        price = product_info["price"]
        assert float(price) > 0.0
    except ValueError as e:
        assert False

def test_scrape_product_info_successful(mocker):
    # Create a mocked response for the initial request
    mocker.patch("requests.get", return_value=mocker.Mock(cookies={"mock_cookie": "value"}))

    # Mock the response for the second request
    mocker.patch("requests.get", return_value=mocker.Mock(content="<html><span id='productTitle'>Mock Product</span><span class='a-price-whole'>29.</span><span class='a-price-fraction'>99</span></html>"))

    scraper = ProductScraper()
    result = scraper.scrape_product_info("https://www.amazon.com/product/123")

    assert result == {"title": "Mock Product", "price": "29.99"}
