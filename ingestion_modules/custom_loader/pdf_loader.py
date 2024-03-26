from llama_index.readers.file import pymu_pdf,unstructured
from llama_index.core import Document
from pathlib import Path

class BasePDFReader():
    # Cannot read image
    @staticmethod
    def read(file_path,merge_document=False):
        reader = pymu_pdf.PyMuPDFReader()
        documents = reader.load(file_path=file_path)
        if merge_document:
            documents = [doc.text for doc in documents]
            documents = "".join(documents)
            documents = [Document(text=documents,id_="1")]
        return documents

class UnstructureReader():
    @staticmethod
    def read(file_path):
        reader = unstructured.UnstructuredReader()
        return reader.load_data(file_path=file_path)