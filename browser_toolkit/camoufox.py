from camoufox import AsyncCamoufox
from playwright.async_api import Page

from browser_toolkit.playwright import PlaywrigthTollKit


class CamoufoxTollKit(PlaywrigthTollKit):
    def __init__(self, browser: AsyncCamoufox, page: Page, *args, **kwargs):
        self.browser: AsyncCamoufox = browser
        self.page: Page = page
