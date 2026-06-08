from playwright.async_api import async_playwright
from browser_toolkit.playwright import PlaywrightTollKit

async def get_playwright_toolkit() -> PlaywrightTollKit:
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    btk = PlaywrightTollKit(
        browser=browser,
        page=page,
    )
    return btk