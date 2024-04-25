from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params
from typing import Union,Optional,List
from strenum import StrEnum
from llama_index.embeddings.fastembed import FastEmbedEmbedding,base
import os

class OpenEmbeddingService(StrEnum):
    HuggingFace = "HuggingFace",
    FastEmbed = "FastEmbed",

class OpenEmbeddingProvider():
    def __init__(self,model_name: Optional[str] = None,service_name: OpenEmbeddingService = OpenEmbeddingService.HuggingFace,batch_size: int = 10,max_length: int = 1024, embedding_model_folder = params.embedding_model_folder):
        # Define variable
        self._embedding_model_folder = embedding_model_folder
        self.model_name = model_name
        self.max_length = max_length
        self.batch_size = batch_size

        # Create folder
        os.makedirs(embedding_model_folder,exist_ok=True)

        # Define cache folder
        self._embedding_model = None
        # Only create embedding model with main class
        if self.__class__.__name__ == "OpenEmbeddingProvider":
            # Hugging Face
            if service_name == OpenEmbeddingService.HuggingFace:
                self._embedding_model = HuggingFaceEmbedding(cache_folder=self._embedding_model_folder,embed_batch_size=self.batch_size)
            # Fast Embed
            elif service_name == OpenEmbeddingService.FastEmbed:

                self._embedding_model = FastEmbedEmbedding(cache_dir=self._embedding_model_folder)
                # self._embedding_model = FastEmbedEmbedding()
            else:
                raise Exception(f"Service {service_name} is not supported!")

            # Insert params
            # self._embedding_model.max_length = self.max_length
            # Check model name
            if self.model_name is not None: self._embedding_model.model_name = model_name
            # Batch size
            batch_size = self._embedding_model.embed_batch_size
            print(f"Initiate {service_name} with model: {self._embedding_model.model_name}, batch size {batch_size}")

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

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]):
        return self._embedding_model.similarity(embedding1,embedding2)


