import pytest
import shutil
from pathlib import Path
from gofannon.github.clone_repo import CloneRepo

TEST_REPO_URL = "https://github.com/octocat/Hello-World.git"
TEST_LOCAL_DIR = "test_cloned_repo"

def teardown_module(module):
    # Clean up the directory after tests run
    if Path(TEST_LOCAL_DIR).exists():
        shutil.rmtree(TEST_LOCAL_DIR)

def test_clone_repo_success():
    tool = CloneRepo()
    result = tool.fn(repo_url=TEST_REPO_URL, local_dir=TEST_LOCAL_DIR)

    assert isinstance(result, str)
    assert Path(TEST_LOCAL_DIR).exists()
    assert "Repository cloned successfully" in result

def test_clone_repo_invalid_url():
    tool = CloneRepo()
    bad_url = "https://github.com/nonexistent/repo.git"
    result = tool.fn(repo_url=bad_url, local_dir="bad_test_dir")

    assert isinstance(result, str)
    assert "Error cloning repository" in result or "Unexpected error" in result
