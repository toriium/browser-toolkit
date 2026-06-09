import asyncio
from browser_toolkit.create_browser.playwright import get_playwright_toolkit



async def test_element_is_present():
    btk = await get_playwright_toolkit()

    await btk.goto("https://webscraper.io/test-sites/e-commerce/allinone/product/60")
    await btk.element_is_present(selector='[class="pull-right price"]', timeout=5)

    await btk.close()

if __name__ == "__main__":
    asyncio.run(test_element_is_present())