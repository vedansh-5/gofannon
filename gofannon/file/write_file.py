from..base import BaseTool
from ..config import FunctionRegistry
import logging

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class WriteFile(BaseTool):
    def __init__(self, name="write_file"):
        super().__init__()
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Write the contents of a sting to a specified file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to be written."
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to be written to the file."
                        }
                    },
                    "required": ["file_path", "content"]
                }
            }
        }

    def fn(self, file_path, content):
        logger.debug(f"Writing file: {file_path}")
        try:
            with open(file_path, 'w') as file:
                file.write(content)

            return f"File {file_path} written successfully."
        except Exception as e:
            logger.error(f"Error writing file: {e}")
            return f"Error writing file: {e}"