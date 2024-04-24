#

# from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
# # Load data
# web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
# docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")
#
# from llama_index.core.node_parser import SemanticSplitterNodeParser
# from llama_index.core.text_splitter import SentenceSplitter
# from ingestion_modules import utils
from llama_index.core import VectorStoreIndex
# from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core import StorageContext
from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenService
open_embedding = OpenEmbedding(service_name=OpenService.FastEmbed)
embedding_model = open_embedding.get_embedding_model()
#
# # Ingestion
# from llama_index.core.ingestion import IngestionPipeline
# pipeline = IngestionPipeline(
#     transformations=[
#         SentenceSplitter(chunk_size=1000, chunk_overlap=200),
#     ],
# )
# docs = pipeline.run(documents=docs)
# # Convert nodes to docs
# docs = utils.convert_nodes_to_docs(docs)

#
from llama_index.vector_stores.astra_db import AstraDBVectorStore
astra_db_store = AstraDBVectorStore(
    token=astra_info["token"],
    api_endpoint="https://24c6d557-7699-4335-b798-98499b8069aa-us-east1.apps.astra.datastax.com",
    collection_name="test_table",
    embedding_dimension=384,
)
# index = VectorStoreIndex.from_documents(docs,embed_model = embedding_model)

storage_context = StorageContext.from_defaults(vector_store=astra_db_store)
index = VectorStoreIndex.from_vector_store()
# index = VectorStoreIndex.from_documents(
#     docs, storage_context=storage_context,
#     embed_model = embedding_model
# )