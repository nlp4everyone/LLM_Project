import os
from llama_index.core.ingestion import IngestionPipeline
from ingestion_modules.custom_loader import CustomWebLoader,CustomPDFReader,WebProvider
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
from ai_modules.embedding_modules import OpenEmbedding,OpenEmbeddingProvider
# from ai_modules.chatmodel_modules import ServiceChatModelProvider,ServiceChatModel
from ai_modules.embedding_modules import ServiceEmbedding
from ingestion_modules.custom_vectorstore import QdrantService,_QDRANT_COLLECTION
from system_component.system_logging import Logger

# Init embedding
# open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
# embedding_model = open_embedding.get_embedding_model()
service_embedding = ServiceEmbedding(service_name="COHERE",model_name="embed-english-light-v3.0")
embedding_model = service_embedding.get_embedding_model()

# Init vector stor service
qdrant_service = QdrantService(mode="local")

# Define large language model
# service_provider = ServiceChatModel()
# llm = service_provider.get_chat_model()

# Web url for crawling
web_url = "https://en.wikipedia.org/wiki/Neymar"

# Default pipeline
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)

def load_documents(url:str):
    # Validating input params
    assert url, "Url cant be empty"
    # Check url

    docs = None
    # When url is a file
    if os.path.isfile(url):
        # Get the extension
        ext = os.path.splitext(url)[1]
        # If extension is PDF
        if str(ext).lower() == ".pdf":
            loader = CustomPDFReader(pdf_provider="LlamaParse")
            docs = loader.load_data(file_path=url)
        else:
            raise Exception(f"File format {ext} is not supported!")
    # When url is a link
    else:
        try:
            loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
            docs = loader.load_data(url)
        except Exception as e:
            print(e)
    return docs

def insert_all_to_database(url:str =web_url,pipeline = pipeline):
    # Get documents
    docs = load_documents(url=url)
    # Check state
    if docs == None:
        raise Exception("Document cant be None")

    # Run through pipeline
    nodes = pipeline.run(documents=docs)
    # Convert nodes to docs
    docs = utils.convert_nodes_to_docs(nodes)

    # Build index
    index = qdrant_service.build_index_from_docs(documents=docs, embedding_model=embedding_model,mode="override")

# # Inspecting time indexing
# beginTime = time.time()
# insert_all_to_database(url=web_url)
# endTime = time.time() - beginTime
# Logger.info(f"Indexing time {round(endTime,2)}s")