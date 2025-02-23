from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..base import BaseTool
import logging

logger = logging.getLogger(__name__)

class HeadlessBrowserBase(BaseTool):
    """
    Base class for headless browser tools.
    On initialization, the provider parameter may be one of:
    "selenium-chrome", "selenium-firefox", "lightpanda", or "remote".
    Currently, only "selenium-chrome" is supported.
    """
    def __init__(self, provider="selenium-chrome", **kwargs):
        super().__init__(**kwargs)
        self.provider = provider.lower()
        supported = ["selenium-chrome", "selenium-firefox", "lightpanda", "remote"]
        if self.provider not in supported:
            raise ValueError(f"Unsupported provider: {self.provider}. Supported providers: {supported}")

    def _get_driver(self):
        if self.provider == "selenium-chrome":
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            # Adjust the executable_path if needed or ensure the chromedriver is in PATH.
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        else:
            raise NotImplementedError(f"Provider {self.provider} is not supported in the current implementation.")

    def get_page_source(self, url):
        driver = self._get_driver()
        try:
            driver.get(url)
            # Optionally, add waits here if needed so that JavaScript can fully execute.
            page_source = driver.page_source
        finally:
            driver.quit()
        return page_source