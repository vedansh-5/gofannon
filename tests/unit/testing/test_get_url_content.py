import pytest
import responses
from gofannon.get_url_content.get_url_content import GetUrlContent

tool = GetUrlContent()

def test_valid_url():
    url = "https://example.com"
    result = tool.fn(url)
    assert isinstance(result, str)
    assert "Example Domain" in result

def test_invalid_url():
    url = "https://nonexistent.thissitedoesnotexist12345.com"
    result = tool.fn(url)
    assert result.startswith("Error:")

def test_malformed_url():
    url = "not_a_url"
    result = tool.fn(url)
    assert result.startswith("Error:")