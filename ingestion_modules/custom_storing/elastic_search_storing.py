from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import StorageContext,VectorStoreIndex
from config import db_params
from llama_index.core import Document
from typing import List

# Define params
ES_NAME = db_params.ES_NAME
ES_CLOUD_ID = db_params.ES_CLOUD_ID
ES_API_KEY = db_params.ES_API_KEY

class ES_Storing():
    def __init__(self,collection_name : str = ES_NAME, es_cloud_id : str = ES_CLOUD_ID , es_api_key : str = ES_API_KEY):
        # Check type
        assert isinstance(collection_name,str), "Collection name must be a string"
        assert isinstance(es_cloud_id, str), "Cloud id must be a string"
        assert isinstance(es_api_key, str), "API Key must be a string"

        # Define vector store
        self._vector_store = ElasticsearchStore(index_name=collection_name,es_cloud_id=es_cloud_id,es_api_key=es_api_key)
        # Print
        print(f"Start Elastic Search Vectorstore!")

    def get_vector_store(self):
        # Return vector store
        return self._vector_store

    def build_index_from_docs(self, documents : List[Document], embedding_model = None):
        if embedding_model == None: raise Exception("Insert embedding model")

        # Build storage context
        storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        return VectorStoreIndex.from_documents(documents=documents,storage_context=storage_context,embed_model=embedding_model)

    def load_index(self, embedding_model = None):
        if embedding_model == None: raise Exception("Insert embedding model")

        # Build storage context
        storage_context = StorageContext.from_defaults(vector_store=self._vector_store)
        return VectorStoreIndex.from_vector_store(vector_store=self._vector_store,storage_context=storage_context,embed_model=embedding_model)