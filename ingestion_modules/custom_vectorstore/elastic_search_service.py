from ingestion_modules.custom_vectorstore.base_method_vectorstore import BaseMethodVectorStore
from config import db_params
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from system_components.system_logging import Logger

# Elastic Search service
ES_NAME = db_params.ES_NAME
ES_CLOUD_ID = db_params.ES_CLOUD_ID
ES_API_KEY = db_params.ES_API_KEY

class ElasticSearchService(BaseMethodVectorStore):
    def __init__(self,collection_name : str = ES_NAME, es_cloud_id : str = ES_CLOUD_ID , es_api_key : str = ES_API_KEY):
        super().__init__()
        self._set_vector_store(collection_name=collection_name,es_cloud_id=es_cloud_id,es_api_key=es_api_key)
        raise Exception("Currently not working")

    def _set_vector_store(self,collection_name : str = ES_NAME, es_cloud_id : str = ES_CLOUD_ID , es_api_key : str = ES_API_KEY):
        # Check type
        assert isinstance(collection_name, str), "Collection name must be a string"
        assert isinstance(es_cloud_id, str), "Cloud id must be a string"
        assert isinstance(es_api_key, str), "API Key must be a string"

        # Define vector store
        self._vector_store = ElasticsearchStore(index_name=collection_name, es_cloud_id=es_cloud_id)
        #                                         es_api_key=es_api_key)
        # self._vector_store = ElasticsearchStore(es_url="http://localhost:9200",index_name="paul_graham")
        # Print status
        Logger.info(f"Start Elastic Search Vectorstore!")
