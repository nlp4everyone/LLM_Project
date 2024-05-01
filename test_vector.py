from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
# Load data
web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenEmbeddingProvider
open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
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


from ingestion_modules.custom_storing.service_storing import Qdrant_Storing
qdrant_storing = Qdrant_Storing()
qdrant_storing.set_vector_store()
index = qdrant_storing.build_index_from_docs(documents=docs,embedding_model=embedding_model)


# Define large language model
from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider,ServiceChatModel
service_provider = ServiceChatModel()
llm = service_provider.get_chat_model()

# Query Data
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Who is Neymar?")
print(response)
print("Hello")