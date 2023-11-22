import unittest.mock as mock
import pytest
from requests.exceptions import RequestException
from amazpy.app import App

class MockTimer:
    def __init__(self, func, interval):
        self.func = func
        self.interval = interval

    def start(self):
        if callable(self.func):
            self.func()
        else:
            print(f"Warning: {self.func} is not callable")

@pytest.fixture
def app():
    return App()

def test_scrape_success(app):
    with mock.patch.object(app, 'product_url') as mock_product_url:
        mock_product_url.get.return_value = 'mocked_url'
        with mock.patch('amazpy.app.ProductScraper') as mock_scraper:
            mock_scraper.return_value.scrape_product_info.return_value = {'title': 'Mocked Product', 'price': '10.0'}

            with mock.patch.object(app, 'update_list_box') as mock_update_list_box:
                with mock.patch('amazpy.app.threading.Timer', side_effect=MockTimer) as mock_timer:
                    app.scrape()

    mock_scraper.return_value.scrape_product_info.assert_called_with('mocked_url')
    assert mock_update_list_box.called

def test_scrape_failure(app):
    with mock.patch.object(app, 'product_url') as mock_product_url:
        mock_product_url.get.return_value = 'mocked_url'
        with mock.patch('amazpy.app.ProductScraper') as mock_scraper:
            mock_scraper.return_value.scrape_product_info.side_effect = RequestException

            with mock.patch.object(app, 'update_list_box') as mock_update_list_box:
                with mock.patch('amazpy.app.threading.Timer', side_effect=MockTimer) as mock_timer:
                    app.scrape()

    mock_scraper.return_value.scrape_product_info.assert_called_with('mocked_url')
    assert not mock_update_list_box.called

# Add this check to avoid ZeroDivisionError
def test_get_average_price_empty_list():
    app = App()
    rows = []
    average_price = app.get_average_price(rows)
    assert average_price == 0.0
