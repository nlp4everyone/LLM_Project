from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService,_QDRANT_COLLECTION
from system_component.system_logging import Logger
from ai_modules.query_modules.custom_query_engine import BaseQueryEngine
import data_ingestion_pdf

# Reference service
qdrant_service = data_ingestion_pdf.qdrant_service
llm = data_ingestion_pdf.llm
embedding_model = data_ingestion_pdf.embedding_model

def querying_step(question: str):
    assert question, "Question cant be empty"
    # Query Data
    index = qdrant_service.load_index(embedding_model=embedding_model)

    # Define query engine
    query_engine = BaseQueryEngine(index=index, chat_model=llm)
    # Print response
    response = query_engine.query(query=question)

    # # Print retrieval
    # retrieval_docs, _ = query_engine.retrieve(query="Who is Neymar?")
    return response

def main():
    # When collection is not existed, create new collection
    if not qdrant_service.collection_exists(collection_name=_QDRANT_COLLECTION):
        data_ingestion_pdf.insert()

    # Find answer
    question = "What is title of Article 2"
    response = querying_step(question)
    print("\n\n\n\n")
    print(response)
    Logger.info(response)
    print("\n\n\n\n")

if __name__ == "__main__":
    main()