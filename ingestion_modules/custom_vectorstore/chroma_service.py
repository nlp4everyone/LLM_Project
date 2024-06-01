import os.path
import chromadb
from strenum import StrEnum
from llama_index.vector_stores.chroma import ChromaVectorStore
from typing import List,Union
from llama_index.core import Document,StorageContext,VectorStoreIndex
from config import params
from llama_index.core.schema import BaseNode
from ingestion_modules.custom_vectorstore import BaseMethodVectorStore
from system_components.system_logging import Logger
# Local vector store

class ChromaMode(StrEnum):
    LOCAL = "Local",
    DOCKER = "Docker",
    Ephemeral = "Ephemeral"

class ChromaService(BaseMethodVectorStore):
    def __init__(self,storing_mode :ChromaMode = ChromaMode.LOCAL,collection_name : str = "chroma_collection",chroma_cache_dir : str = "chroma_vectorstore"):
        super().__init__()
        # Define params
        self.collection_name = collection_name
        self._storing_mode = storing_mode
        # Default local cache
        self.cache_dir = os.path.join(params.cache_folder,chroma_cache_dir)

        # Choose mode
        # Local mode
        if self._storing_mode == ChromaMode.LOCAL:
            self._database = chromadb.PersistentClient(path=self.cache_dir)
        # Docker mode
        elif self._storing_mode == ChromaMode.DOCKER:
            self._database = chromadb.HttpClient()
        # Ephemeral mode
        else:
            self._database = chromadb.EphemeralClient()

        # Print status
        Logger.info(f"Start Chroma Vectorstore with {self._storing_mode} Mode!")


    def build_index_from_docs(
            self,
            documents: Union[List[Document],List[BaseNode]],
            embedding_model
    ):
        assert isinstance(documents, list), "Please insert list of documents"
        assert documents, "Data cannot be empty"

        # Build collection, vector store and storage context
        chroma_collection = self._database.get_or_create_collection(name=self.collection_name)
        self._vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        # Build index
        super().build_index_from_docs(documents = documents,embedding_model = embedding_model)

    def load_index(self,embedding_model):
        # Ephemeral case not supported!
        if self._storing_mode == ChromaMode.Ephemeral:
            empheral_mode_msg = "Not supported Ephemeral Mode. This function only works for loading data from database"
            raise Exception(empheral_mode_msg)

        # Check if local mode or Cloud mode
        if self._storing_mode == ChromaMode.LOCAL:
            database = chromadb.PersistentClient(path=self.cache_dir)
            # Define vector store
            chroma_collection = database.get_or_create_collection(self.collection_name)
            self._vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

            # Create vector store
            super().load_index(embedding_model = embedding_model)

