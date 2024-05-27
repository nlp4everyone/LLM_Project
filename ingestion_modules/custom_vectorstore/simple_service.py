import os.path
from llama_index.core import (
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext,
    Document
)
from ingestion_modules.custom_vectorstore import BaseMethodVectorStore
from config import params
from typing import List,Union
from llama_index.core.schema import BaseNode
from system_component.system_logging import Logger
cached_folder = params.cache_folder

# Local vector store
class SimpleService(BaseMethodVectorStore):
    def __init__(self,simple_cached_dir : str = "simple_vectorstore",collection_name = "llama_index"):
        super().__init__()
        # Simple cached dir
        self.cached_path = os.path.join(cached_folder,simple_cached_dir)
        # Default index
        self.collection_name = collection_name

    def build_index_from_docs(
            self,
            documents : Union[List[Document],List[BaseNode]],
            embedding_model
    ):
        # Check type
        assert isinstance(documents,list), "Please insert list of documents"
        assert documents, "Data cannot be empty"

        # Build index
        index = super().build_index_from_docs(documents = documents,embedding_model = embedding_model)

        index.set_index_id(self.collection_name)
        # Save to storage
        index.storage_context.persist(self.cached_path)
        # Logging
        Logger.info(f"Saved index to : {self.cached_path}")
        return index

    def load_index(self,embedding_model):
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=self.cached_path)
        # load index
        return load_index_from_storage(storage_context, index_id=self.collection_name,embed_model=embedding_model)