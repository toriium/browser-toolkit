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
    browser_version = "125.0"
    options = webdriver.ChromeOptions()
    capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVideo": False,  # Will record screen
            "enableVNC": True,
        },
    }
    options.browser_version = browser_version

    extra_capabilities = {"goog:loggingPrefs": {"performance": "ALL"}}

    capabilities.update(extra_capabilities)

    [options.set_capability(name=k, value=v) for k, v in capabilities.items()]

    driver = webdriver.Remote(command_executor=WEBDRIVER_URL, options=options)

    # executable_path = get_latest_chrome_driver_path()
    # driver = webdriver.Chrome(options=options, service=Service(executable_path=executable_path))

    stk = SeleniumToolKit(driver=driver)
    return stk


if __name__ == "__main__":
    driver = get_selenium_toolkit()
