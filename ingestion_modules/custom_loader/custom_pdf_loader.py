from llama_index.readers.file import pymu_pdf,unstructured
# from llama_index.core import Document
from pathlib import Path
from enum import Enum
import os

class PDFProvider(Enum):
    PYMUPDF = 0
    UNSTRUCTURED = 1
    LLAMAPARSE = 2

class CustomPDFReader():
    def __init__(self,pdf_provider : PDFProvider = PDFProvider.PYMUPDF):
        # Define variable
        self.pdf_provider = pdf_provider

        self.reader = None
        # Get object
        # PyMuPDF Reader
        if self.pdf_provider == PDFProvider.PYMUPDF:
            self.reader = pymu_pdf.PyMuPDFReader()
        # UNSTRUCTURED Reader
        elif self.pdf_provider == PDFProvider.UNSTRUCTURED:
            self.reader = unstructured.UnstructuredReader()
        # LlamaParse Reader
        elif self.pdf_provider == PDFProvider.LLAMAPARSE:
            self.reader = unstructured.UnstructuredReader()

    def load(self,file_path:str):
        # Check file existed
        if not os.path.exists(file_path):
            raise Exception("File is not existed!")
        return self.reader.load_data(Path(file_path))


