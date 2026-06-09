from selenium.webdriver.common.by import By


def create_locator(query_selector: str) -> tuple:
    if query_selector[0] == "/":
        locator = (By.XPATH, query_selector)
    else:
        locator = (By.CSS_SELECTOR, query_selector)

    return locator
