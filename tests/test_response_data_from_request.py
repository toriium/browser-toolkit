import time

from selenium.webdriver import Chrome, DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from selenium_toolkit import SeleniumToolKit
from tests.get_driver import get_selenium_toolkit


def test_element_is_present():
    stk = get_selenium_toolkit()

    stk.goto("https://statusinvest.com.br/")
    time.sleep(5)

    request_data = stk.get_requests(request_url="https://statusinvest.com.br/account/userdata")
    value = stk.get_response_body_from_request_id(request_id=request_data[0].request_id)
    stk.quit()

    assert value


if __name__ == "__main__":
    test_element_is_present()
