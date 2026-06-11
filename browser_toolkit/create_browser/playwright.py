
from playwright.async_api import async_playwright, Browser, Page
from browser_toolkit.playwright import PlaywrightTollKit


async def get_playwright(headless: bool = False) -> tuple[Browser, Page]:
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=headless)
    page = await browser.new_page()
    return browser, page


async def get_playwright_toolkit() -> PlaywrightTollKit:
    browser, page = await get_playwright()
    btk = PlaywrightTollKit(
        browser=browser,
        page=page,
    )
    return btk


async def main():
    browser_toolkit = await get_playwright_toolkit()
    await browser_toolkit.goto("https://www.google.com")
    title = await browser_toolkit.title
    await browser_toolkit.close_browser()