import os.path

from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document,StorageContext,load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import params

# Define variables
embedding_cache_folder = os.path.join(params.cache_folder,"embedding_cache")
storing_cache_folder = os.path.join("./",params.cache_folder,"storing_cache")

# Define transformation
transformations = [
    SentenceSplitter(chunk_size=300,chunk_overlap=100),
    HuggingFaceEmbedding(model_name=params.local_embedding_model,cache_folder=embedding_cache_folder) # Local embedding
]

class LocalIngestion():
    def __init__(self,transformations = transformations,num_of_workers = 10):
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

    def save_local_pipeline(self,storing_cache_folder = storing_cache_folder):
        # Save pipeline to local cache
        self.pipeline.persist(storing_cache_folder)

    def load_local_pipeline(self,storing_cache_folder = storing_cache_folder):
        storage_context = StorageContext.from_defaults(persist_dir=storing_cache_folder)
        print(storage_context)
        # return load_index_from_storage(storage_context)