from..base import BaseTool
from requests import get
import json
from ..config import FunctionRegistry
import logging

logger = logging.getLogger(__name__)


@FunctionRegistry.register
class ListIssues(BaseTool):
    def __init__(self, api_key=None, name="list_issues"):
        super().__init__()
        self.api_key = api_key
        self.name = name
        self.API_SERVICE = 'github'

    @property
    def definition(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "List all issues in a GitHub repository",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_url": {
                            "type": "string",
                            "description": "The URL of the repository, e.g. https://github.com/The-AI-Alliance/gofannon"
                        },
                        "state": {
                            "type": "string",
                            "enum": ["open", "closed", "all"],
                            "description": "Filter issues by state (default: open)",
                            "default": "open"
                        },
                        "labels": {
                            "type": "string",
                            "description": "Comma-separated list of label names to filter by"
                        },
                        "sort": {
                            "type": "string",
                            "enum": ["created", "updated", "comments"],
                            "description": "What to sort results by (default: created)",
                            "default": "created"
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["asc", "desc"],
                            "description": "Sort direction (default: desc)",
                            "default": "desc"
                        },
                        "since": {
                            "type": "string",
                            "description": "Only show issues updated after this date (ISO 8601 format)"
                        }
                    },
                    "required": ["repo_url"]
                }
            }
        }

    def fn(self, repo_url, state="open", labels=None, sort="created", direction="desc", since=None):
        logger.debug(f"Listing issues for repo {repo_url} with state={state}")
        # Extracting the owner and repo name from the URL
        repo_parts = repo_url.rstrip('/').split('/')
        owner = repo_parts[-2]
        repo = repo_parts[-1]

        api_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        headers = {
            'Authorization': f'token {self.api_key}',
            'Accept': 'application/vnd.github.v3+json'
        }
        params = {
            'state': state,
            'sort': sort,
            'direction': direction
        }

        if labels:
            params['labels'] = labels
        if since:
            params['since'] = since

        response = get(api_url, headers=headers, params=params)
        response.raise_for_status()

        issues = response.json()

        # Format the response
        formatted_issues = []
        for issue in issues:
            # Skip pull requests (GitHub API returns PRs as issues too)
            if 'pull_request' in issue:
                continue

            formatted_issues.append({
                "number": issue['number'],
                "title": issue['title'],
                "state": issue['state'],
                "created_at": issue['created_at'],
                "updated_at": issue['updated_at'],
                "html_url": issue['html_url'],
                "labels": [label['name'] for label in issue['labels']],
                "user": issue['user']['login']
            })

        return formatted_issues