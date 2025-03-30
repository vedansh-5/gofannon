from ..base import BaseTool
from ..config import FunctionRegistry, ToolConfig
import logging
import requests

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class apod(BaseTool):
    def __init__(self, api_key=None ,name='apod'):
        super().__init__()
        self.name = name
        self.api_key = api_key or ToolConfig.get("nasa_apod_api_key")

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Get the Astronomy Picture of the Day from NASA",
                "parameters":{
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    
    def fn(self):
        logger.debug("Fetching NASA APOD data")
        if not self.api_key:
            logger.error("API key is missing. Cannot fetch APOD data.")
            return {"error": "API key is missing. Please set it in the environment or pass it as an argument."}
        url = "https://api.nasa.gov/planetary/apod"
        params = {
            "api_key": self.api_key
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return{
                "title": data.get("title"),
                "date": data.get("date"),
                "explanation": data.get("explanation"),
                "image_url": data.get("url"),
                "media_type": data.get("media_type"),
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from NASA APOD: {e}")
            return {
                "error": str(e)
            }