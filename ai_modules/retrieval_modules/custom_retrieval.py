from llama_index.core import VectorStoreIndex,get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from ai_modules.retrieval_modules import local_models


class BaseRetrieval():
    def __init__(self,nodes=None,similarity_top_k=3):
        if nodes is None:
            raise Exception("Please insert list of nodes data")
        # Nodes
        self.nodes = nodes
        # Index
        self.index = VectorStoreIndex(self.nodes, embed_model=local_models.local_embedding)
        # Params
        self.similarity_top_k = similarity_top_k
        # Retrieval
        self._retrieval = VectorIndexRetriever(self.index,similarity_top_k=self.similarity_top_k)
        # configure response synthesizer
        self._response_synthesizer = get_response_synthesizer(llm=local_models.local_llm)
        # Set query engine
        self._set_query_engine()


    def _set_query_engine(self):
        # Query engine
        self._query_engine = RetrieverQueryEngine(
            retriever=self._retrieval,
            response_synthesizer=self._response_synthesizer,
            node_postprocessors= self._set_postprocessors()
        )
    def _set_postprocessors(self,node_postprocessors=None):
        if node_postprocessors is None:
            default_postprocessors = [SimilarityPostprocessor(similarity_cutoff=0.7)]
            self._node_postprocessors = default_postprocessors
            return self._node_postprocessors
        # Return node
        self._node_postprocessors = node_postprocessors
        return self._node_postprocessors

    def query(self,query):
        # Query to get answer
        return self._query_engine.query(query)

    def retrieve(self,query):
        # Retrieve documents relevant
        return self._query_engine.retrieve(query)


class CustomRetrieval(BaseRetrieval):
    def __init__(self,nodes=None,similarity_top_k=3):
        super().__init__(nodes=nodes,similarity_top_k=similarity_top_k)

    def set_retrieval(self,retrieval:BaseRetrieval):
        # Replace retrieval
        if not isinstance(retrieval,BaseRetrieval):
            raise Exception("Please insert right type of retrieval")
        self._retrieval = retrieval

        # Set query engine
        self._set_query_engine()


