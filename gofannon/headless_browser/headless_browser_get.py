from .base import HeadlessBrowserBase
from ..config import FunctionRegistry
import logging

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class HeadlessBrowserGet(HeadlessBrowserBase):
    def __init__(self, provider="selenium-chrome", name="headless_browser_get"):
        super().__init__(provider=provider)
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Retrieve the contents of a web page with JavaScript rendered using a headless browser.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL of the web page to fetch"
                        }
                    },
                    "required": ["url"]
                }
            }
        }

    def fn(self, url):
        logger.debug(f"Fetching URL with headless browser using provider {self.provider}: {url}")
        return self.get_page_source(url)