import pytest
from gofannon.nasa.apod import AstronomyPhotoOfTheDayTool
import responses

@responses.activate
def test_apod_successful_response():
    """Test APOD tool with a successful API response."""
    mock_response = {
        "title": "Astronomy Picture of the Day",
        "date": "2025-04-01",
        "explanation": "This is a test explanation.",
        "url": "https://example.com/image.jpg",
        "media_type": "image",
    }
    responses.add(
        responses.GET,
        "https://api.nasa.gov/planetary/apod",
        json=mock_response,
        status=200,
    )

    tool = AstronomyPhotoOfTheDayTool(api_key="nasa_apod_api_key")
    result = tool.fn()

    assert result["title"] == "Astronomy Picture of the Day"
    assert result["date"] == "2025-04-01"
    assert result["explanation"] == "This is a test explanation for the APOD."
    assert result["url"] == "https://example.com/image.jpg"
    assert result["media_type"] == "image"

def test_apod_missing_api_key():
    "Test APOD tool when the API key is missing."""
    tool = AstronomyPhotoOfTheDayTool(api_key=None)
    result = tool.fn()

    assert "error" in result
    assert result["error"] == "API key is missing. Please set it in the environment or pass it as an argument."

@responses.activate
def test_apod_error_response():
    """Test APOD tool with an error response from th API."""
    responses.add(
        responses.GET,
        "https://api.nasa.gov/planetary/apod",
        status=500,
    )

    tool = AstronomyPhotoOfTheDayTool(api_key="test_api_key")
    result = tool.fn()

    assert "error" in result
    assert "500 Server Error" in result["error"]

@responses.activate
def test_apod_invalid_api_key():
    """Test APOD tool with an invalid API key."""
    mock_error = {
        "error": {
            "code": "API_KEY_INVALID",
            "message": "An invalid API key was supplied."
        }
    }

    responses.add(
        responses.GET,
        "https://api.nasa.gov/planetary/apod",
        json=mock_error,
        status=403,
    )

    tool = AstronomyPhotoOfTheDayTool(api_key="invalid_api_key")
    result = tool.fn()
    assert "error" in result
    assert "API_KEY_INVALID" in result["error"]

def test_definition():
    """Test that the tool definition is correctly structured."""
    tool = AstronomyPhotoOfTheDayTool(api_key="test_api_key")
    definition = tool.definition

    assert isinstance(definition, dict)
    assert definition["type"] == "function"
    assert definition["function"]["name"] == "apod"
    assert "parameters" in definition["function"]