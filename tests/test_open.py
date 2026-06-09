import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium_toolkit import SeleniumToolKit
from tests.get_driver import get_selenium_toolkit


def test_webdriver_is_open():
    stk = get_selenium_toolkit()

    stk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/545")

    time.sleep(2)
    stk.quit()

    assert not stk.webdriver_is_open()
