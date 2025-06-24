import pytest
from gofannon.grant_query.grant_query import GrantsQueryTool
import requests
from unittest.mock import patch, MagicMock

@patch("requests.post")
def test_grant_query_success(mock_post):
    """Test GrantsQueryTool with a successful API response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "totalResults": 2,
        "results": [
            {
                "content": "Grant 1 Title",
                "metadata": {
                    "identifier": "GRANT1",
                    "deadlineDate": "2025-12-31"
                },
                "url": "https://example.com/grant1"
            },
            {
                "content": "Grant 2 Title",
                "metadata": {
                    "identifier": "GRANT2",
                    "deadlineDate": "2025-11-30"
                },
                "url": "https://example.com/grant2"
            }
        ]
    }
    mock_post.return_value = mock_response

    tool = GrantsQueryTool()
    result = tool.fn(query="climate", page_size=2, page_number=1)

    assert result["total_results"] == 2
    assert result["page"] == 1
    assert len(result["grants"]) == 2
    assert result["grants"][0]["title"] == "Grant 1 Title"
    assert result["grants"][0]["identifier"] == "GRANT1"
    assert result["grants"][0]["deadline"] == "2025-12-31"
    assert result["grants"][0]["url"] == "https://example.com/grant1"

def test_grant_query_empty_query():
    """Test GrantsQueryTool with an empty query."""
    tool = GrantsQueryTool()
    with pytest.raises(ValueError):
        tool.fn(query="")

@patch("requests.post")
def test_grant_query_api_error(mock_post):
    """Test GrantsQueryTool with an API error response."""
    mock_post.side_effect = requests.exceptions.RequestException("API error")
    tool = GrantsQueryTool()
    with pytest.raises(requests.exceptions.RequestException):
        tool.fn(query="ai")

@patch("requests.post")
def test_grant_query_no_results(mock_post):
    """Test GrantsQueryTool with no results."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "totalResults": 0,
        "results": []
    }
    mock_post.return_value = mock_response

    tool = GrantsQueryTool()
    result = tool.fn(query="nonexistent")
    assert result["total_results"] == 0
    assert result["grants"] == []

def test_grant_query_definition():
    """Test that the tool definition is correctly structured."""
    tool = GrantsQueryTool()
    definition = tool.definition

    assert isinstance(definition, dict)
    assert definition["type"] == "function"
    assert definition["function"]["name"] == tool.name
    assert "parameters" in definition["function"]
    assert "query" in definition["function"]["parameters"]["properties"]

