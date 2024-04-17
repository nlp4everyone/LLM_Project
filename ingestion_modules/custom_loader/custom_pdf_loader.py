from llama_index.readers.file import pymu_pdf,unstructured
from llama_parse.base import LlamaParse
from enum import Enum
from config.params import *
from typing import Union,List
from pathlib import Path
import os

class PDFProvider(Enum):
    PYMUPDF = 0
    UNSTRUCTURED = 1
    LLAMAPARSE = 2

class CustomPDFReader():
    def __init__(self,pdf_provider : PDFProvider = PDFProvider.PYMUPDF):
        # Define variable
        self._pdf_provider = pdf_provider

        self._reader = None
        # Get object
        # PyMuPDF Reader
        if self._pdf_provider == PDFProvider.PYMUPDF:
            self._reader = pymu_pdf.PyMuPDFReader()
        # UNSTRUCTURED Reader
        elif self._pdf_provider == PDFProvider.UNSTRUCTURED:
            self._reader = unstructured.UnstructuredReader()
        # LlamaParse Reader
        elif self._pdf_provider == PDFProvider.LLAMAPARSE:
            self._reader = LlamaParse(api_key=LLAMAPARSE_KEY)
        else:
            raise Exception(f"Service {self._pdf_provider} is not supported!")

    def load_data(self,file_path:Union[List[str],str]):
        # Check file existed
        if isinstance(file_path,str):
            if not os.path.exists(file_path):
                raise Exception("File is not existed!")
        # Return value
        return self._reader.load_data(file_path)

    async def aload_data(self,file_path:Union[List[str],str]):
        # Check file existed
        if isinstance(file_path, str):
            if not os.path.exists(file_path):
                raise Exception("File is not existed!")
        # Return value
        data = await self._reader.aload_data(file_path)
        return data

