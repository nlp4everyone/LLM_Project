from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params
from typing import Union
from strenum import StrEnum

class HFEmbeddingModel(StrEnum):
    BGE_SMALL = "BAAI/bge-small-en-v1.5",
    BGE_BASE = "BAAI/bge-base-en-v1.5",
    BGE_LARGE = "BAAI/bge-large-en-v1.5",


class HFEmbedding():
    def __init__(self,model_name: Union[HFEmbeddingModel,str] = HFEmbeddingModel.BGE_SMALL,batch_size: int = 10,max_length: int = 1024, cached_folder_path = params.cache_folder):
        # Define variable
        self._cached_folder_path = cached_folder_path
        self.model_name = model_name
        self.max_length = max_length
        self.batch_size = batch_size

        # Define cache folder
        self._embedding_model = None
        # Only create embedding model with main class
        if self.__class__.__name__ == "HFEmbedding":
            self._embedding_model = HuggingFaceEmbedding(model_name = self.model_name,cache_folder=self._cached_folder_path,embed_batch_size=self.batch_size)

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
