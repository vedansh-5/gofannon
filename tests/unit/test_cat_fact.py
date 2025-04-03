import pytest
import requests
from gofannon.cat_fact.catfact import CatFact

def test_cat_fact_success(mocker):
    """Test that CatFactProvider returns a valid cat fact."""
    tool = CatFact()

    # Mock API response with a valid fact
    mock_response = {"fact": "Cats sleep 70% of their lives."}
    mocker.patch("requests.get", return_value=mocker.Mock(json=lambda: mock_response, status_code=200))

    result = tool.fn()

    assert isinstance(result, dict)
    assert "fact" in result
    assert isinstance(result["fact"], str)
    assert len(result["fact"]) > 0

def test_cat_fact_api_failure(mocker):
    """Test how CatFactProvider handles API failure (non-200 status code)."""
    tool = CatFact()

    # Mock API failure response (500 Internal Server Error)
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=500, json=lambda: {}))

    result = tool.fn()

    assert isinstance(result, dict)
    assert "error" in result
    assert isinstance(result["error"], str)
    assert "500" in result["error"]

def test_cat_fact_invalid_json(mocker):
    """Test how CatFactProvider handles a response with invalid JSON."""
    tool = CatFact()

    # Mock response with invalid JSON (raises JSONDecodeError)
    mock_mock = mocker.Mock(status_code=200)
    mock_mock.json.side_effect = requests.exceptions.JSONDecodeError("Expecting value", "", 0)
    mocker.patch("requests.get", return_value=mock_mock)

    result = tool.fn()

    assert isinstance(result, dict)
    assert "error" in result
    assert "JSONDecodeError" in result["error"]

def test_cat_fact_timeout(mocker):
    """Test how CatFactProvider handles a request timeout."""
    tool = CatFact()

    # Mock a request timeout
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    result = tool.fn()

    assert isinstance(result, dict)
    assert "error" in result
    assert "Timeout" in result["error"]

def test_cat_fact_network_error(mocker):
    """Test how CatFactProvider handles a network error (e.g., no internet)."""
    tool = CatFact()

    # Mock a network error
    mocker.patch("requests.get", side_effect=requests.exceptions.ConnectionError)

    result = tool.fn()

    assert isinstance(result, dict)
    assert "error" in result
    assert "ConnectionError" in result["error"]