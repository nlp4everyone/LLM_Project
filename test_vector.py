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

# Start Vector Store
# from ingestion_modules.custom_storing.chroma_storing import ChromaStoring
# chroma_storing = ChromaStoring()
# index = chroma_storing.build_index_from_docs(documents=docs,embedding_model=embedding_model)

from ingestion_modules.custom_storing.elastic_search_storing import ES_Storing
es_storing = ES_Storing()
index = es_storing.load_index(embedding_model=embedding_model)


# Define large language model
from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider
service_provider = ServiceChatModelProvider()
llm = service_provider.get_chat_model()

# Query Data
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("Who is Neymar?")
print(response)