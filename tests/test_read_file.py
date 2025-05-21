import pytest
import os
from pathlib import Path
from gofannon.file.read_file import ReadFile

TEST_FILE_PATH = "test_sample_file.txt"
TEST_CONTENT = "This is a test file for ReadFile."

def setup_module(module):
    # Create a temporary file for testing
    with open(TEST_FILE_PATH, "w") as f:
        f.write(TEST_CONTENT)

def teardown_module(module):
    # Clean up the test file
    if Path(TEST_FILE_PATH).exists():
        os.remove(TEST_FILE_PATH)

def test_read_file_success():
    tool = ReadFile()
    result = tool.fn(file_path=TEST_FILE_PATH)

    assert isinstance(result, str)
    assert result == TEST_CONTENT

def test_read_file_not_found():
    tool = ReadFile()
    result = tool.fn(file_path="non_existent_file.txt")

    assert isinstance(result, str)
    assert "Error reading file" in result
    assert "does not exist" in result
