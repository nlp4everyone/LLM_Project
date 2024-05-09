from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService,_QDRANT_COLLECTION
from system_component.system_logging import Logger
from ai_modules.query_modules.custom_query_engine import BaseQueryEngine
import data_ingestion_web

# Reference service
qdrant_service = data_ingestion_web.qdrant_service
llm = data_ingestion_web.llm
embedding_model = data_ingestion_web.embedding_model

def chat_response():
    # Define index
    index = qdrant_service.load_index()