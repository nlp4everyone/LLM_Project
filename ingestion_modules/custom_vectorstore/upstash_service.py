from llama_index.vector_stores.upstash import UpstashVectorStore
from ingestion_modules.custom_vectorstore.base_method_vectorstore import BaseMethodVectorStore
from config import db_params
# Upstash service
UPSTASH_URL = db_params.UPSTASH_URL
UPSTASH_TOKEN = db_params.UPSTASH_TOKEN

# Notes: Free cloud service with displaying embedding, sentences , etc (https://console.upstash.com/vector)
class UpstashService(BaseMethodVectorStore):
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