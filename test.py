from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
# Load data
web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")

from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils

# Qdrant
from llama_index.core import StorageContext
# from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import SimpleVectorStore
# import qdrant_client
from ai_modules.embedding_modules.open_embedding import OpenEmbeddingProvider,OpenService
embedding_provider = OpenEmbeddingProvider(service_name=OpenService.FastEmbed)
embedding_model = embedding_provider.get_embedding_model()

# Ingestion
from llama_index.core.ingestion import IngestionPipeline
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)
docs = pipeline.run(documents=docs)


import time

# Convert nodes to docs
docs = utils.convert_nodes_to_docs(docs)


start_time = time.perf_counter()
index = VectorStoreIndex.from_documents(docs,embed_model = embedding_model)
duration = time.perf_counter() - start_time
print(duration)


# client = qdrant_client.QdrantClient(
#     url="https://node-0-eeae207b-0004-44d8-bf80-56e76aa88392.us-east4-0.gcp.cloud.qdrant.io",
#     # set API KEY for Qdrant Cloud
#     api_key="j8RFyWFGT_5XGCry3FCl25N4sFDcK3dK_d5rK4p8_Dr5gPtLnJM2WQ",
# )
# vector_store = QdrantVectorStore(client=client, collection_name="Qdrant")
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# index = VectorStoreIndex.from_documents(
#     documents=docs,
#     storage_context=storage_context,
#     embed_model = embedding_model
# )
# from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModel
# service_chatmodel = ServiceChatModel()
# llm = service_chatmodel.get_chat_model()
# #
# query_engine = index.as_query_engine(llm=llm)
# ans = query_engine.query("Who is Neymar?")
# print(ans)

