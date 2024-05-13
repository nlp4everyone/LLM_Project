from llama_index.core.ingestion import IngestionPipeline
# from ingestion_modules.custom_loader.web_loader import CustomWebLoader,WebProvider
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
# from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenEmbeddingProvider
from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider,ServiceChatModel
from ai_modules.embedding_modules.service_embedding import ServiceEmbedding
from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService,_QDRANT_COLLECTION
from ingestion_modules.custom_loader.pdf_loader import PDFReader
# Init embedding
# open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
# embedding_model = open_embedding.get_embedding_model()
service_embedding = ServiceEmbedding(service_name="COHERE",model_name="embed-english-light-v3.0")
embedding_model = service_embedding.get_embedding_model()

# Init vector stor service
qdrant_service = QdrantService(mode="local")

# Define large language model
service_provider = ServiceChatModel(service_name="COHERE")
llm = service_provider.get_chat_model()

# Web url for crawling
pdf_path = "test_rag.pdf"

# Default pipeline
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)

def insert(url=pdf_path, pipeline = pipeline):

    pdf_file = PDFReader()
    content = pdf_file.load_data(pdf_path)

    # Run through pipeline
    nodes = pipeline.run(documents=content)

    # Convert nodes to docs
    docs = utils.convert_nodes_to_docs(nodes)

    # Build index
    qdrant_service.build_index_from_docs(documents=docs, embedding_model=embedding_model)
    