from llama_index.core import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from typing import Optional

# Base post processor
default_postprocessors = [
    # SimilarityPostprocessor(similarity_cutoff=0.7)
]


class BaseQueryEngine():
    def __init__(self,index, chat_model, similarity_top_k=3):
        assert chat_model, "Chat model cant be empty"
        assert index, "Index cant be empty"

        # Default params
        self.similarity_top_k = similarity_top_k
        self._index = index
        self._chat_model = chat_model

        # Retrieval
        self._retrieval = VectorIndexRetriever(self._index, similarity_top_k=self.similarity_top_k)
        # configure response synthesizer
        self._response_synthesizer = get_response_synthesizer(llm=self._chat_model)
        # Set query engine
        self.update_query_engine()

    def update_query_engine(self,node_postprocessor : Optional[list] = None):
        # Base postprocessor
        postprocessor = default_postprocessors
        if node_postprocessor is not None: postprocessor = node_postprocessor

        # Return query engine
        self._query_engine = RetrieverQueryEngine(
            retriever=self._retrieval,
            response_synthesizer=self._response_synthesizer,
            node_postprocessors= postprocessor
        )
        return self._query_engine

    def query(self, query:str):
        assert query, "Query must be string"

        # Query to get answer
        return self._query_engine.query(query)

    def retrieve(self, query:str):
        assert query, "Query must be string"

        # Retrieve documents relevant
        raw_retrieval_docs = self._query_engine.retrieve(query)
        # Structure retrieval document
        structured_documents = [{"Content":doc.text,"metadata":doc.metadata,"score":doc.score} for doc in raw_retrieval_docs]
        return raw_retrieval_docs,structured_documents


# class CustomRetrieval(BaseRetrieval):
#     def __init__(self, nodes=None, similarity_top_k=3):
#         super().__init__(nodes=nodes, similarity_top_k=similarity_top_k)
#
#     def set_retrieval(self, retrieval: BaseRetrieval):
#         # Replace retrieval
#         if not isinstance(retrieval, BaseRetrieval):
#             raise Exception("Please insert right type of retrieval")
#         self._retrieval = retrieval
#
#         # Set query engine
#         self._set_query_engine()
