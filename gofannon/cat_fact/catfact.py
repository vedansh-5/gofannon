from ..base import BaseTool
from  ..config import FunctionRegistry
import logging
import requests

logger = logging.getLogger(__name__)

"""Fetch a random fun fact about cats.

    Uses the Cat Fact API (https://catfact.ninja/fact) to retrieve a random cat fact.
    """

@FunctionRegistry.register
class CatFact(BaseTool):
    def __init__(self, name = "catfact"):
        super().__init__()
        self.name = name
    
    @property
    def definition(self):
        return{
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Fetches a random fun fact about cats.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    
    def fn(self):
        logger.debug("Fetching a random cat fact...")
        url = "https://catfact.ninja/fact"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {"fact" : data.get("fact", "No fact found")}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching cat fact: {e}")
            return {"error": str(e)}