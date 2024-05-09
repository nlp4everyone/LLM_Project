from ai_modules.query_modules.custom_query_engine import BaseQueryEngine
from ai_modules.chatmodel_modules.base_chatmodel import BaseChatModel
from ai_modules.embedding_modules.base_embedding import BaseEmbedding

def querying_step(question: str,vector_service, chat_model: BaseChatModel, embedding_model: BaseEmbedding):
    assert question, "Question cant be empty"
    # Query Data
    index = vector_service.load_index(embedding_model=embedding_model)

    # Define query engine
    query_engine = BaseQueryEngine(index=index, chat_model=chat_model)
    # Print response
    response = query_engine.query(query=question)

    # # Print retrieval
    # retrieval_docs, _ = query_engine.retrieve(query="Who is Neymar?")
    return response
