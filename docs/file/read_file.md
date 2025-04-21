# ReadFile

The `ReadFile` tool allows you to read the contents of a specified file from the local filesystem.

## Parameters

* `file_path`: The path to the file to be read (e.g. `./data/input.txt`)

## Example Usage

```python
from gofannon.file.read_file import ReadFile

tool = ReadFile()
result = tool.fn(
    file_path="./data/input.txt"
)
print(result)
```

This will read and return the contents of the `./data/input.txt` file.
