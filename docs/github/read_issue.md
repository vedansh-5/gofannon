# Read Issue

The `ReadIssue` API reads an issue and its comments from a GitHub repository.

## Parameters
* `repo_url`: The URL of the repository, e.g. https://github.com/The-AI-Alliance/gofannon
* `issue_number`: The number of the issue to read

## Example Usage

```python  
from gofannon.github.read_issue import ReadIssue

read_issue = ReadIssue(api_key="your_api_key_here")
result = read_issue.fn("https://github.com/The-AI-Alliance/gofannon", 123)
print(result)  
```