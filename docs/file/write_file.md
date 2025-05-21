# WriteFile

The `WriteFile` tool allows you to write a string of content to a specified file on the local filesystem.

## Parameters

* `file_path`: The path to the file to be written (e.g. `./output.txt`)
* `content`: The string content to write into the file (e.g. `"Hello, world!"`)

## Example Usage

```python
from gofannon.file.write_file import WriteFile

tool = WriteFile()
result = tool.fn(
    file_path="./output.txt",
    content="Hello, world!"
)
print(result)
```

This will create or overwrite the `./output.txt` file with the provided content.