import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from selenium_toolkit import SeleniumToolKit
from tests.get_driver import get_selenium_toolkit


def test_element_is_present():
    stk = get_selenium_toolkit()

    stk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/545")
    stk.element_is_present(wait_time=5, query_selector='[class="pull-right price"]')

    stk.quit()
