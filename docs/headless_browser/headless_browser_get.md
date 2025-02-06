# HeadlessBrowserGet

The `HeadlessBrowserGet` API retrieves the rendered HTML content of a web page using a headless browser. This tool is particularly useful for pages that require JavaScript execution in order to display dynamic content.

## Parameters

- `url`: The URL of the web page to fetch.    
  *Type*: string    
  *Description*: The URL to fetch and render using a headless browser.

## Configuration

Upon initialization, the tool accepts a `provider` parameter which defines the headless browser backend to use. Currently, only `"selenium-chrome"` is supported. The API automatically sets up a Chrome webdriver in headless mode and returns the full page source with JavaScript executed.

## Example Usage

```python  
from gofannon.headless_browser.headless_browser_get import HeadlessBrowserGet  
  
# Initialize the tool with the default provider (selenium-chrome)  
browser_get = HeadlessBrowserGet()  
  
# Get the rendered HTML content of the page  
page_content = browser_get.fn("https://example.com")  
print(page_content)  
```

## Background

Dynamic web pages often require the execution of JavaScript to fully render 
content. Traditional HTTP requests (e.g., via requests.get) do not process 
JavaScript; thus, headless browsers are commonly used in such scenarios. 
HeadlessBrowserGet leverages tools from Selenium WebDriver (with chrome-options)
to fetch pages with JavaScript rendered, providing up-to-date and complete content.


You can now add these markdown documentation files to your repo under the 
docs/headless_browser folder.