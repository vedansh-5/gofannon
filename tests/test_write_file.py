import pytest
from pathlib import Path
import os
from gofannon.file.write_file import WriteFile 

TEST_FILE_PATH = "test_output_file.txt"
TEST_CONTENT = "This is content written by WriteFile."

def teardown_module(module):
    # Remove the test file after tests run
    if Path(TEST_FILE_PATH).exists():
        os.remove(TEST_FILE_PATH)

def test_write_file_success():
    tool = WriteFile()
    result = tool.fn(file_path=TEST_FILE_PATH, content=TEST_CONTENT)

    assert isinstance(result, str)
    assert "written successfully" in result
    assert Path(TEST_FILE_PATH).exists()
    with open(TEST_FILE_PATH, 'r') as file:
        assert file.read() == TEST_CONTENT

def test_write_file_invalid_path():
    tool = WriteFile()
    # Attempt to write to an invalid path (e.g., a directory that shouldn't exist or isn't writable)
    invalid_path = "/invalid_dir/test.txt"
    result = tool.fn(file_path=invalid_path, content="data")

    assert isinstance(result, str)
    assert "Error writing file" in result
