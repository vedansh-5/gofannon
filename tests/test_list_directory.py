import pytest
import os
from pathlib import Path
import shutil

from gofannon.file.list_directory import ListDirectory

TEST_ROOT = Path("test_dir")
SUBDIR_1 = TEST_ROOT / "subdir1"
SUBDIR_2 = TEST_ROOT / "subdir2"
FILE_1 = TEST_ROOT / "file1.txt"
FILE_2 = SUBDIR_1 / "file2.txt"

def setup_module(module):
    # Create a nested directory structure for testing
    TEST_ROOT.mkdir(exist_ok=True)
    SUBDIR_1.mkdir(exist_ok=True)
    SUBDIR_2.mkdir(exist_ok=True)
    FILE_1.write_text("This is file 1.")
    FILE_2.write_text("This is file 2.")

def teardown_module(module):
    # Clean up after tests
    if TEST_ROOT.exists():
        shutil.rmtree(TEST_ROOT)

def test_list_directory_success():
    tool = ListDirectory()
    result = tool.fn(directory_path=str(TEST_ROOT))

    assert isinstance(result, str)
    assert str(TEST_ROOT) in result
    assert "file1.txt" in result
    assert "subdir1/" in result
    assert "subdir2/" in result
    assert "file2.txt" in result

def test_list_directory_max_depth_zero():
    tool = ListDirectory()
    result = tool.fn(directory_path=str(TEST_ROOT), max_depth=0)

    assert isinstance(result, str)
    assert "file1.txt" in result
    assert "subdir1/" in result
    assert "subdir2/" in result
    assert "file2.txt" not in result

def test_list_directory_nonexistent():
    tool = ListDirectory()
    result = tool.fn(directory_path="nonexistent_dir")

    assert result.startswith("Error:")
    assert "does not exist" in result

def test_list_directory_not_a_directory(tmp_path):
    file_path = tmp_path / "not_a_dir.txt"
    file_path.write_text("I am a file")

    tool = ListDirectory()
    result = tool.fn(directory_path=str(file_path))

    assert result.startswith("Error:")
    assert "is not a directory" in result

def test_list_directory_permission_denied(monkeypatch):
    tool = ListDirectory()

    def fake_listdir(path):
        raise PermissionError("Permission denied")

    monkeypatch.setattr(os, "listdir", fake_listdir)

    result = tool.fn(directory_path=str(TEST_ROOT))
    assert "[Permission Denied]" in result
