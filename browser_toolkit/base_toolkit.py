import asyncio
import functools
from abc import ABC, abstractmethod
import inspect
from random import uniform

class WebElement:
    pass


def main_decorator(func):
    @functools.wraps(func)
    async def wrapper(self: BaseToolkit, *args, **kwargs):
        sleep_time = uniform(*self._wait_time_range)
        await asyncio.sleep(sleep_time)
        try:
            return await func(self, *args, **kwargs)
        except Exception as e:
            if self._exception_directory:
                await self.save_screenshot(f'{self._exception_directory}/{func.__name__}.png')
            raise e
    return wrapper


class AutoDecorate:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for attr_name, attr_value in cls.__dict__.items():
            if inspect.iscoroutinefunction(attr_value):
                setattr(cls, attr_name, main_decorator(attr_value))


class BaseBrowserToolkit(ABC):
    _wait_time_range = (0, 0)
    _exception_directory: str | None = None

    def __init__(self, browser):
        self.browser = browser

    # --------------------------- START decorators ---------------------------
    def change_wait_time(self, range_time: tuple = (0, 0)):
        first, last = range_time

        if not (first >= 0 and last >= first):
            raise ValueError(f'range_time must be a tuple with positive values')

        self._wait_time_range = range_time

    def change_exception_directory(self, exception_directory: str):
        self._exception_directory = exception_directory

    @abstractmethod
    async def save_screenshot(self, file_path: str) -> None:
        """
        Takes a screenshot of the current page and saves it to the exception directory if it is set
        :param file_path:
        :return:
        """
        pass
    # --------------------------- END decorators ---------------------------
    async def query_selector(self, query_selector: str, web_element: WebElement | None = None) -> WebElement | None:
        """
        Queries the page and returns the first element matching the query selector.
        :param query_selector:
        :param web_element:
        :return:
        """
        pass

    async def query_selector_all(self, query_selector: str, web_element: WebElement | None = None) -> WebElement | None:
        """
        Queries the page and returns all elements matching the query selector.
        :param query_selector:
        :param web_element:
        :return:
        """
        pass

    # --------------------------- START Actions ---------------------------
    @abstractmethod
    async def goto(self, url: str) -> None:
        """
        Navigates to URL
        :param url:
        :return:
        """
        pass

    @abstractmethod
    async def click(self, selector: str) -> None:
        """
        Clicks the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        pass

    @abstractmethod
    async def click_js(self, selector: str) -> None:
        """
        Clicks the element matching the selector using JavaScript

        :param selector: string - CSS selector or XPath
        :return:
        """
        pass

    @abstractmethod
    async def type(self, text: str, selector: str, interval: float | int, clear_before: bool) -> None:
        """
        Fills the element matching the selector with the text

        :param text: string - text to fill
        :param selector: string - CSS selector or XPath
        :param interval: float or int - time to wait between each character
        :param clear_before: bool - whether to clear the field before filling
        :return:
        """
        pass

    @abstractmethod
    async def clear(self, selector: str) -> None:
        """
        Clears the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        pass

    @abstractmethod
    async def scroll_to_element(self, selector: str) -> None:
        """
        Scrolls to the element matching the selector

        :param selector: string - CSS selector or XPath
        :return:
        """
        pass

    @abstractmethod
    async def scroll_to_top(self) -> None:
        """
        Scrolls to the top of the page

        :return:
        """
        pass

    @abstractmethod
    async def scroll_to_bottom(self) -> None:
        """
        Scrolls to the bottom of the page

        :return:
        """
        pass

    @abstractmethod
    async def reload(self) -> None:
        """
        Reloads the page

        :return:
        """
        pass

    @abstractmethod
    async def hard_reload(self) -> None:
        """
        Hard reloads the page (ignoring cache)

        :return:
        """
        pass
    # --------------------------- END Actions ---------------------------

    # --------------------------- START page data ---------------------------
    @property
    @abstractmethod
    async def current_url(self) -> str:
        """
        Gets the current URL

        :return: str - current URL
        """
        pass

    @property
    @abstractmethod
    async def page_source(self) -> str:
        """
        Gets the page source

        :return: str - page source
        """
        pass

    @abstractmethod
    async def get_text(self, selector: str) -> str:
        """
        Gets the text from the element matching the selector

        :param selector: string - CSS selector or XPath
        :return: str - text of the element
        """

    @abstractmethod
    async def get_attribute(self, selector: str, attribute: str) -> str:
        """
        Gets the attribute from the element matching the selector

        :param selector: string - CSS selector or XPath
        :param attribute: string - attribute name
        :return: str - attribute of the element
        """
        pass
    # --------------------------- END page data ---------------------------

    # --------------------------- START network ---------------------------
    @abstractmethod
    async def get_network_requests(self) -> list[dict]:
        ...

    @abstractmethod
    async def get_network_response_body(self, request_id: str) -> str:
        """
        Gets the response body of the network request with the given request ID

        :param request_id: string - network request ID
        :return: str - response body of the network request
        """
        pass
    # --------------------------- END network ---------------------------


    # --------------------------- START scripts ---------------------------
    @abstractmethod
    async def execute_script(self, script: str) -> any:
        """
        Executes the JavaScript script in the context of the current page

        :param script: string - JavaScript code to execute
        :return:
        """
        pass

    @abstractmethod
    async def execute_cdp_cmd(self, cmd: str, params: dict) -> any:
        """
        Executes the Chrome DevTools Protocol command in the context of the current page

        :param cmd: string - CDP command to execute
        :param params: dict - parameters for the CDP command
        :return:
        """
        pass

    # --------------------------- END scripts ---------------------------

    # --------------------------- START wait ---------------------------
    @abstractmethod
    async def element_is_present(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is present

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is present
        """
        pass

    @abstractmethod
    async def element_is_visible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is visible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is visible
        """
        pass

    @abstractmethod
    async def element_is_invisible(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is invisible

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is invisible
        """
        pass

    @abstractmethod
    async def element_is_clickable(self, selector: str, timeout: int) -> bool:
        """
        Checks if the element matching the selector is clickable

        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the element is clickable
        """
        pass

    @abstractmethod
    async def text_is_present(self, text: str, selector: str, timeout: int) -> bool:
        """
        Checks if the text is present in the element matching the selector

        :param text: string - text to check
        :param selector: string - CSS selector or XPath
        :param timeout: int - seconds to wait for the element
        :return: bool - whether the text is present in the element
        """
        pass

    async def alert_is_present(self, timeout: int, message: str) -> bool:
        """
        Checks if an alert is present

        :param timeout: int - seconds to wait for the alert
        :param message: str - alert message
        :return: bool - whether an alert is present
        """
        pass

    @abstractmethod
    async def page_is_loading(self, timeout: int) -> bool:
        """
        Checks if the page is ready

        :param timeout: int - seconds to wait for the page to be ready
        :return: bool - whether the page is ready
        """
        pass

    # --------------------------- END wait ---------------------------

    # --------------------------- START session data ---------------------------
    @abstractmethod
    async def get_cookies(self) -> dict:
        """
        Gets all cookies
        :return: dict
        """
        pass

    @abstractmethod
    async def get_all_local_storage(self) -> dict:
        """
        Gets all local storage
        :return: dict
        """
        pass
    # --------------------------- END session data ---------------------------


    @abstractmethod
    async def close(self) -> None:
        """
        Closes the browser tab
        :return:
        """
