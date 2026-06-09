from tests.get_driver import get_selenium_toolkit


def test_scroll_window():
    stk = get_selenium_toolkit()

    stk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/60")

    stk.scroll_window(query_selector=".copyright")

    print("waiting")
