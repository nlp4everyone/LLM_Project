from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
# Load data
web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.text_splitter import SentenceSplitter

# Ingestion
from llama_index.core.ingestion import IngestionPipeline
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)
docs = pipeline.run(documents=docs)
print(docs)

# Qdrant
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import SimpleVectorStore
import qdrant_client
client = qdrant_client.QdrantClient(
    url="https://node-0-eeae207b-0004-44d8-bf80-56e76aa88392.us-east4-0.gcp.cloud.qdrant.io",
    # set API KEY for Qdrant Cloud
    api_key="j8RFyWFGT_5XGCry3FCl25N4sFDcK3dK_d5rK4p8_Dr5gPtLnJM2WQ",
)
vector_store = QdrantVectorStore(client=client, collection_name="Qdrant")
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents=docs,
    storage_context=storage_context,
)

# print(index)

print(index)
