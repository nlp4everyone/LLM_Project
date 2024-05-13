from llama_index.vector_stores.upstash import UpstashVectorStore
from ingestion_modules.custom_vectorstore.base_method_vectorstore import BaseMethodVectorStore
from config import db_params
from system_component.system_logging import Logger

# Upstash service
UPSTASH_URL = db_params.UPSTASH_URL
UPSTASH_TOKEN = db_params.UPSTASH_TOKEN

# Notes: Free cloud service with displaying embedding, sentences , etc (https://console.upstash.com/vector)
class UpstashService(BaseMethodVectorStore):
    def __init__(self, upstash_url : str = UPSTASH_URL , upstash_token : str = UPSTASH_TOKEN):
        super().__init__()
        # Set value
        self.upstash_url = upstash_url
        self.upstash_token = upstash_token
        # Set vector store
        self._set_vector_store(upstash_url = upstash_url, upstash_token = upstash_token)

    def _set_vector_store(self, upstash_url : str, upstash_token : str):
        # Check type# Check type
        assert isinstance(upstash_url, str), "Upstash url must be a string"
        assert isinstance(upstash_token, str), "Upstash token must be a string"

        # Update status
        Logger.info(f"Start Uptash Vector Store!")
        # Define vector store
        return UpstashVectorStore(url=upstash_url,token=upstash_token)
