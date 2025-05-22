import os 
import pytest
from gofannon.pdf_reader.pdf_reader import ReadPdf
import responses

# Test assets directory
ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")

def test_valid_pdf_extraction():
    tool = ReadPdf()
    pdf_path = os.path.join(ASSET_DIR, "sample.pdf")
    result = tool.fn(pdf_path)
    assert isinstance(result, str)
    assert "Sample PDF text" in result

def test_file_not_found():
    tool = ReadPdf()
    fake_path = os.path.join(ASSET_DIR, "nonexistetnt.pdf")
    result = tool.fn(fake_path)
    assert result.startswith("Error: File not found")

def file_extension():
    tool = ReadPdf()
    text_path = os.path.join(ASSET_DIR, "not_a_pdf.txt")
    result = tool.fn(text_path)
    assert result.startswith("Error: File") and "is not a PFD" in result

def test_definition_schema():
    tool = ReadPdf()
    definition = tool.definition
    assert isinstance(definition,dict)
    assert definition["type"] == "function"
    assert definition["function"]["name"] == "pdf_reader"
    assert "file_path" in definition["function"]["parameters"]["properties"]
                                     