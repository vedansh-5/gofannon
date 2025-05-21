import os

from..base import BaseTool
from ..config import FunctionRegistry
import logging

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class ListDirectory(BaseTool):
    def __init__(self, name="list_directory"):
        super().__init__()
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "List the contents of a directory recursively in a tree-like format",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory_path": {
                            "type": "string",
                            "description": "The path of the directory to list"
                        },
                        "max_depth": {
                            "type": "integer",
                            "description": "Maximum depth to recurse into (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["directory_path"]
                }
            }
        }

    def _build_tree(self, path, prefix="", depth=0, max_depth=5):
        if depth > max_depth:
            return ""

        try:
            entries = os.listdir(path)
        except PermissionError:
            return f"{prefix}[Permission Denied]\n"
        except FileNotFoundError:
            return f"{prefix}[Directory Not Found]\n"

        tree = ""
        entries.sort()
        length = len(entries)

        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            is_last = i == length - 1

            if os.path.isdir(full_path):
                tree += f"{prefix}{'└── ' if is_last else '├── '}{entry}/\n"
                tree += self._build_tree(
                    full_path,
                    prefix + ("    " if is_last else "│   "),
                    depth + 1,
                    max_depth
                )
            else:
                tree += f"{prefix}{'└── ' if is_last else '├── '}{entry}\n"

        return tree

    def fn(self, directory_path, max_depth=5):
        logger.debug(f"Listing directory: {directory_path}")

        if not os.path.exists(directory_path):
            return f"Error: Directory '{directory_path}' does not exist"

        if not os.path.isdir(directory_path):
            return f"Error: '{directory_path}' is not a directory"

        tree = self._build_tree(directory_path, max_depth=max_depth)
        return f"{directory_path}/\n{tree}"