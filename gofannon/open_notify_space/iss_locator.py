import jsonschema
import jsonschema.exceptions
from ..base import BaseTool
from ..config import FunctionRegistry

import logging

import requests
from jsonschema import validate

logger = logging.getLogger(__name__)

valid_iss_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string", "enum": ["success"]},
        "timestamp": {"type": "integer"},
        "iss_position": {
            "type": "object",
            "properties": {
                "longitude": {"type": "string"},
                "latitude": {"type": "string"},
            },
            "required": ["longitude", "latitude"],
        },
    },
    "required": ["message", "timestamp", "iss_position"],
}


@FunctionRegistry.register
class IssLocator(BaseTool):
    def __init__(self, name="iss_locator"):
        super().__init__()
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Returns the latitude / longitude of the current location of the International Space Station (ISS)",
                "parameters": {},
                "required": [],
            },
        }

    # This function will return one of two strings:
    #
    # "According to OpenNotify.org, the International Space Station can be found at (lat, long) (x,y)"
    # or
    # "The ISS endpoint returned an error. No location for the ISS can be determined"

    def fn(self):
        base_url = "http://api.open-notify.org/iss-now.json"
        logger.debug(f"Fetching ISS pos from OpenNotify.org at {base_url}")
        err_msg = "Error: The ISS endpoint returned an error. No location for the ISS can be determined"
        response = err_msg
        try:
            http_response = requests.get(base_url)
            response_json = http_response.json()
            # Validate the returned schema is valid.
            validate(response_json, valid_iss_schema)
            # Does not seem to be a way to evaluate strings as floats in a range in jsonschema,
            # other than using a REALLY ugly regex.
            lat = float(response_json["iss_position"]["latitude"])
            long = float(response_json["iss_position"]["longitude"])
            if (lat > -90 and lat < 90) and (long > -180 and long < 180):
                response = f"According to OpenNotify.org, the International Space Station can be found at (lat, long) ({lat},{long})"
            else:
                raise ValueError(f"(latitude, longitude) out of range: ({lat},{long})")
        except requests.exceptions.HTTPError as errh:
            logger.debug(f"HTTP exception: GET at {base_url} returns {errh}")
            pass
        except requests.exceptions.ConnectionError as errc:
            logger.debug(f"HTTP connection exception: GET at {base_url} returns {errc}")
            pass
        except requests.exceptions.Timeout as errt:
            logger.debug(f"HTTP timeout exception: GET at {base_url} returns {errt}")
            pass
        except requests.exceptions.RequestException as err:
            logger.debug(f"Requests exception: GET at {base_url} returns {err}")
            pass
        except jsonschema.exceptions.ValidationError as errj:
            logger.debug(
                f"JSON validation failure GET at {base_url} malformed response: {errj}"
            )
            pass
        except ValueError as errv:
            logger.debug(
                f"Value Exception GET at {base_url} malformed response: {errv}"
            )
            pass
        except Exception as erre:
            logger.debug(f"General exception GET at {base_url} Error: {erre}")
            pass

        return response
