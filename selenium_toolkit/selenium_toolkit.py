import json
import traceback
import time
from random import uniform
from typing import Union, Type
from dataclasses import dataclass
from http.cookies import SimpleCookie

import trio
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    InvalidSessionIdException,
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from selenium_toolkit.utils import create_locator
from enum import StrEnum
import functools


class RequestType(StrEnum):
    DOCUMENT = "Document"
    XHR = "XHR"
    IMAGE = "Image"
    SCRIPT = "Script"
    STYLESHEET = "Stylesheet"
    FONT = "Font"
    FETCH = "Fetch"
    OTHER = "Other"


@dataclass
class Redirect:
    url: str


@dataclass
class Request:
    url: str
    request_id: str
    cookies: dict
    headers: dict
    redirect: Redirect = None
    type: RequestType = None


def auto_wait(func) -> Type["Response"]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        obj_wait_time = args[0]._wait_time_range
        wait = uniform(*obj_wait_time)
        time.sleep(wait)

        return func(*args, **kwargs)

    return wrapper


class SeleniumToolKit:
    _wait_time_range = (0, 0)

    def __init__(self, driver):
        self.__driver: Union[WebDriver, ChromiumDriver] = driver

    @property
    def driver(self) -> Union[WebDriver, ChromiumDriver]:
        return self.__driver

    def change_wait_time(self, range_time: tuple = (0, 0)):
        first, last = range_time

        if not (first >= 0 and last >= first):
            raise ValueError(f"range_time must be a tuple with positive values")

        self._wait_time_range = range_time

    @auto_wait
    def goto(self, url: str) -> None:
        self.__driver.get(url=url)

    def query_selector(self, query_selector: str, web_element: WebElement = None) -> Union[WebElement, None]:
        """
        :param query_selector: css or xpath
        :param web_element:  If None is passed will perform the query selector in the whole page
        """
        if not query_selector:
            raise ValueError("You need send a query_selector")

        target = web_element if web_element else self.__driver

        if query_selector[0] == "/":
            web_element = target.find_element(By.XPATH, query_selector)
        else:
            web_element = target.find_element(By.CSS_SELECTOR, query_selector)

        return web_element

    def query_selector_all(self, query_selector: str, web_element: WebElement = None) -> Union[list[WebElement], None]:
        """
        :param query_selector: css or xpath
        :param web_element:  If None is passed will perform the query selector in the whole page
        """
        if not query_selector:
            raise ValueError("You need send a query_selector")

        target = web_element if web_element else self.__driver

        if query_selector[0] == "/":
            web_elements = target.find_elements(By.XPATH, query_selector)
        else:
            web_elements = target.find_elements(By.CSS_SELECTOR, query_selector)

        return web_elements

    def find_element_by_text(self, text: str):
        query_selector = f"//*[contains(text(), '{text}' )]"
        web_element = self.query_selector(query_selector=query_selector)
        return web_element

    def find_elements_by_text(self, text: str):
        query_selector = f"//*[contains(text(), '{text}' )]"
        web_element = self.query_selector_all(query_selector=query_selector)
        return web_element

    def find_element_by_tag_and_text(self, tag: str, text: str):
        query_selector = f"//{tag}[contains(text(), '{text}' )]"
        web_elements = self.query_selector(query_selector=query_selector)
        return web_elements

    def find_elements_by_tag_and_text(self, tag: str, text: str):
        query_selector = f"//{tag}[contains(text(), '{text}' )]"
        web_elements = self.query_selector_all(query_selector=query_selector)
        return web_elements

    def get_text(self, query_selector: str) -> str:
        try:
            return self.query_selector(query_selector=query_selector).text
        except NoSuchElementException as e:
            raise e

    def get_attribute(self, query_selector: str, attribute: str) -> str:
        try:
            return self.query_selector(query_selector=query_selector).get_attribute(attribute)
        except NoSuchElementException as e:
            raise e

    @auto_wait
    def click(self, query_selector: str) -> None:
        self.query_selector(query_selector=query_selector).click()

    @auto_wait
    def fill(self, text: str, query_selector: str) -> None:
        element = self.query_selector(query_selector=query_selector)
        element.send_keys(text)

    @auto_wait
    def clear(self, query_selector: str) -> None:
        self.query_selector(query_selector=query_selector).clear()

    def fill_in_random_time(self, text: str, query_selector: str) -> None:
        element = self.query_selector(query_selector=query_selector)
        for letter in text:
            time.sleep(uniform(0.3, 0.8))
            element.send_keys(letter)

    def clear_and_fill(self, text: str, query_selector: str, random_time=False) -> None:
        self.clear(query_selector=query_selector)
        if random_time:
            self.fill_in_random_time(text=text, query_selector=query_selector)
        else:
            self.fill(text=text, query_selector=query_selector)

    def element_is_present(self, wait_time: int, query_selector: str) -> bool:
        try:
            WebDriverWait(self.__driver, wait_time).until(
                EC.presence_of_element_located(create_locator(query_selector))
            )
            return True
        except TimeoutException:
            return False

    def element_is_visible(self, wait_time: int, query_selector: str) -> bool:
        try:
            WebDriverWait(self.__driver, wait_time).until(
                EC.visibility_of_element_located(create_locator(query_selector))
            )
            return True
        except TimeoutException:
            return False

    def element_is_invisible(self, wait_time: int, query_selector: str) -> bool:
        try:
            WebDriverWait(self.__driver, wait_time).until(
                EC.invisibility_of_element_located(create_locator(query_selector))
            )
            return True
        except TimeoutException:
            return False

    def element_is_clickable(self, wait_time: int, query_selector: str) -> bool:
        try:
            WebDriverWait(self.__driver, wait_time).until(EC.element_to_be_clickable(create_locator(query_selector)))
            return True
        except TimeoutException:
            return False

    def text_is_present(self, wait_time: int, query_selector: str, text: str) -> bool:
        try:
            WebDriverWait(self.__driver, wait_time).until(
                EC.text_to_be_present_in_element(create_locator(query_selector), text_=text)
            )
            return True
        except TimeoutException:
            return False

    def alert_is_present(self, wait_time: int, message: str) -> bool:
        try:
            WebDriverWait(self.__driver, wait_time).until(EC.alert_is_present(), message=message)
            return True
        except TimeoutException:
            return False

    def page_is_loading(self) -> bool:
        if self.__driver.execute_script("return document.readyState") != "complete":
            return True
        else:
            return False

    def block_urls(self, urls: list) -> None:
        if not isinstance(self.__driver, ChromiumDriver):
            TypeError("Your driver must be a ChromiumDriver type to use this method")

        self.execute_cdp_cmd("Network.setBlockedURLs", {"urls": urls})
        self.execute_cdp_cmd("Network.enable", {})

    def driver_hard_refresh(self) -> None:
        self.__driver.execute_script("location.reload(true)")

    def webdriver_is_open(self) -> bool:
        try:
            self.__driver.execute_script("console.log('ola eu estou funcionando');")
            return True
        except InvalidSessionIdException:
            return False

    def get_all_requests(self) -> list[dict]:
        """
        !!! ALERT !!!
        For this method works the code below is necessary in the driver's creation

        # selenium < 4.0
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        driver = webdriver.Chrome(desired_capabilities=capabilities

        # selenium > 4.0
        capabilities = {"performance": "ALL"}
        options.set_capability("goog:loggingPrefs", capabilities)
        """

        if not isinstance(self.__driver, ChromiumDriver):
            TypeError("Your driver must be a ChromiumDriver type to use this method")

        logs_raw = self.__driver.get_log("performance")
        parsed_logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
        return parsed_logs

    def get_requests(self, request_url: str) -> list[Request] | None:
        parsed_logs = self.get_all_requests()
        methods = [
            "Network.responseReceived",
            "Network.requestWillBeSent",
            "Network.requestWillBeSentExtraInfo",
            # "Page.windowOpen"  # I Only see in Redirect, maybe add in the future, does not have request_id
        ]
        received_response_list = [response for response in parsed_logs if response["method"] in methods]

        resp_url = None
        matched_requests_id = set()
        for response in received_response_list:
            urls_to_match = []
            params = response["params"]
            target_request_id = params.get("requestId")
            if params.get("request"):
                urls_to_match.append(params["request"]["url"])
            if params.get("response"):
                urls_to_match.append(params["response"]["url"])
            if params.get("redirectResponse"):
                urls_to_match.append(params["redirectResponse"]["url"])

            for url in urls_to_match:
                if request_url in url:
                    matched_requests_id.add(target_request_id)

        if not matched_requests_id:
            return None

        matched_requests = []
        for target_request_id in matched_requests_id:
            cookies = dict()
            headers = dict()
            url: str = None
            redirect = None
            request_type: RequestType = None
            for response in received_response_list:
                params = response["params"]
                request_id = params.get("requestId")
                method = response.get("method")

                if target_request_id == request_id:
                    if method == "Network.requestWillBeSentExtraInfo":
                        headers = params.get("headers")

                        cookies_string = headers.get("cookie")
                        if not cookies_string:
                            continue

                        cookie_parser = SimpleCookie()
                        cookie_parser.load(cookies_string)
                        cookies = dict(cookie_parser)

                    if method == "Network.requestWillBeSent":
                        url = params["request"]["url"]
                        request_type = RequestType(params["type"])

                        if params.get("redirectResponse"):
                            redirect_url = params["redirectResponse"]["url"]
                            if request_url in redirect_url:
                                redirect = Redirect(url=redirect_url)

            request_data = Request(
                url=url,
                request_id=target_request_id,
                cookies=cookies,
                headers=headers,
                redirect=redirect,
                type=request_type,
            )
            matched_requests.append(request_data)

        return matched_requests

    def response_data_from_request(self, request_url: str, request_id: str = None) -> str | None:
        if request_id:
            response_body = self.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            return response_body

        received_requests = self.get_requests(request_url=request_url)
        if not received_requests:
            return None

        if len(received_requests) > 1:
            raise ValueError("more than one request matched")

        return self.get_response_body_from_request_id(request_id=received_requests[0].request_id)

    def get_response_body_from_request_id(self, request_id: str = None) -> str | None:
        try:
            response_body = self.execute_cdp_cmd(cmd="Network.getResponseBody", cmd_args={"requestId": request_id})
        except WebDriverException:
            return None

        return response_body

    # def execute_cdp_cmd(self, cmd: str, cmd_args: dict) -> str:
    #     execute_command = {'method': cmd, 'params': cmd_args}
    #     async def execute_cdp_async():
    #         async with self.__driver.bidi_connection() as session:
    #             cdp_session = session.session
    #             return await cdp_session.execute(execute_command)
    #
    #     return trio.run(execute_cdp_async)

    def execute_cdp_cmd(self, cmd: str, cmd_args: dict) -> str:
        """
        Useful for when executing CDP command in a remote driver
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % self.__driver.session_id
        url = self.__driver.command_executor._url + resource
        body = json.dumps({"cmd": cmd, "params": cmd_args})
        response = self.__driver.command_executor._request("POST", url, body)
        return response.get("value")

    def scroll_window(self, query_selector: str = None, web_element: WebElement = None) -> None:
        """
        Scrolls window to element position
        """
        assert query_selector or web_element, "You need to provide query_selector or web_element"

        if web_element is None:
            web_element = self.query_selector(query_selector=query_selector)

        js_code = "arguments[0].scrollIntoView();"
        self.__driver.execute_script(js_code, web_element)

    def get_all_local_storage(
        self,
    ) -> dict:
        return self.__driver.execute_script(f"return window.localStorage")

    def quit(self):
        if self.webdriver_is_open():
            self.__driver.quit()
            return
