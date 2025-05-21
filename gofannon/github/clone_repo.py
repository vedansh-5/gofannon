import git
from pathlib import Path

from..base import BaseTool
from ..config import FunctionRegistry
import logging

logger = logging.getLogger(__name__)

@FunctionRegistry.register
class CloneRepo(BaseTool):
    """
    Clone a GitHub repository to a specified local directory.
    This tool takes a GitHub repository URL and a target local directory,
    then clones the repository into that directory using GitPython.
    Returns a success message if the operation completes successfully,
    or an error message if it fails.
    """
    def __init__(self, name="clone_github_repo"):
        super().__init__()
        self.name = name

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Clone a GitHub repository to a specified local directory.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_url": {
                            "type": "string",
                            "description": "The URL of the GitHub repository to clone."
                        },
                        "local_dir": {
                            "type": "string",
                            "description": "The local directory where the repository should be cloned."
                        }
                    },
                    "required": ["repo_url", "local_dir"]
                }
            }
        }

    def fn(self, repo_url, local_dir):
        logger.debug(f"Cloning repository {repo_url} to {local_dir}")

        # Ensure the local directory exists
        local_dir_path = Path(local_dir)
        if not local_dir_path.exists():
            local_dir_path.mkdir(parents=True, exist_ok=True)

        try:
            # Clone the repository
            repo = git.Repo.clone_from(repo_url, local_dir_path)
            return f"Repository cloned successfully to {local_dir}"
        except git.exc.GitCommandError as e:
            logger.error(f"Error cloning repository: {e}")
            return f"Error cloning repository: {e}"
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"Unexpected error: {e}"