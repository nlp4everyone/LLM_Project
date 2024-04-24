from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params
from typing import Union,Optional
# from strenum import StrEnum
from enum import Enum
from llama_index.embeddings.fastembed import FastEmbedEmbedding

class OpenEmbeddingService(Enum):
    HuggingFace = 0,
    FastEmbed = 1,

class OpenEmbeddingProvider():
    def __init__(self,model_name: Optional[str] = None,service_name: OpenEmbeddingService = OpenEmbeddingService.HuggingFace,batch_size: int = 10,max_length: int = 1024, cached_folder_path = params.cache_folder):
        # Define variable
        self._cached_folder_path = cached_folder_path
        self.model_name = model_name
        self.max_length = max_length
        self.batch_size = batch_size

        # Define cache folder
        self._embedding_model = None
        # Only create embedding model with main class
        if self.__class__.__name__ == "OpenEmbedding":
            # Hugging Face
            if service_name == OpenEmbeddingService.HuggingFace:
                self._embedding_model = HuggingFaceEmbedding(cache_folder=self._cached_folder_path,embed_batch_size=self.batch_size)
            # Fast Embed
            elif service_name == OpenEmbeddingService.FastEmbed:
                self._embedding_model = FastEmbedEmbedding(cache_dir=self._cached_folder_path)
            else:
                raise Exception(f"Service {service_name} is not supported!")
            # Insert params
            self._embedding_model.max_length = self.max_length
            # Check model name
            if self.model_name is not None: self._embedding_model.model_name = model_name

    def get_embedding_model(self):
        # Return embedding model
        return self._embedding_model

    def get_text_embedding(self,input: str):
        # Get text embedding
        return self._embedding_model.get_text_embedding(input)

    async def aget_text_embedding(self,input: str):
        # Get text embedding
        embedding = await self._embedding_model.aget_text_embedding(input)
        return embedding

    def get_query_embedding(self, input: str):
        # Get text embedding
        return self._embedding_model.get_query_embedding(input)

    async def aget_query_embedding(self, input: str):
        # Get text embedding
        embedding = await self._embedding_model.aget_query_embedding(input)
        return embedding
