from ingestion_modules.custom_vectorstore.base_method_vectorstore import BaseMethodVectorStore
from config import db_params
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from typing import Literal,List
from system_component.system_logging import Logger
from llama_index.core import Document
import qdrant_client

# Define params
# Qdrant service
_QDRANT_TOKEN = db_params.QDRANT_TOKEN
_QDRANT_URL = db_params.QDRANT_URL
_QDRANT_PORT = db_params.QDRANT_PORT
_QDRANT_COLLECTION = db_params.QDRANT_COLLECTION


class QdrantService(BaseMethodVectorStore,QdrantClient):
    def __init__(self,mode : Literal["memory","local","cloud"] = "local", qdrant_token : str = _QDRANT_TOKEN , qdrant_url : str = _QDRANT_URL,collection_name: str = _QDRANT_COLLECTION):
        super().__init__()
        # Init params
        self.qdrant_token = qdrant_token
        self.qdrant_url = qdrant_url
        self._mode = mode
        self.collection_name = collection_name

        # Check type
        assert isinstance(qdrant_token, str), "Cloud id must be a string"
        assert isinstance(qdrant_url, str), "API Key must be a string"

        # Init client
        # self._client = None
        # Memory mode
        if self._mode == "memory":
            self._client = qdrant_client.QdrantClient(
                location=":memory:"
            )
        # Local host mode
        elif self._mode == "local":
            self._client = qdrant_client.QdrantClient(
                host="localhost",
                port=_QDRANT_PORT
            )
        elif self._mode == "cloud":
            self._client = qdrant_client.QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_token
            )
        else:
            Logger.exception("Wrong qdrant mode")
            raise Exception("Wrong qdrant mode")

        # Set vector store
        self._set_vector_store()


    def _set_vector_store(self):
        # Validating
        assert self.collection_name, "Collection name cant be empty"
        # Define vector store
        try:
            # Logging status
            Logger.info(f"Start Qdrant Vectorstore with collection name {self.collection_name}")
            self._vector_store = QdrantVectorStore(client=self._client, collection_name=self.collection_name)

        except:
            Logger.exception("Connection Refused")
            raise Exception("Connection Refused")

    def build_index_from_docs(self,documents: List[Document], embedding_model, mode: Literal["insert", "override"] = "insert"):
        # When recreate collection available
        if mode == "override":
            # Check if collection existed, delete it
            if self.collection_exists(self.collection_name): self.delete_collection(self.collection_name)

        # Set vector store again
        self._set_vector_store()
        # Apply abstraction
        super().build_index_from_docs(documents=documents,embedding_model=embedding_model)


    def load_index(self, embedding_model):
        assert self.collection_name, "Collection cant be None"
        if not self._client.collection_exists(self.collection_name):
            raise Exception(f"Collection: {self.collection_name} isn't existed")
        # Load normal
        index = super().load_index(embedding_model=embedding_model)
        return index