from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider,ServiceChatModel
from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService,_QDRANT_COLLECTION
from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenEmbeddingProvider
from llama_index.core.ingestion import IngestionPipeline
from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
import logging

# Creating an object
logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',level=logging.INFO)
logger = logging.getLogger()

# Init embedding
open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
embedding_model = open_embedding.get_embedding_model()

# Init
qdrant_service = QdrantService(mode="local")

# Define large language model
service_provider = ServiceChatModel()
llm = service_provider.get_chat_model()

# Web url for crawling
web_url = "https://en.wikipedia.org/wiki/Neymar"

def insert_data(url=web_url):
    # Load data
    web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
    docs = web_loader.load_data(url)

    # Ingestion
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=1000, chunk_overlap=200),
        ],
    )
    nodes = pipeline.run(documents=docs)

    # Convert nodes to docs
    docs = utils.convert_nodes_to_docs(nodes)
    index = qdrant_service.build_index_from_docs(documents=docs, embedding_model=embedding_model)

def main():
    # When collection is not existed, create new collection
    if not qdrant_service.collection_exists(collection_name=_QDRANT_COLLECTION):
        insert_data()
        logger.debug(f"Insert collection {_QDRANT_COLLECTION}")

    # Query Data
    index = qdrant_service.load_index(embedding_model=embedding_model)
    query_engine = index.as_query_engine(llm=llm,verbose=True)
    response = query_engine.query("Who is Neymar?")
    print("Response")
    print(response)
    logger.info("Hello")


if __name__ == "__main__":
    main()