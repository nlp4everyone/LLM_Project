from typing import Union,Literal,Optional
from config.params import *
from ai_modules.embedding_modules.open_embedding import HFEmbedding
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.embeddings.cohere import CohereEmbedding

# Elastic Search Embedding: Notitfy
class ServiceEmbedding(HFEmbedding):
    def __init__(self,model_name: Optional[str] = None,service_name: Literal["COHERE","GRADIENT","MISTRAL","OPENAI","TOGETHER"] = "COHERE",batch_size: int = 10):
        super().__init__()
        # Define variables
        self.list_services = list(supported_services.keys())
        self.model_name = model_name
        # Check service available
        if service_name not in self.list_services: raise Exception(f"Service {service_name} is not supported!")

        # Define key
        self.api_key = supported_services[service_name]["KEY"]

        # Default embedding
        self._embedding_model = CohereEmbedding(cohere_api_key=self.api_key,input_type="search_query")
        # TOGETHER service
        if service_name == "TOGETHER":
            self._embedding_model = TogetherEmbedding(api_key=self.api_key,model_name="togethercomputer/m2-bert-80M-8k-retrieval")
        elif service_name == "COHERE":
            self._embedding_model = CohereEmbedding(cohere_api_key=self.api_key)
