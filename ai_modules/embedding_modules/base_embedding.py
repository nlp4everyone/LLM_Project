from typing import List


class BaseEmbedding():
    def __init__(self,batch_size: int = 10,max_length: int = 1024):
        # Define variable
        self.max_length = max_length
        self.batch_size = batch_size\

        # Define embedding model
        self._embedding_model = None

    def get_embedding_model(self):
        # Return embedding model
        return self._embedding_model

    def get_text_embedding(self,input: str):
        # Check embedding model
        if self._embedding_model is None: raise Exception("Require embedding model")
        # Check input
        assert isinstance(input,str), "Input must be string"
        assert input, "Input can be empty"

        # Get text embedding
        return self._embedding_model.get_text_embedding(input)

    async def aget_text_embedding(self,input: str):
        # Check embedding model
        if self._embedding_model is None: raise Exception("Require embedding model")
        # Check input
        assert isinstance(input, str), "Input must be string"
        assert input, "Input can be empty"

        # Get text embedding
        embedding = await self._embedding_model.aget_text_embedding(input)
        return embedding

    def get_query_embedding(self, input: str):
        # Check embedding model
        if self._embedding_model is None: raise Exception("Require embedding model")
        # Check input
        assert isinstance(input, str), "Input must be string"
        assert input, "Input can be empty"

        # Get text embedding
        return self._embedding_model.get_query_embedding(input)

    async def aget_query_embedding(self, input: str):
        # Check embedding model
        if self._embedding_model is None: raise Exception("Require embedding model")
        # Check input
        assert isinstance(input, str), "Input must be string"
        assert input, "Input can be empty"

        # Get text embedding
        embedding = await self._embedding_model.aget_query_embedding(input)
        return embedding

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]):
        # Check embedding model
        if self._embedding_model is None: raise Exception("Require embedding model")

        return self._embedding_model.similarity(embedding1,embedding2)