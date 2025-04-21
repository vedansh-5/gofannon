import pytest
from unittest.mock import patch, MagicMock
from gofannon.github.list_issues import ListIssues
from requests.exceptions import HTTPError

# Check where the requests.get is imported in the module
def test_list_issues_success():
    # Patch at the exact point where requests.get is used in your code
    with patch('gofannon.github.list_issues.get') as mock_get:
        # Create a mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "number": 1,
                "title": "Bug in authentication",
                "state": "open",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-02T00:00:00Z",
                "html_url": "https://github.com/owner/repo/issues/1",
                "labels": [{"name": "bug"}, {"name": "priority"}],
                "user": {"login": "testuser"}
            },
            {
                "number": 2,
                "title": "Feature request",
                "state": "open",
                "created_at": "2023-01-03T00:00:00Z",
                "updated_at": "2023-01-04T00:00:00Z",
                "html_url": "https://github.com/owner/repo/issues/2",
                "labels": [{"name": "enhancement"}],
                "user": {"login": "testuser2"}
            },
            {
                "number": 3,
                "title": "Pull request",
                "state": "open",
                "created_at": "2023-01-05T00:00:00Z",
                "updated_at": "2023-01-06T00:00:00Z",
                "html_url": "https://github.com/owner/repo/pull/3",
                "labels": [{"name": "enhancement"}],
                "user": {"login": "testuser3"},
                "pull_request": {"url": "https://api.github.com/repos/owner/repo/pulls/3"}  # This is a PR
            }
        ]
        # Ensure raise_for_status doesn't do anything
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Initialize with dummy API key
        tool = ListIssues(api_key="dummy_key")
        
        # Call the function
        result = tool.fn(
            repo_url="https://github.com/owner/repo",
            state="open"
        )
        
        # Verify the correct API call was made
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/issues",
            headers={
                'Authorization': 'token dummy_key',
                'Accept': 'application/vnd.github.v3+json'
            },
            params={
                'state': 'open',
                'sort': 'created',
                'direction': 'desc'
            }
        )
        
        # Check that the result is formatted correctly and PRs are filtered out
        assert len(result) == 2  # Only 2 issues, PR was filtered out
        assert result[0]["number"] == 1
        assert result[0]["title"] == "Bug in authentication"
        assert result[0]["labels"] == ["bug", "priority"]
        assert result[1]["number"] == 2
        assert "pull_request" not in result[0]
        assert "pull_request" not in result[1]

def test_list_issues_with_parameters():
    with patch('gofannon.github.list_issues.get') as mock_get:
        # Create a mock response
        mock_response = MagicMock()
        mock_response.json.return_value = []  # Empty list for simplicity
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Initialize with dummy API key
        tool = ListIssues(api_key="dummy_key")
        
        # Call the function with parameters
        result = tool.fn(
            repo_url="https://github.com/owner/repo",
            state="closed",
            labels="bug,enhancement",
            sort="updated",
            direction="asc",
            since="2023-01-01T00:00:00Z"
        )
        
        # Verify the correct API call was made with all parameters
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/owner/repo/issues",
            headers={
                'Authorization': 'token dummy_key',
                'Accept': 'application/vnd.github.v3+json'
            },
            params={
                'state': 'closed',
                'sort': 'updated',
                'direction': 'asc',
                'labels': 'bug,enhancement',
                'since': '2023-01-01T00:00:00Z'
            }
        )
        
        # Check that the result is an empty list
        assert result == []

def test_list_issues_api_error():
    with patch('gofannon.github.list_issues.get') as mock_get:
        # Create the mock and make raise_for_status throw an exception
        mock_response = MagicMock()
        http_error = HTTPError("API error")
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response
        
        # Initialize with dummy API key
        tool = ListIssues(api_key="dummy_key")
        
        # Call should raise the exception
        with pytest.raises(HTTPError) as excinfo:
            tool.fn(repo_url="https://github.com/owner/repo")
        
        # Verify the exception 
        assert excinfo.value is http_error
        assert "API error" in str(excinfo.value)