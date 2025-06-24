# EU Grants API Tools

Tools for querying the European Commission's grants database using their search API.

## Available Tools

### Grants Query

The `GrantsQueryTool` allows searching for EU grant funding opportunities using the EU Search API.

#### Usage

```python
from gofannon.eu_grants.grants_query import EUGrantsQueryTool

# Create the tool
tool = EUGrantsQueryTool()

# Search for grants
results = tool.fn(query="renewable energy")

# Print the first result
if results["grants"]:
    first_grant = results["grants"][0]
    print(f"Title: {first_grant['title']}")
    print(f"Identifier: {first_grant['identifier']}")
    print(f"Deadline: {first_grant['deadline']}")
    print(f"URL: {first_grant['url']}")
```

#### Parameters

- **query** (str): Search query to find relevant grant opportunities (required)
- **page_size** (int): Number of results to return (default: 5)
- **page_number** (int): Page number for paginated results (default: 1)

#### Return Value

The tool returns a dictionary with the following structure:

```
{
  "total_results": 42,  # Total number of results found
  "page": 1,            # Current page number
  "grants": [           # List of grant results
    {
      "title": "Grant title",
      "identifier": "GRANT-ID-123",
      "deadline": "2025-12-31",
      "url": "https://example.com/grant"
    },
    # More grant results...
  ]
}
```

#### API Information

This tool uses the public EU Search API. No authentication is required as it uses the public "SEDIA" API key.