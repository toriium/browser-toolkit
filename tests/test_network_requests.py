import asyncio

from browser_toolkit.create_browser.playwright import get_playwright_toolkit


async def test_network_requests():
    btk = await get_playwright_toolkit()

    await btk.goto("https://scrapingtest.com/ecommerce/pagination")
    await asyncio.sleep(5)

    all_requests = await btk.get_network_requests()

    assert all_requests


if __name__ == "__main__":
    asyncio.run(test_network_requests())
