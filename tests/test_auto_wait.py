from tests.get_driver import get_selenium_toolkit


def test_auto_wait():
    sk = get_selenium_toolkit()

    sk.change_wait_time(range_time=(0, 1))

    sk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/545")

    sk.change_wait_time(range_time=(5, 5))

    sk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/544")

    assert True


if __name__ == "__main__":
    test_auto_wait()
