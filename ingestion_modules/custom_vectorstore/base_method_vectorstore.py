from llama_index.core import VectorStoreIndex
from llama_index.core import Document
from typing import List
from llama_index.core import StorageContext
from system_component.system_logging import Logger

class BaseMethodVectorStore():
    def __init__(self):
        # Set vector store
        self._vector_store = None

    def get_vector_store(self):
        # Return vector store
        return self._vector_store

    def build_index_from_docs(self, documents: List[Document], embedding_model):
        # Check service
        if self._vector_store == None:
            Logger.exception("Please set vector store")
            raise Exception("Please set vector store")

        # Check input
        assert isinstance(documents, list), "Please insert list of documents"
        assert documents, "Data cannot be empty"

        # Build storage context
        storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        return VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context,
                                               embed_model=embedding_model)

    def load_index(self, embedding_model):
        # Check service
        if self._vector_store == None:
            Logger.exception("Please set vector store")
            raise Exception("Please set vector store")

        # Build storage context
        storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        return VectorStoreIndex.from_vector_store(vector_store=self._vector_store, storage_context=storage_context,
                                                  embed_model=embedding_model)