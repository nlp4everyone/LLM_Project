from ingestion_modules.custom_vectorstore.base_method_vectorstore import (
    BaseMethodVectorStore,
)
from config import db_params
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from typing import Literal, List , Union
from system_components.system_logging import Logger
from llama_index.core import Document
import qdrant_client
from llama_index.core import StorageContext,VectorStoreIndex

# Define params
# Qdrant service
_QDRANT_MODE = db_params.QDRANT_MODE
_QDRANT_TOKEN = db_params.QDRANT_TOKEN
_QDRANT_URL = db_params.QDRANT_URL
_QDRANT_PORT = db_params.QDRANT_PORT
_QDRANT_COLLECTION = db_params.QDRANT_COLLECTION

# Document
# https://github.com/qdrant/fastembed\
# https://qdrant.tech/documentation/concepts/

class QdrantService(BaseMethodVectorStore, QdrantClient):
    def __init__(
        self,
        collection_name: str = None,
        mode: Literal["memory", "local", "cloud"] = _QDRANT_MODE,
        use_async : bool = True,
        qdrant_token: str = _QDRANT_TOKEN,
        qdrant_url: str = _QDRANT_URL,
    ):
        super().__init__()
        # Init params
        self._mode = mode if mode else "local"
        self._use_async = use_async
        self.qdrant_token = qdrant_token
        self.qdrant_url = qdrant_url

        # collection_name is passed in fastapi. If not call api, take collection_name from env
        self.collection_name = (
            collection_name if collection_name else _QDRANT_COLLECTION
        )

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

        # Asynchronous mode
        if self._use_async:
            # Local mode
            if self._mode == "local":
                self._aclient = qdrant_client.AsyncQdrantClient(
                    host="localhost",
                    port=_QDRANT_PORT
                )
            # Cloud mode
            elif self._mode == "cloud":
                self._aclient = qdrant_client.AsyncQdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_token
                )
            else:
                raise Exception("Mode memory cant not support asynchronous")

        # Log state
        Logger.info("Init Qdrant Vectorstore!")

    def _set_vector_store(self):
        # Validating
        assert self.collection_name, "Collection name cant be empty"

        # Define vector store
        try:
            # Logging status
            Logger.info(
                f"Start Qdrant Vectorstore with collection name {self.collection_name}"
            )

            # Set vector store without async
            if not self._use_async:
                self._vector_store = QdrantVectorStore(
                    client = self._client,
                    collection_name = self.collection_name
                )
            else:
                self._vector_store = QdrantVectorStore(
                    client = self._client,
                    collection_name = self.collection_name,
                    aclient = self._aclient,
                    prefer_grpc=True
                )
            Logger.info(f"Start Qdrant Vectorstore with collection name {self.collection_name}")

        except Exception as e:
            Logger.info(e)


    def build_index_from_docs(
        self,
        documents: Union[List[Document],List[BaseNode]],
        embedding_model,
        mode: Literal["insert", "override"] = "insert",
    ):
        # When recreate collection available
        if mode == "override":
            # Check if collection existed, delete it
            # if self.collection_exists(self.collection_name): self.delete_collection(self.collection_name)
            pass

        # Set vector store again ( New)
        self._set_vector_store()
        # Apply abstraction
        # super().build_index_from_docs(
        #     documents=documents, embedding_model=embedding_model
        # )
        # Check service
        if self._vector_store == None:
            Logger.exception("Please set vector store")
            raise Exception("Please set vector store")

        # Check input
        assert isinstance(documents, list), "Please insert list of documents"
        assert documents, "Data cannot be empty"

        # Build storage context
        storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        # Update state
        Logger.info("Building index ...")

        # Check nodes or doc
        if isinstance(documents[0], Document):
            return VectorStoreIndex.from_documents(documents=documents,
                                                   storage_context=storage_context,
                                                   embed_model=embedding_model,
                                                   use_async = self._use_async)
        # Vector store with Node mode
        return VectorStoreIndex(nodes = documents, embed_model = embedding_model, storage_context = storage_context,use_async = self._use_async)

    def load_index(self, embedding_model):
        assert self.collection_name, "Collection cant be None"
        # if not self.collection_exists(self.collection_name):
        #     raise Exception(f"Collection: {self.collection_name} isn't existed")

        # Set vector store again ( New)
        self._set_vector_store()
        # Load normal
        index = super().load_index(embedding_model=embedding_model)
        return index