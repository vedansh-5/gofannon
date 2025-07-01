# MCP Server with Gofannon Tools

Gofannon can be run via an MCP server; whether on its own or for Anthropic's desktop client.

The following is an example `server.py` file. You can update it to use any gofannon tool; the Addition tool is included below, but any tool can be added with the .export_to_mcp method.

```python
from mcp.server.fastmcp import FastMCP
from gofannon.basic_math.addition import Addition

# Create an MCP server
mcp = FastMCP("Gofannon Demo")

# Add an addition tool
add = Addition()
add.export_to_mcp(mcp)
```

To install for Anthropic Desktop run:

```bash
mcp install server.py
```

For additional information [see Anthropic's Documentation](https://github.com/modelcontextprotocol/python-sdk#quickstart) and their [clickable instructions](https://www.anthropic.com/engineering/desktop-extensions).

## Another example and how to set environment variables for tools
### Install packages
`pip install gofannon`

This example `server.py` file includes the Gofannon tools for Arxiv and Google searching, as well as generic URL content fetching:
```python
from mcp.server.fastmcp import FastMCP
from os import getenv
from gofannon.arxiv.get_article import GetArticle
from gofannon.arxiv.search import Search
from gofannon.get_url_content.get_url_content import GetUrlContent
from gofannon.google_search.google_search import GoogleSearch

# Create an MCP server
mcp = FastMCP("Gofannon Demo")

# Add arxiv
get_article = GetArticle()
get_article.export_to_mcp(mcp)
search = Search()
search.export_to_mcp(mcp)

# Add url content
get_url_content = GetUrlContent()
get_url_content.export_to_mcp(mcp)

# Add google search
google_search = GoogleSearch(getenv('GOOGLE_SEARCH_API_KEY'), getenv('GOOGLE_SEARCH_ENGINE_ID'))
google_search.export_to_mcp(mcp)
```
### Run the server
1. Save the above script in a file, e.g. `server.py`
2. Export environment variables with the key/ids required
    * `export GOOGLE_SEARCH_API_KEY=<your-search-api-key>`
    * `export GOOGLE_SEARCH_ENGINE_ID=<your-search-engine-id>`
3. `mcp run server.py` (for stdio transport) or `mcp run server.py -t sse` (for sse transport)

### Call the server
1. Install `cmcp` on your client host
    * `pip install cmcp`
2. Make calls
    * List tools `cmcp http://<hostname-or-IP-address>:8000/sse tools/list`
    * Use a tool `cmcp http://<hostname-or-IP-address>:8000/sse tools/call name=google_search arguments:='{"query": "mahout"}'`

## For more info
* [Python SDK for MCP](https://github.com/modelcontextprotocol/python-sdk)
* [cMCP (cURL for MCP)](https://github.com/RussellLuo/cmcp)
