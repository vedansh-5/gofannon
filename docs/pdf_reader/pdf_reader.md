## pdf\_reader

The `pdf_reader` tool extracts text content from a specified PDF file located on the local filesystem.

## Function Constructor Parameters

The function takes a file path and returns the extracted text from the PDF as a string:

```
"Here is the full text content extracted from the PDF file..."
```

If the PDF has no text, is not found, or is invalid, it returns an error message:

```
"Error: File not found at path '/path/to/file.pdf'."
"Error: File '/path/to/file.txt' is not a PDF."
"No text content could be extracted from this PDF."
```

## API Parameters

| Parameter  | Type   | Description                     |
| ---------- | ------ | ------------------------------- |
| file\_path | string | The local path to the PDF file. |

## Example Usage

```python
from gofannon.tools.pdf_reader import ReadPdf

# Create an instance of the tool
reader = ReadPdf()

# Extract text from a PDF
result = reader.fn("tests/assets/sample.pdf")

# Print the extracted text
print(result)
```

## Error Handling

The tool handles common file-related issues and returns clear error messages:

* If the file does not exist or is not a PDF, it returns an error string.
* If the PDF has no extractable text, it returns a user-friendly message.
* Unexpected internal exceptions are caught and returned as error strings.
