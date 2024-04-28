from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
# Load data
web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
from ai_modules.embedding_modules.open_embedding import OpenEmbeddingService,OpenEmbeddingProvider
open_embedding = OpenEmbeddingProvider(service_name=OpenEmbeddingService.FastEmbed)
embedding_model = open_embedding.get_embedding_model()

# Ingestion
from llama_index.core.ingestion import IngestionPipeline
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)
docs = pipeline.run(documents=docs)

# Convert nodes to docs
docs = utils.convert_nodes_to_docs(docs)

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.upstash import UpstashVectorStore
from llama_index.core import StorageContext

from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, AsyncQdrantClient
import qdrant_client

# creates a persistant index to disk
client = qdrant_client.QdrantClient(
    # you can use :memory: mode for fast and light-weight experiments,
    # it does not require to have Qdrant deployed anywhere
    # but requires qdrant-client >= 1.1.1
    # location=":memory:"
    # otherwise set Qdrant instance address with:
    # url="http://:"
    # otherwise set Qdrant instance with host and port:
    host="localhost",
    port=6333
    # set API KEY for Qdrant Cloud
    # api_key="",
)
vector_store = QdrantVectorStore(client=client, collection_name="paul_graham")

storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    docs,
    storage_context=storage_context,
)


# Define large language model
from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider
service_provider = ServiceChatModelProvider()
llm = service_provider.get_chat_model()

# Query Data
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Who is Neymar?")
print(response)