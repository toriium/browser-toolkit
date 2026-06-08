# browser-toolkit

Browser Toolkit that provides a single inteface to interact with different browser automations.


Supported automations include:
- Selenium
- Playwright
- Camoufox (Via Playwright implementation)
- Pydoll

Features that currently browser-toolkit can offer:

- **Async First**
- **More legible automation code**
- **Abstractions of browsers methods**
- **Helpful tools to use when interacting with browsers**



## Install
```
# Pip
pip install browser-toolkit

# Uv
uv add browser-toolkit

# Poetry
poetry add browser-toolkit
```

## Basic
```python
from playwright.async_api import async_playwright
from browser_toolkit.playwright import PlaywrightTollKit
import asyncio

async def main():
    # Create an instance
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Pass instance to BrowserToolKit
        btk = PlaywrightTollKit(browser=browser, page=page)
        
        # Navigate to a website
        await btk.goto('https://www.example.com')
        
        # Create a selector
        se_class = '.class1'
        
        # Use BrowserToolKit to find a web element
        web_element = await btk.selector(selector=se_class)
    
        # With returned web_element use click() method
        await web_element.click()
        
        # Or you can click directly with BrowserToolKit
        await btk.click(selector=se_class)
        
        # close instance with BrowserToolKit
        await btk.close()

if __name__ == "__main__":
    asyncio.run(main())
```