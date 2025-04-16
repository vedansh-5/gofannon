# CloneRepo

The `CloneRepo` tool allows you to clone a GitHub repository to a specified local directory using GitPython.

## Parameters

* `repo_url`: The URL of the GitHub repository to clone (e.g. `https://github.com/octocat/Hello-World.git`)
* `local_dir`: The local directory path where the repository should be cloned (e.g. `./cloned_repo`)

## Example Usage

```python
from gofannon.github.clone_repo import CloneRepo

tool = CloneRepo()
result = tool.fn(
    repo_url="https://github.com/octocat/Hello-World.git",
    local_dir="./cloned_repo"
)
print(result)
```

This will clone the specified GitHub repository into the `./cloned_repo` directory.