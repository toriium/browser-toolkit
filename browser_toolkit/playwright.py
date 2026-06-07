from browser_toolkit.base_toolkit import BaseBrowserToolkit
from playwright.async_api import Page, Browser


class PlaywrigthTollKit(BaseBrowserToolkit):
    def __init__(self, browser: Browser, page: Page, *args, **kwargs):
        self.browser: Browser = browser
        self.page: Page = page
