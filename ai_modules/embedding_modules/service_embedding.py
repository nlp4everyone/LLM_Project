from typing import Literal,Optional,Union
from config.params import *
from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.embeddings.nomic import NomicEmbedding
from ai_modules.embedding_modules.base_embedding import BaseEmbedding
from system_component import Logger

# Elastic Search Embedding: Notitfy
class ServiceEmbedding(BaseEmbedding):
    def __init__(self,model_name: Optional[str] = None,service_name: Union[Literal["COHERE","GRADIENT","MISTRAL","OPENAI","TOGETHER","VOYAGE","NOMIC"],str] = "COHERE",batch_size: int = 10,max_length : int = 1024):
        super().__init__(batch_size = batch_size,max_length= max_length)
        # Define variables
        self.list_services = list(supported_services.keys())
        self.model_name = model_name

        # Check service available
        if service_name not in self.list_services: raise Exception(f"Service {service_name} is not supported!")

        # Define key
        self.api_key = supported_services[service_name]["KEY"]
        # TOGETHER service
        if service_name == "TOGETHER":
            from llama_index.embeddings.together import TogetherEmbedding
            self._embedding_model = TogetherEmbedding(api_key=self.api_key,model_name="togethercomputer/m2-bert-80M-8k-retrieval")
        elif service_name == "COHERE":
            from llama_index.embeddings.cohere import CohereEmbedding
            self._embedding_model = CohereEmbedding(cohere_api_key=self.api_key)
        elif service_name == "VOYAGE":
            from llama_index.embeddings.voyageai import VoyageEmbedding
            self._embedding_model = VoyageEmbedding(model_name="voyage-2",voyage_api_key=self.api_key,embed_batch_size=self.batch_size)
        elif service_name == "OPENAI":
            self._embedding_model = OpenAIEmbedding(api_key=self.api_key,embed_batch_size=self.batch_size)
        elif service_name == "MISTRAL":
            mistral_exception_msg = "Mistral currently required charge"
            Logger.exception(mistral_exception_msg)
            raise Exception(mistral_exception_msg)
        # elif service_name == "NOMIC":
        #     self._embedding_model = NomicEmbedding(api_key=self.api_key,embed_batch_size=self.batch_size)
        else:
            service_exception_msg = f"Service {service_name} is not supported!"
            Logger.exception(service_exception_msg)
            raise Exception(service_exception_msg)

        # Specify model name and batch size
        self._embedding_model.model_name = self.model_name
        self._embedding_model.embed_batch_size = self.batch_size

        #Logging Info
        Logger.info(f"Launch {service_name} service embedding!")

