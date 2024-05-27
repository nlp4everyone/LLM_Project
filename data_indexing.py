import os
from llama_index.core.ingestion import IngestionPipeline
from ingestion_modules.custom_loader import CustomWebLoader,CustomPDFReader,WebProvider
from llama_index.core.text_splitter import SentenceSplitter
from ingestion_modules import utils
# from ai_modules.embedding_modules import OpenEmbedding,OpenEmbeddingProvider
from ai_modules.embedding_modules import ServiceEmbedding
from ingestion_modules.custom_vectorstore import QdrantService,_QDRANT_COLLECTION
from config import params
from llama_index.core import Document,Settings
# from system_component.system_logging import Logger
from llama_index.core.extractors import TitleExtractor,QuestionsAnsweredExtractor,KeywordExtractor,SummaryExtractor,PydanticProgramExtractor
from llama_index.extractors.entity import EntityExtractor
from ai_modules.chatmodel_modules import ServiceChatModel,ServiceChatModelProvider
import time

# Init embedding
# open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
# embedding_model = open_embedding.get_embedding_model()
service_embedding = ServiceEmbedding(service_name=params.embedding_service, model_name=params.embedding_model_name)
embedding_model = service_embedding.get_embedding_model()

# Define chat model
chat_service = ServiceChatModel(service_name=ServiceChatModelProvider.GROQ)
llm = chat_service.get_chat_model()

Settings.llm = llm
# Init vector stor service
qdrant_service = QdrantService(mode="local")

# Web url for crawling
web_url = "https://en.wikipedia.org/wiki/Neymar"


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

def preprocess(docs: list[Document],pipeline):
    # Check state
    if docs == None:
        raise Exception("Document cant be None")

    # Run through pipeline
    nodes = pipeline.run(documents=docs)
    return nodes

def insert_all_to_database(nodes,embedding_model):

    # Convert nodes to docs
    # docs = utils.convert_nodes_to_docs(nodes)

    # Build index
    index = qdrant_service.build_index_from_docs(documents=nodes, embedding_model=embedding_model)

def main():
    # Default pipeline
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=800, chunk_overlap=100),
            TitleExtractor(), # Extract document_title metadata
            # QuestionsAnsweredExtractor(questions=3,num_workers=4)
            # SummaryExtractor(num_workers=4)
            #KeywordExtractor(keywords=3,num_workers=16)
            # EntityExtractor(device="cuda") # Extract entity with BERT model
        ],
    )

    # Get documents from url
    docs = load_documents(url=web_url)
    # Get nodes
    nodes = preprocess(docs=docs,pipeline=pipeline)

    # Insert to database
    insert_all_to_database(nodes=nodes,embedding_model=embedding_model)

if __name__ == "__main__":
    beginTime = time.time()
    main()
    endTime = time.time() - beginTime
    print(f"Process in {round(endTime,3)}s")
