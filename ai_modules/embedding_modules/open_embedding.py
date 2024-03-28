from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params
from typing import Union
from strenum import StrEnum
class EmbeddingNameEnum(StrEnum):
    BGE_SMALL = "BAAI/bge-small-en-v1.5",
    BGE_BASE = "BAAI/bge-base-en-v1.5",
    BGE_LARGE = "BAAI/bge-large-en-v1.5",


class HFEmbedding():

    @staticmethod
    def get_embedding_model(model_name: Union[EmbeddingNameEnum,str] = EmbeddingNameEnum.BGE_SMALL, cached_folder = params.cache_folder):
        # Return embedding
        return HuggingFaceEmbedding(model_name = model_name,cache_folder=cached_folder)