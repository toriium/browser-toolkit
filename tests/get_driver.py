from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium_toolkit import SeleniumToolKit

HOST = "localhost"
WEBDRIVER_URL = f"http://{HOST}:4444/wd/hub"


def get_latest_chrome_driver_path() -> str:
    latest_driver_path = ChromeDriverManager().install()
    return latest_driver_path


def get_selenium_toolkit() -> SeleniumToolKit:
    options = webdriver.ChromeOptions()
    capabilities = {}

    extra_capabilities = {"goog:loggingPrefs": {"performance": "ALL"}}

    capabilities.update(extra_capabilities)

    [options.set_capability(name=k, value=v) for k, v in capabilities.items()]


    executable_path = get_latest_chrome_driver_path()
    driver = webdriver.Chrome(options=options, service=Service(executable_path=executable_path))

    stk = SeleniumToolKit(driver=driver)
    return stk


if __name__ == "__main__":
    driver = get_selenium_toolkit()
