import asyncio

from browser_toolkit.create_browser.playwright import get_playwright_toolkit



async def test_element_is_present():
    btk = await get_playwright_toolkit()

    await btk.goto("https://statusinvest.com.br/")
    await asyncio.sleep(5)

    request_data = await btk.get_requests(request_url="https://statusinvest.com.br/account/userdata")
    value = await btk.get_response_body_from_request_id(request_id=request_data[0].request_id)
    await btk.close()

    assert value


if __name__ == "__main__":
    test_element_is_present()
