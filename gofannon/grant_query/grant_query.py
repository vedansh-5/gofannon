from ..base import BaseTool
from ..config import FunctionRegistry
import logging
import requests

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class GrantsQueryTool(BaseTool):
    """Query the EU Grants database for funding opportunities
    
    Uses the EU Search API to find grant opportunities based on a search query.
    Returns information about matching grants including title, identifier, deadline date and URL.
    """
    def __init__(self, name="grants_query"):
        super().__init__
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Search for EU grant funding opportunities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to find relevant grant opportuities"
                        },
                        "page_size": {
                            "type": "integer",
                            "description": "Number of results to return (default: 5)",
                            "default": 5
                        },
                        "page_number": {
                            "type": "integer",
                            "description": "Page number for paginated results (default: 1)",
                            "default": 1
                        }
                    },
                    "requrired": ["query"]
                }
            }
        }
    
    def fn(self, query, page_size=5, page_number=1):
        """Search for EU grants based on a query
        
        Args:
            query (str): Search term to find relevant grants
            page_size (int): Number of results to return (default: 5)
            page_number (int): Page number for paginated results (default: 1)
        
        Returns:
            dict: Dictionary containing sarch results and metadata
            
        Raises:
            ValueError: If the query is empty
            requests.RequestException: If there is an error with the API request
        """

        try:
            if not query:
                raise ValueError("Query cannot be empty")
            
            logger.debug(f"Searching for EU grants with query: {query}")

            response = requests.post(
                "https://api.tech.ec.europe.eu/search-api/prod/rest/search",
                params={
                    "apiKey": "SEDIA", 
                    "text": query, 
                    "pageSize": page_size, 
                    "pageNumber": page_number
                },
                 json={
                    "languages": ["en"],
                    "displayFields": ["title", "identifier", "deadlineDate", "url"]
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            formatted_results = []
            for item in data.get("results", []):
                title = item.get("content")
                metadata = item.get("metadata", {})
                deadline = metadata.get("deadlineDate")
                identifier = metadata.get("identifier")
                url = item.get("url")
                
                formatted_results.append({
                    "title": title,
                    "identifier": identifier,
                    "deadline": deadline,
                    "url": url
                })
            
            result = {
                "total_results": data.get("totalResults", 0),
                "page": page_number,
                "grants": formatted_results
            }
            return result
             
        except ValueError as e:
            logger.error(f"Value error in eu_grants_query: {str(e)}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed in eu_grants_query: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in eu_grants_query: {str(e)}")
            raise