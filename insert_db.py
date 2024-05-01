# Import modules
from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenEmbeddingProvider
from llama_index.core.ingestion import IngestionPipeline
from ingestion_modules.custom_storing.simple_storing import SimpleStoring

# Load data
web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")

# Instanate embeddung
open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
embedding_model = open_embedding.get_embedding_model()

# Ingestion
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)
nodes = pipeline.run(documents=docs)

# Convert nodes to docs
docs = utils.convert_nodes_to_docs(nodes)

# Insert to db
# qdrant_service = Qdrant_Storing(mode=QdrantMode.LOCALHOST)
# index = qdrant_service.build_index_from_docs(documents=docs,embedding_model=embedding_model)
simple_storing = SimpleStoring()
simple_storing.build_index_from_docs(documents=docs,embedding_model=embedding_model)

