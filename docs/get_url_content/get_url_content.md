# `get_url_content` Tool

## Description

`get_url_content` is a simple web scraping tool that makes an HTTP GET request to retrieve the raw text or HTML content of a provided URL. This tool **does not execute JavaScript** and is suitable for scraping static content.

## Location

* **File:** `gofannon/web_tools/get_url_content.py`
* **Test:** `tests/unit/testing/test_get_url_content.py`

## Class

```python
GetUrlContent(name="get_url_content")
```

## Method

```python
def fn(self, url: str) -> str
```

## Parameters

| Name  | Type  | Description                                                                               |
| ----- | ----- | ----------------------------------------------------------------------------------------- |
| `url` | `str` | The URL to fetch content from. Must be a full valid URL, e.g., `https://www.example.com`. |

## Returns

* **Success:** Returns the plain text or HTML content as a string.
* **Failure:** Returns a descriptive error string, e.g., `"Error: Connection error occurred - ..."`.

## Dependencies

* `requests`

## Example Usage

```python
from gofannon.web_tools.get_url_content import GetUrlContent

tool = GetUrlContent()
result = tool.fn("https://example.com")
print(result)
```

## Example URL

* [https://example.com](https://example.com)

## Use Cases

* Scraping static HTML pages
* Validating URL content
* Building non-JS crawlers
* Integrating with pipelines for data ingestion
