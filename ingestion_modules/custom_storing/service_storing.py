from ingestion_modules.custom_storing.base_method_storing import BaseMethodStoring
from config import db_params
from llama_index.vector_stores.upstash import UpstashVectorStore
from llama_index.vector_stores.elasticsearch import ElasticsearchStore


# Define params
# Upstash service
UPSTASH_URL = db_params.UPSTASH_URL
UPSTASH_TOKEN = db_params.UPSTASH_TOKEN

# Elastic Search service
ES_NAME = db_params.ES_NAME
ES_CLOUD_ID = db_params.ES_CLOUD_ID
ES_API_KEY = db_params.ES_API_KEY



# Notes: Free cloud service with displaying embedding, sentences , etc (https://console.upstash.com/vector)
class Upstash_Storing(BaseMethodStoring):
    def set_vector_store(self, upstash_url : str = UPSTASH_URL , upstash_token : str = UPSTASH_TOKEN):
        # Check type# Check type
        assert isinstance(upstash_url, str), "Upstash url must be a string"
        assert isinstance(upstash_token, str), "Upstash token must be a string"

        # Define vector store
        self._vector_store = UpstashVectorStore(url=upstash_url,token=upstash_token)
        # Print
        print(f"Start Uptash Vector Store!")

class ES_Storing(BaseMethodStoring):
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
