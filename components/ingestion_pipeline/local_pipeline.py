import os.path
from llama_index.core.ingestion import IngestionPipeline,IngestionCache
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document,StorageContext,load_index_from_storage
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client
from config import params
from components import local_models

# Define variables
embedding_cache_folder = os.path.join(params.cache_folder,"embedding_cache")
storing_cache_folder = os.path.join("./",params.cache_folder,"storing_cache")

# Define transformation
local_transformations = [
    SentenceSplitter(chunk_size=300,chunk_overlap=100),
    local_models.local_embedding
]


class LocalIngestion():
    def __init__(self,transformations = local_transformations,num_of_workers = 4):
        # Define variable
        self._transformations = transformations
        self.num_of_workers = num_of_workers
        # Define pipeline
        self.pipeline = IngestionPipeline(
            transformations = self._transformations
        )

    def run(self,document:Document):
        # Return run
        if not isinstance(document,list):
            raise Exception("Please input list of Document")
        return self.pipeline.run(documents=document)

    async def arun(self,document:Document):
        # Return run
        if not isinstance(document,list):
            raise Exception("Please input list of Document")
        nodes = await self.pipeline.arun(documents=document)
        return nodes

    def save_local_pipeline(self,storing_cache_folder = storing_cache_folder):
        # Save pipeline to local cache
        self.pipeline.persist(storing_cache_folder)

    def load_local_pipeline(self,storing_cache_folder = storing_cache_folder):
        return  self.pipeline.load(storing_cache_folder)
        # storage_context = StorageContext.from_defaults(vector_store=vector_store,persist_dir=storing_cache_folder)
        # return load_index_from_storage(storage_context)