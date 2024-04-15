from typing import Union,Literal,Optional
from config.params import *
from ai_modules.embedding_modules.open_embedding import HFEmbedding
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.embeddings.cohere import CohereEmbedding

# class ServiceEmbedding():
#     def __init__(self,model_name: Union[str,None] = None,service_name: Literal["COHERE","GRADIENT","MISTRAL","OPENAI"] = "COHERE"):
#         # Define variables
#         self.list_services = list(supported_services.keys())
#         # Check service available
#         if service_name not in self.list_services: raise Exception(f"Service {service_name} is not supported!")
#
#         # Define key
#         self.api_key = supported_services[service_name]["KEY"]
#         # Default embedding
#         self.embedding_model = CohereEmbedding(cohere_api_key=self.api_key,input_type="search_query")
#
#     # @staticmethod
#     # def get_embedding_model(model_name: Union[EmbeddingNameEnum,str] = EmbeddingNameEnum.BGE_SMALL, cached_folder = params.cache_folder):
#     #     # Return embedding
#     #     return HuggingFaceEmbedding(model_name = model_name,cache_folder=cached_folder)

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
            print("He")
            self._embedding_model = TogetherEmbedding(api_key=self.api_key,model_name="togethercomputer/m2-bert-80M-8k-retrieval")
    # def get_text_embedding(self,input: str):
    #     # Get text embedding
    #     return self.embedding_model.get_text_embedding(input)
    #
    # async def aget_text_embedding(self,input: str):
    #     # Get text embedding
    #     embedding = await self.embedding_model.aget_text_embedding(input)
    #     return embedding
    #
    # def get_query_embedding(self, input: str):
    #     # Get text embedding
    #     return self.embedding_model.get_query_embedding(input)
    #
    # async def aget_query_embedding(self, input: str):
    #     # Get text embedding
    #     embedding = await self.embedding_model.aget_query_embedding(input)
    #     return embedding
