# ListDirectory

The `ListDirectory` tool allows you to recursively list the contents of a directory in a tree-like format, similar to the Unix `tree` command.

## Parameters

* `directory_path`: The path of the directory to list (e.g. `./my_project`)
* `max_depth`: *(optional)* The maximum depth to recurse into subdirectories (default: `5`)

## Example Usage

```python
from gofannon.file.list_directory import ListDirectory

tool = ListDirectory()
result = tool.fn(
    directory_path="./my_project",
    max_depth=2
)
print(result)
```

This will output a tree representation of the contents of the `./my_project` directory up to 2 levels deep.

If the path does not exist or is not a directory, an error message will be returned. The tool also gracefully handles permission errors by marking inaccessible directories with `[Permission Denied]`.