import os

from..base import BaseTool
from ..config import FunctionRegistry
import logging

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class ReadFile(BaseTool):
    """
    A tool for reading the contents of a file from the local filesystem.

    This class provides a function that takes a file path as input and returns
    the contents of that file as a string.

    Attributes:
        file_path (str): The path to the file that should be read.
    """
    def __init__(self, name="read_file"):
        super().__init__()
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Read the contents of a specified file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to be read."
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }

    def fn(self, file_path):
        logger.debug(f"Reading file: {file_path}")
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file '{file_path}' does not exist.")

            with open(file_path, 'r') as file:
                content = file.read()

            return content
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return f"Error reading file: {e}"