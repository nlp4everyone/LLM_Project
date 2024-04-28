import os.path
from llama_index.core import (
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext,
    Document
)
from config import params
from typing import List
cached_folder = params.cache_folder
# Local vector store
class SimpleVectorStore():
    def __init__(self,simple_cached_dir : str = "simple_vectorstore",collection_name = "llama_index"):
        # Simple cached dir
        self.cached_path = os.path.join(cached_folder,simple_cached_dir)
        # Default index
        self.collection_name = collection_name

    def build_index_from_docs(self,documents : List[Document],embedding_model = None ):
        # Check type
        if embedding_model == None: raise Exception("Please insert embedding model")
        assert isinstance(documents,list), "Please insert list of documents"
        assert documents, "Data cannot be empty"

        # Build index
        index = VectorStoreIndex.from_documents(documents, embed_model=embedding_model,use_async=True)
        index.set_index_id(self.collection_name)
        # Save to storage
        index.storage_context.persist(self.cached_path)
        return index

    def load_index(self,embedding_model = None ):
        # Check type
        if embedding_model == None: raise Exception("Please insert embedding model")
        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir=self.cached_path)
        # load index
        return load_index_from_storage(storage_context, index_id=self.collection_name,embed_model=embedding_model)