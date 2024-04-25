import os.path

import chromadb
from enum import Enum
from llama_index.vector_stores.chroma import ChromaVectorStore
from typing import List
from llama_index.core import Document,StorageContext,VectorStoreIndex
from config import params

class ChromeStoringMode(Enum):
    LOCAL = 0,
    DOCKER = 1

class ChromaStoring():
    def __init__(self,storing_mode :ChromeStoringMode = ChromeStoringMode.LOCAL,collection_name : str = "chroma_collection",chroma_cache_dir : str = "chroma_vectorstore"):
        # Define params
        self.collection_name = collection_name
        self._storing_mode = storing_mode
        # Default local cache
        self.cache_dir = os.path.join(params.cache_folder,chroma_cache_dir)

        # Choose mode
        if self._storing_mode == ChromeStoringMode.LOCAL:
            self._database = chromadb.PersistentClient(path=self.cache_dir)
        else:
            self._database = chromadb.HttpClient()

        # Print
        print("Start Chroma Vectorstore !")


    def build_index_from_docs(self,documents: List[Document], embedding_model = None):
        if embedding_model is None: raise Exception("Please insert embedding model")

        # Build collection, vector store and storage context
        chroma_collection = self._database.get_or_create_collection(name=self.collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Return index
        return VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, embed_model=embedding_model
        )

    def load_index_from_docs(self,embedding_model = None):
        if embedding_model is None: raise Exception("Please insert embedding model")

        # Check if local mode or Cloud mode
        if self._storing_mode == ChromeStoringMode.LOCAL:
            database = chromadb.PersistentClient(path=self.cache_dir)
            chroma_collection = database.get_or_create_collection(self.collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            return VectorStoreIndex.from_vector_store(
                vector_store,
                embed_model=embedding_model,
            )

