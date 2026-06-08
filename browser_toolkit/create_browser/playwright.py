from playwright.async_api import async_playwright, Browser, Page
from browser_toolkit.playwright import PlaywrightTollKit

async def get_playwright(headless: bool = False)-> tuple[Browser, Page]:
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
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://playwright.dev")
        print(await page.title())
        await browser.close()