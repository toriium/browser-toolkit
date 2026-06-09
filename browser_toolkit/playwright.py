from typing import Self

from playwright._impl._api_structures import SetCookieParam
from playwright.async_api import Page, Browser, TimeoutError, ElementHandle, Cookie as PlaywrightCookie

from browser_toolkit.base_toolkit import BaseBrowserToolkit, BaseWebElement
from browser_toolkit.types import Cookie
from browser_toolkit.utils import raise_not_implemented


class PlaywrightWebElement(BaseWebElement):
    def __init__(self, web_element: ElementHandle):
        self.web_element = web_element

    async def click(self, selector: str, delay: int = 0) -> None:
        """
        Clicks the element

        :param selector: string - CSS selector or XPath
        :param delay: int - time to keep the mouse button pressed in seconds (default: 0)
        :return:
        """
        await self.web_element.click(delay=delay)

    async def click_js(self) -> None:
        """
        Clicks the element using JavaScript

        :return:
        """
        await self.web_element.evaluate("element => element.click()")

    async def type(self, text: str, interval: float | int, clear_before: bool) -> None:
        """
        Fills the element with the text

        :param text: string - text to fill
        :param interval: float or int - time to wait between each character in seconds
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        if clear_before:
            await self.clear()
        await self.web_element.type(text, delay=interval * 1000)

    async def clear(self) -> None:
        """
        Clears the element

        :return:
        """
        await self.web_element.fill("")

    async def selector(self, selector: str) -> Self | None:
        """
        Queries the web_element and returns the first element matching the selector.
        :param selector:
        :return:
        """
        element = await self.web_element.query_selector(selector=selector)
        if element:
            return PlaywrightWebElement(web_element=element)
        return None

    async def selector_all(self, selector: str) -> list[Self]:
        """
        Queries the web_element and returns all elements matching the selector.
        :param selector:
        :return:
        """
        elements = await self.web_element.query_selector_all(selector=selector)
        return [PlaywrightWebElement(web_element=element) for element in elements]


class PlaywrightTollKit(BaseBrowserToolkit):
    def __init__(self, browser: Browser, page: Page, *args, **kwargs):
        self.browser: Browser = browser
        self.page: Page = page

    # --------------------------- START session management ---------------------------

    async def close(self) -> None:
        """
        Closes the browser tab
        :return:
        """
        await self.page.close()

    # --------------------------- END session management ---------------------------

    # --------------------------- START selectors ---------------------------

    async def selector(self, selector: str, web_element: BaseWebElement | None = None) -> BaseWebElement | None:
        """
        Queries the page and returns the first element matching the selector.
        If a web_element is provided, it queries within that element instead of the whole page.
        :param selector:
        :param web_element:
        :return:
        """
        element = await self.page.query_selector(selector=selector)
        if element:
            return PlaywrightWebElement(web_element=element)
        return None

    async def selector_all(self, selector: str, web_element: BaseWebElement | None = None) -> list[BaseWebElement]:
        """
        Queries the page and returns all elements matching the selector.
        If a web_element is provided, it queries within that element instead of the whole page.
        :param selector:
        :param web_element:
        :return:
        """
        elements = await self.page.query_selector_all(selector=selector)
        return [PlaywrightWebElement(web_element=element) for element in elements]

    # --------------------------- END selectors ---------------------------

    # --------------------------- START Actions ---------------------------

    async def goto(self, url: str, timeout: int = 30) -> None:
        """
        Navigates to URL

        :param url: url to navigate to
        :param timeout: maximum time to wait for the page to load in seconds
        :return:
        """
        await self.page.goto(url=url, timeout=timeout * 1000)

    async def click(self, selector: str, delay: int = 0) -> None:
        """
        Clicks the element matching the selector

        :param selector: string - CSS selector or XPath
        :param delay: int - time to keep the mouse button pressed in seconds (default: 0)
        :return:
        """
        await self.page.locator(selector=selector).click(delay=delay)

    async def click_js(self, selector: str) -> None:
        """
        Clicks the element matching the selector using JavaScript

        :param selector: string - CSS selector or XPath
        :return:
        """
        command = f"document.querySelector('{selector}').click()"
        await self.page.evaluate(expression=command)

    async def type(self, text: str, selector: str, interval: float | int, clear_before: bool) -> None:
        """
        Fills the element matching the selector with the text

        :param text: string - text to fill
        :param selector: string - CSS selector or XPath
        :param interval: float or int - time to wait between each character
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        if clear_before:
            await self.clear(selector=selector)
        await self.page.locator(selector=selector).type(text, delay=interval * 1000)

    async def clear(self, selector: str) -> None:
        """
        Clears the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        await self.page.locator(selector).fill("")

    async def scroll_to_element(self, selector: str) -> None:
        """
        Scrolls to the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        command = f"document.querySelector('{selector}').scrollIntoView()"
        await self.page.evaluate(expression=command)

    async def scroll_to_top(self) -> None:
        """
        Scrolls to the top of the page

        :return:
        """
        await self.page.evaluate("window.scrollTo(0, 0);")

    async def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of the page

        :return:
        """
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

    async def reload(self) -> None:
        """
        Reloads the page

        :return:
        """
        await self.page.reload()

    async def hard_reload(self) -> None:
        """
        Hard reloads the page (ignoring cache)

        :return:
        """
        cmd = "window.location.reload()"
        await self.page.evaluate(expression=cmd)

    # --------------------------- END Actions ---------------------------

    # --------------------------- START page data ---------------------------
    @property
    async def current_url(self) -> str:
        """
        Gets the current URL

        :return: str - current URL
        """
        return self.page.url

    @property
    async def title(self) -> str:
        """
        Gets the page title

        :return: str - page title
        """
        return await self.page.title()

    @property
    async def page_source(self) -> str:
        """
        Gets the page source

        :return: str - page source
        """
        return await self.page.content()

    async def get_text(self, selector: str) -> str:
        """
        Gets the text from the element matching the selector

        :param selector: string - CSS selector or XPath
        :return: str - text of the element
        """
        return await self.page.locator(selector=selector).text_content()

    async def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Gets the attribute from the element matching the selector

        :param selector: string - CSS selector or XPath
        :param attribute: string - attribute name
        :return: str - attribute of the element
        """
        return await self.page.locator(selector=selector).get_attribute(name=attribute)

    async def save_screenshot(self, file_path: str) -> None:
        """
        Takes a screenshot of the current page and saves it to the exception directory if it is set
        :param file_path:
        :return:
        """
        await self.page.screenshot(path=file_path)

    # --------------------------- END page data ---------------------------

    # --------------------------- START network ---------------------------

    async def get_network_requests(self) -> list[dict]:
        """
        Get all network Requests
        :return:
        """
        raise_not_implemented()

    async def get_network_response_body(self, request_id: str) -> str:
        """
        Gets the response body of the network request with the given request ID

        :param request_id: string - network request ID
        :return: str - response body of the network request
        """
        raise_not_implemented()

    # --------------------------- END network ---------------------------

    # --------------------------- START scripts ---------------------------
    async def execute_script(self, script: str) -> any:
        """
        Executes the JavaScript script in the context of the current page

        :param script: string - JavaScript code to execute
        :return:
        """
        return await self.page.evaluate(expression=script)

    async def execute_cdp_cmd(self, cmd: str, params: dict) -> any:
        """
        Executes the Chrome DevTools Protocol command in the context of the current page

        :param cmd: string - CDP command to execute
        :param params: dict - parameters for the CDP command
        :return:
        """
        raise_not_implemented()

    # --------------------------- END scripts ---------------------------

    # --------------------------- START wait ---------------------------
    async def element_is_present(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is present

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is present
        """
        try:
            await self.page.wait_for_selector(selector=selector, timeout=timeout * 1000, state="attached")
            return True
        except TimeoutError:
            return False

    async def element_is_visible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is visible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is visible
        """
        try:
            await self.page.wait_for_selector(selector=selector, timeout=timeout * 1000, state="visible")
            return True
        except TimeoutError:
            return False

    async def element_is_invisible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is invisible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is invisible
        """
        try:
            await self.page.wait_for_selector(selector=selector, timeout=timeout * 1000, state="hidden")
            return True
        except TimeoutError:
            return False

    async def element_is_clickable(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is clickable

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is clickable
        """
        try:
            await self.page.locator(selector=selector).click(trial=True)
            return True
        except:
            return False

    async def text_is_present(self, text: str, selector: str, timeout: int) -> bool:
        """
        Checks if the text is present in the element matching the selector

        :param text: string - text to check
        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the text is present in the element
        """
        try:
            await self.page.wait_for_selector(selector=selector, timeout=timeout * 1000, state="visible")
            element_text = await self.page.locator(selector=selector).text_content()
            return text in element_text
        except TimeoutError:
            return False

    async def alert_is_present(self, timeout: int, message: str) -> bool:
        """
        Checks if an alert is present

        :param timeout: int - seconds to wait for the alert
        :param message: str - alert message
        :return: bool - whether an alert is present
        """
        try:
            await self.page.wait_for_event("dialog", timeout=timeout * 1000)
            return True
        except TimeoutError:
            return False

    async def page_is_loading(self, timeout: int) -> bool:
        """
        Checks if the page is ready

        :param timeout: int - seconds to wait for the page to be ready
        :return: bool - whether the page is ready
        """
        try:
            await self.page.wait_for_load_state(state="load", timeout=timeout * 1000)
            return False
        except TimeoutError:
            return True

    # --------------------------- END wait ---------------------------

    # --------------------------- START session data ---------------------------
    async def get_all_cookies(self) -> list[Cookie]:
        """
        Gets all cookies
        :return: dict
        """
        raw_cookies: list[PlaywrightCookie] = await self.page.context.cookies()
        transformed_cookies: list[Cookie] = []
        for raw_cookie in raw_cookies:
            transformed_cookie = Cookie(
                name=raw_cookie.get("name"),
                value=raw_cookie.get("value"),
                url=raw_cookie.get("url"),
                domain=raw_cookie.get("domain"),
                path=raw_cookie.get("path"),
                expires=raw_cookie.get("expires"),
                httpOnly=raw_cookie.get("httpOnly"),
                secure=raw_cookie.get("secure"),
                sameSite=raw_cookie.get("sameSite"),
                partitionKey=raw_cookie.get("partitionKey"),
            )
            transformed_cookies.append(transformed_cookie)

        return transformed_cookies

    async def add_cookie(self, cookie: Cookie) -> None:
        """
        Adds a cookie to the current session

        :param cookie: Cookie - cookie to add
        :return:
        """
        transformed_cookie: SetCookieParam = SetCookieParam(
            name=cookie.name,
            value=cookie.value,
            url=cookie.url,
            domain=cookie.domain,
            path=cookie.path,
            expires=cookie.expires,
            httpOnly=cookie.httpOnly,
            secure=cookie.secure,
            sameSite=cookie.sameSite,
            partitionKey=cookie.partitionKey,
        )
        await self.page.context.add_cookies(cookies=[transformed_cookie])

    async def delete_all_cookies(self) -> None:
        """
        Deletes all cookies from the current session
        :return:
        """
        await self.page.context.clear_cookies()

    async def delete_cookie_by_name(self, name: str) -> None:
        """
        Deletes a cookie by name

        :param name: string - name of the cookie to delete
        :return:
        """
        await self.page.context.clear_cookies(name=name)

    async def delete_cookie_filter(
        self, name: str | None = None, domain: str | None = None, path: str | None = None
    ) -> None:
        """
        Deletes cookies by name, domain, and path

        :param name:
        :param domain:
        :param path:
        :return:
        """
        await self.page.context.clear_cookies(name=name, domain=domain, path=path)

    async def get_all_local_storage(self) -> dict:
        """
        Gets all local storage
        :return: dict
        """
        local_storage = await self.page.evaluate("() => Object.fromEntries(Object.entries(localStorage))")
        if not isinstance(local_storage, dict):
            local_storage = {}
        return local_storage

    # --------------------------- END session data ---------------------------
