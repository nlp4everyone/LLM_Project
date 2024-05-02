from ingestion_modules.custom_storing.base_method_storing import BaseMethodStoring
from config import db_params
from llama_index.vector_stores.upstash import UpstashVectorStore
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from enum import Enum
import qdrant_client

# Define params
# Upstash service
UPSTASH_URL = db_params.UPSTASH_URL
UPSTASH_TOKEN = db_params.UPSTASH_TOKEN

# Elastic Search service
ES_NAME = db_params.ES_NAME
ES_CLOUD_ID = db_params.ES_CLOUD_ID
ES_API_KEY = db_params.ES_API_KEY

# Qdrant service
QDRANT_TOKEN = db_params.QDRANT_TOKEN
QDRANT_URL = db_params.QDRANT_URL
QDRANT_PORT = db_params.QDRANT_PORT
QDRANT_COLLECTION = db_params.QDRANT_COLLECTION

class QdrantMode(Enum):
    MEMORY = 0,
    LOCALHOST = 1,
    CLOUD = 2

# Notes: Free cloud service with displaying embedding, sentences , etc (https://console.upstash.com/vector)
class Upstash_Storing(BaseMethodStoring):
    def __init__(self):
        super().__init__()
        self.set_vector_store()

    def set_vector_store(self, upstash_url : str = UPSTASH_URL , upstash_token : str = UPSTASH_TOKEN):
        # Check type# Check type
        assert isinstance(upstash_url, str), "Upstash url must be a string"
        assert isinstance(upstash_token, str), "Upstash token must be a string"

        # Define vector store
        self._vector_store = UpstashVectorStore(url=upstash_url,token=upstash_token)
        # Print
        print(f"Start Uptash Vector Store!")

class ES_Storing(BaseMethodStoring):
    def __init__(self):
        super().__init__()
        self.set_vector_store()

    def set_vector_store(self,collection_name : str = ES_NAME, es_cloud_id : str = ES_CLOUD_ID , es_api_key : str = ES_API_KEY):
        # Check type
        assert isinstance(collection_name, str), "Collection name must be a string"
        assert isinstance(es_cloud_id, str), "Cloud id must be a string"
        assert isinstance(es_api_key, str), "API Key must be a string"

        # Define vector store
        self._vector_store = ElasticsearchStore(index_name=collection_name, es_cloud_id=es_cloud_id,
                                                es_api_key=es_api_key)
        # Print
        print(f"Start Elastic Search Vectorstore!")

class Qdrant_Storing(BaseMethodStoring,QdrantClient):
    def __init__(self,mode : QdrantMode = QdrantMode.MEMORY,collection_name : str = QDRANT_COLLECTION, qdrant_token : str = QDRANT_TOKEN , qdrant_url : str = QDRANT_URL):
        super().__init__()
        # Init params
        self.qdrant_token = qdrant_token
        self.qdrant_url = qdrant_url
        self.collection_name = collection_name
        self._mode = mode

        # Check type
        assert isinstance(collection_name, str), "Collection name must be a string"
        assert isinstance(qdrant_token, str), "Cloud id must be a string"
        assert isinstance(qdrant_url, str), "API Key must be a string"

        # Init client
        self._client = None
        # Memory mode
        if self._mode == QdrantMode.MEMORY:
            self._client = qdrant_client.QdrantClient(
                location=":memory:"
            )
        # Local host mode
        elif self._mode == QdrantMode.LOCALHOST:
            self._client = qdrant_client.QdrantClient(
                host="localhost",
                port=QDRANT_PORT
            )
        elif self._mode == QdrantMode.CLOUD:
            self._client = qdrant_client.QdrantClient(
                url=self.qdrant_url,
                api_key=self.qdrant_token
            )
        else:
            raise Exception("Wrong qdrant mode")
        # Set vector store
        self.set_vector_store()

    def set_vector_store(self):
        # Define vector store
        self._vector_store = QdrantVectorStore(client=self._client, collection_name="llama-project")
        # Print
        print(f"Start Qdrant Vectorstore!")
