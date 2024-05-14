import sys
import os

current_path = os.getcwd()
sys.path.append(current_path)
from ingestion_modules.custom_loader.custom_pdf_loader import CustomPDFReader
from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService
from ai_modules.embedding_modules.service_embedding import (
    ServiceEmbedding,
)  # Change to custom
from llama_index.core.ingestion import IngestionPipeline  # Change to custom
from llama_index.core.text_splitter import SentenceSplitter  # Change to custom
from ingestion_modules import utils

save_path = "save_pdf"


# Function to save pdf after upload
def save_pdf(file, file_name):
    with open(f"{save_path}/{file_name}", "wb") as f:
        f.write(file)
    f.close()


service_embedding = ServiceEmbedding(
    service_name="COHERE", model_name="embed-english-light-v3.0"
)
embedding_model = service_embedding.get_embedding_model()
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)


# Function to create a collection in qdrant db
def create_collection(content: str, collection_name: str):
    # Init vector_store
    qdrant_service = QdrantService(collection_name=collection_name, mode="local")

    nodes = pipeline.run(documents=content)

    # Convert nodes to docs
    docs = utils.convert_nodes_to_docs(nodes)

    # Build index
    qdrant_service.build_index_from_docs(
        documents=docs, embedding_model=embedding_model
    )
