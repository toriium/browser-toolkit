import asyncio

from browser_toolkit.create_browser.playwright import get_playwright_toolkit

async def test_auto_wait():
    btk = await get_playwright_toolkit()

    await btk.change_wait_time(range_time=(0, 1))

    await btk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/60")

    await  btk.change_wait_time(range_time=(5, 5))

    await btk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/61")
    assert True


if __name__ == "__main__":
    asyncio.run(test_auto_wait())
