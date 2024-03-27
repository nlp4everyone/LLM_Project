from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params
import os

class HFEmbedding():

    @staticmethod
    def get_embedding_model(model_name = "BAAI/bge-small-en-v1.5",cached_folder = params.cache_folder):
        # Return embedding
        return HuggingFaceEmbedding(model_name = model_name,cache_folder=cached_folder)