from ..base import BaseTool
from ..config import FunctionRegistry, ToolConfig
import logging
import requests
import os
import pdfplumber
from pdfminer.pdfparser import PDFSyntaxError

logger = logging.getLogger(__name__)

"""  
    A tool for reading the text content from a PDF file.  
  
    This class provides a function that takes a file path to a PDF as input  
    and returns its text content as a string.  
    """  

@FunctionRegistry.register
class ReadPdf(BaseTool) :
    def __init__(self, name="pdf_reader"):
        super().__init__()
        self.name=name

    @property
    def definition(self):
        return{
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Read teh text content from a PDF file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The local path to the PDF file to be read."
                        }
                    },
                    "required": ["file_path"]
                }
            }
        }

    def fn(self, file_path: str) -> str :
        logger.debug(f"Reading PDF file: {file_path}")
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return f"Error: File not found at path '{file_path}'."
            if not file_path.lower().endswith(".pdf"):
                logger.error(f"File is not a PDF: {file_path}")  
                return f"Error: File '{file_path}' is not a PDF." 
            
            text_content = []
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                    else:
                        logger.debug(f"No text extracted from page {page_num+1} of {file_path}")

            if not text_content:  
                logger.warning(f"No text could be extracted from the PDF: {file_path}")  
                return "No text content could be extracted from this PDF."
            
            return "\n".join(text_content)  
        
        except PDFSyntaxError:  
            logger.error(f"Error parsing PDF (syntax error): {file_path}")  
            return f"Error: Could not parse PDF file '{file_path}'. It might be corrupted or not a valid PDF."  
        except Exception as e:  
            logger.error(f"An unexpected error occurred while reading PDF '{file_path}': {e}", exc_info=True)  
            return f"Error reading PDF file '{file_path}': {e}"  