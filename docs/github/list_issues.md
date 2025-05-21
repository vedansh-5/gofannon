# ListIssues Tool

The `ListIssues` tool allows you to list issues from a GitHub repository with flexible filtering and sorting options.

## Parameters

* `repo_url`: The URL of the GitHub repository (e.g. `https://github.com/The-AI-Alliance/gofannon`)
* `state`: *(optional)* The state of issues to return (`open`, `closed`, or `all`). Default is `open`.
* `labels`: *(optional)* A comma-separated list of label names to filter by.
* `sort`: *(optional)* The field to sort by (`created`, `updated`, or `comments`). Default is `created`.
* `direction`: *(optional)* The direction of sorting (`asc` or `desc`). Default is `desc`.
* `since`: *(optional)* Only return issues updated after this date (in ISO 8601 format).

## Example Usage

```python
from gofannon.github.list_issues import ListIssues

tool = ListIssues(api_key="your_github_token")
result = tool.fn(
    repo_url="https://github.com/The-AI-Alliance/gofannon",
    state="open",
    labels="bug,enhancement",
    sort="updated",
    direction="asc"
)

for issue in result:
    print(issue["title"], issue["html_url"])
```

This will return a list of open issues in the specified repository that are labeled with "bug" or "enhancement", sorted by the most recently updated.

Pull requests are automatically excluded from the results.

If the repository cannot be accessed or the request fails, an exception will be raised.
