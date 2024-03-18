from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params
from llama_index.llms.ollama import Ollama
import os

# Embedding
embedding_cache_folder = os.path.join(params.cache_folder,"embedding_cache")
try:
    local_embedding = HuggingFaceEmbedding(model_name=params.local_embedding_model,cache_folder=embedding_cache_folder) # Local embedding
except:
    raise Exception("Cannot install embedding")

# LLM
embedding_cache_folder = os.path.join(params.cache_folder,"embedding_cache")
try:
    local_llm = Ollama(model="zephyr", request_timeout=60.0) # Local LLM
except:
    raise Exception("Cannot install LLM")

