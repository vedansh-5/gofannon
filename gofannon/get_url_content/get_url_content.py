from ..base import BaseTool
from ..config import FunctionRegistry, ToolConfig
import requests
import logging

logger = logging.getLogger(__name__)

"""Fetches the text content of a given URL.

This tool makes a simple GET request and returns the raw text content.
It does not render JavaScript or handle complex interactions."""

@FunctionRegistry.register
class GetUrlContent(BaseTool):
    def __init__(self, name="get_url_content"):
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": (
                    "Fetches the text content of a given URL. "
                    "This tool makes a simple GET request and returns the raw text content. "
                    "It does not render JavaScript or handle complex interactions."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to fetch content from (e.g., 'https://www.example.com')."
                        }
                    },
                    "required": ["url"]
                }
            }
        }
    
    def fn(self, url: str):
        logger.debug(f"Attempting to fetch content from URL: {url}")
        try:
            headers = {
                'User-Agent': (
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/91.0.4472.124 Safari/537.36'
                )
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            logger.info(f"Successfully fetched content from URL: {url}")
            return response.text
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching URL {url}: {e}")
            return f"Error: HTTP error - {e}"
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error fetching URL {url}: {e}")
            return f"Error: Connection error - {e}"
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout fetching URL {url}: {e}")
            return f"Error: Timeout - {e}"
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching URL {url}: {e}")
            return f"Error: Request error - {e}"
        except Exception as e:
            logger.error(f"Unexpected error fetching URL {url}: {e}")
            return f"Error: Unexpected error - {e}"