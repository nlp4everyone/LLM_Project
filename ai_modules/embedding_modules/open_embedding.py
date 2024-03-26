from llama_index.embeddings.huggingface import HuggingFaceEmbedding

class HFEmbedding():

    @staticmethod
    def get_embedding_model(model_name = "BAAI/bge-small-en-v1.5"):
        return HuggingFaceEmbedding(model_name = model_name)