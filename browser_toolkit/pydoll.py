from typing import Self, Any

from pydoll.protocol.network.types import CookieParam, Cookie as PydollCookie
from pydoll.browser.tab import Tab
from pydoll.browser.chromium.chrome import Chrome
from pydoll.elements.web_element import WebElement

from browser_toolkit.base_toolkit import BaseBrowserToolkit, BaseWebElement
from browser_toolkit.types import Cookie, BoundingBox
from browser_toolkit.utils import raise_not_implemented


class PydollWebElement(BaseWebElement):
    def __init__(self, web_element: WebElement):
        self.web_element = web_element

    async def get_text(self) -> str:
        """
        Gets the text from the element

        :return: str - text of the element
        """
        text = await self.web_element.text
        return text or ""

    async def get_attribute(self, attribute: str) -> str | None:
        """
        Gets the attribute from the element

        :param attribute: string - attribute name
        :return: str - attribute of the element
        """
        return self.web_element.get_attribute(name=attribute)

    async def get_position(self) -> BoundingBox:
        """
        Gets the position of the element

        :return: BoundingBox - position of the element
        """
        bounding_box = await self.web_element.bounds
        if not bounding_box:
            raise ValueError("Could not get bounding box for element")
        return BoundingBox(
            x=bounding_box["x"],
            y=bounding_box["y"],
            width=bounding_box["width"],
            height=bounding_box["height"],
        )

    async def click(self, hold_time: int = 0) -> None:
        """
        Clicks the element

        :param hold_time: int - time to keep the mouse button pressed in seconds (default: 0)
        :return:
        """
        await self.web_element.click(hold_time=hold_time, humanize=True)

    async def click_js(self) -> None:
        """
        Clicks the element using JavaScript

        :return:
        """
        await self.web_element.click_using_js()

    async def type(self, text: str, interval: float | int = 0, clear_before: bool = False) -> None:
        """
        Fills the element with the text

        :param text: string - text to fill
        :param interval: float or int - time to wait in seconds between each character
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        if clear_before:
            await self.clear()
        await self.web_element.type_text(text=text, humanize=True, interval=interval)

    async def clear(self) -> None:
        """
        Clears the element

        :return:
        """
        await self.web_element.clear()

    async def query(self, selector: str) -> Self | None:
        """
        Queries the web_element and returns the first element matching the selector.
        :param selector:
        :return:
        """
        element = await self.web_element.query(expression=selector, timeout=0, find_all=False, raise_exc=False)
        if element:
            return PydollWebElement(web_element=element)
        return None

    async def query_all(self, selector: str) -> list[Self]:
        """
        Queries the web_element and returns all elements matching the selector.
        :param selector:
        :return:
        """
        elements = await self.web_element.query(expression=selector, timeout=0, find_all=True, raise_exc=False)
        return [PydollWebElement(web_element=element) for element in elements]


class PydollTollKit(BaseBrowserToolkit):
    def __init__(self, browser: Chrome, page: Tab, *args, **kwargs):
        self.browser: Chrome = browser
        self.page: Tab = page

    # --------------------------- START session management ---------------------------

    async def close_page(self) -> None:
        """
        Closes the browser tab
        :return:
        """
        await self.page.close()

    async def close_browser(self) -> None:
        """
        Closes the browser process and all its pages
        :return:
        """
        await self.browser.close()

    # --------------------------- END session management ---------------------------

    # --------------------------- START selectors ---------------------------

    async def query(self, selector: str) -> BaseWebElement | None:
        """
        Queries the page and returns the first element matching the selector.
        :param selector:
        :return: BaseWebElement | None
        """
        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=False)
        if element:
            return PydollWebElement(web_element=element)
        return None

    async def query_all(self, selector: str) -> list[BaseWebElement]:
        """
        Queries the page and returns all elements matching the selector.
        :param selector: str
        :return: list[BaseWebElement]
        """
        elements = await self.page.query(expression=selector, timeout=0, find_all=True, raise_exc=False)
        return [PydollWebElement(web_element=element) for element in elements]

    # --------------------------- END selectors ---------------------------

    # --------------------------- START Actions ---------------------------

    async def goto(self, url: str, timeout: int = 30) -> None:
        """
        Navigates to URL

        :param url: url to navigate to
        :param timeout: maximum time to wait for the page to load in seconds
        :return:
        """
        await self.page.go_to(url=url, timeout=timeout)

    async def click(self, selector: str, hold_time: int = 0) -> None:
        """
        Clicks the element matching the selector

        :param selector: string - CSS selector or XPath
        :param hold_time: int - time to keep the mouse button pressed in seconds (default: 0)
        :return:
        """
        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=True)
        await element.click(hold_time=hold_time, humanize=True)

    async def click_js(self, selector: str) -> None:
        """
        Clicks the element matching the selector using JavaScript

        :param selector: string - CSS selector or XPath
        :return:
        """
        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=True)
        await element.click_using_js()

    async def type(self, text: str, selector: str, interval: float | int = 0, clear_before: bool = False) -> None:
        """
        Fills the element matching the selector with the text

        :param text: string - text to fill
        :param selector: string - CSS selector or XPath
        :param interval: float or int - time to wait in seconds between each character
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        if clear_before:
            await self.clear(selector=selector)

        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=True)
        await element.type_text(text=text, humanize=True, interval=interval)

    async def clear(self, selector: str) -> None:
        """
        Clears the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=True)
        await element.clear()

    async def scroll_to_element(self, selector: str) -> None:
        """
        Scrolls to the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        command = f"document.querySelector('{selector}').scrollIntoView()"
        await self.execute_script(script=command)

    async def scroll_to_top(self) -> None:
        """
        Scrolls to the top of the page

        :return:
        """
        cmd = "window.scrollTo(0, 0)"
        await self.execute_script(script=cmd)

    async def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of the page

        :return:
        """
        cmd = "window.scrollTo(0, document.body.scrollHeight);"
        await self.execute_script(script=cmd)

    async def reload(self) -> None:
        """
        Reloads the page

        :return:
        """
        await self.page.refresh(ignore_cache=False)

    async def hard_reload(self) -> None:
        """
        Hard reloads the page (ignoring cache)

        :return:
        """
        await self.page.refresh(ignore_cache=True)


    # --------------------------- END Actions ---------------------------

    # --------------------------- START page data ---------------------------
    @property
    async def current_url(self) -> str:
        """
        Gets the current URL

        :return: str - current URL
        """
        return await self.page.current_url

    @property
    async def title(self) -> str:
        """
        Gets the page title

        :return: str - page title
        """
        return await self.page.title

    @property
    async def page_source(self) -> str:
        """
        Gets the page source

        :return: str - page source
        """
        return await self.page.page_source

    async def get_text(self, selector: str) -> str:
        """
        Gets the text from the element matching the selector

        :param selector: string - CSS selector or XPath
        :return: str - text of the element
        """
        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=True)
        return await element.text

    async def get_attribute(self, selector: str, attribute: str) -> str | None:
        """
        Gets the attribute from the element matching the selector

        :param selector: str - CSS selector or XPath
        :param attribute: str - attribute name
        :return: str - attribute of the element
        """
        element = await self.page.query(expression=selector, timeout=0, find_all=False, raise_exc=True)
        return element.get_attribute(name=attribute)

    async def save_screenshot(self, file_path: str) -> None:
        """
        Takes a screenshot of the current page and saves it to the exception directory if it is set
        :param file_path:
        :return:
        """
        await self.page.take_screenshot(path=file_path, quality=100)

    # --------------------------- END page data ---------------------------

    # --------------------------- START network ---------------------------

    async def get_network_requests(self) -> list[dict]:
        """
        Get all network Requests
        :return:
        """
        return await self.page.get_network_logs()
        pass

    async def get_network_response_body(self, request_id: str) -> str:
        """
        Gets the response body of the network request with the given request ID

        :param request_id: string - network request ID
        :return: str - response body of the network request
        """
        return await self.page.get_network_response_body(request_id=request_id)

    # --------------------------- END network ---------------------------

    # --------------------------- START scripts ---------------------------
    async def execute_script(self, script: str) -> Any:
        """
        Executes the JavaScript script in the context of the current page

        :param script: string - JavaScript code to execute
        :return:
        """
        return await self.page.execute_script(script=script)

    async def execute_cdp_cmd(self, cmd: str, params: dict) -> Any:
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
        element = await self.page.query(expression=selector, timeout=timeout, find_all=True, raise_exc=False)
        return bool(element)

    async def element_is_visible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is visible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is visible
        """
        element = await self.page.query(expression=selector, timeout=timeout, find_all=True, raise_exc=False)
        return bool(element)

    async def element_is_invisible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is invisible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is invisible
        """
        element = await self.page.query(expression=selector, timeout=timeout, find_all=True, raise_exc=False)
        return True if element is None else False

    async def element_is_clickable(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is clickable

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is clickable
        """
        element = await self.page.query(expression=selector, timeout=timeout, find_all=False, raise_exc=False)
        if not element:
            return False
        return await element.is_visible()

    async def text_is_present(self, text: str, selector: str, timeout: int) -> bool:
        """
        Checks if the text is present in the element matching the selector

        :param text: string - text to check
        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the text is present in the element
        """
        element = await self.query(selector=selector)
        if not element:
            return False
        element_text = await element.get_text()
        return text in element_text


    async def alert_is_present(self, timeout: int, message: str) -> bool:
        """
        Checks if an alert is present

        :param timeout: int - seconds to wait for the alert
        :param message: str - alert message
        :return: bool - whether an alert is present
        """
        raise_not_implemented()

    async def page_is_loading(self, timeout: int) -> bool:
        """
        Checks if the page is ready

        :param timeout: int - seconds to wait for the page to be ready
        :return: bool - whether the page is ready
        """
        cmd = "return document.readyState"
        if self.page.execute_script(cmd) != "complete":
            return True
        else:
            return False

    # --------------------------- END wait ---------------------------

    # --------------------------- START session data ---------------------------
    async def get_all_cookies(self) -> list[Cookie]:
        """
        Gets all cookies
        :return: list[Cookie]
        """
        raw_cookies: list[PydollCookie] = await self.page.get_cookies()
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
        transformed_cookie: CookieParam = CookieParam(
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
        await self.page.set_cookies(cookies=[transformed_cookie])

    async def delete_all_cookies(self) -> None:
        """
        Deletes all cookies from the current session
        :return:
        """
        await self.page.delete_all_cookies()

    async def delete_cookie_by_name(self, name: str) -> None:
        """
        Deletes a cookie by name

        :param name: string - name of the cookie to delete
        :return:
        """
        raise_not_implemented()

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
        raise_not_implemented()

    async def get_all_local_storage(self) -> dict:
        """
        Gets all local storage
        :return: dict
        """
        cmd = "() => Object.fromEntries(Object.entries(localStorage))"
        raw = await self.page.execute_script(script=cmd, return_by_value=True)
        if not isinstance(raw, dict):
            return {}
        local_storage = raw["result"]["result"]["value"]
        return local_storage



    # --------------------------- END session data ---------------------------
