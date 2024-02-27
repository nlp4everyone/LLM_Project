from llama_index.readers.web import TrafilaturaWebReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core import Settings
from llama_index.embeddings import huggingface
from llama_index.llms.ollama import Ollama
urls = ["https://en.wikipedia.org/wiki/Adolf_Hitler"]
import time


Settings.llm = Ollama(model="zephyr")
# Load data
web_reader = TrafilaturaWebReader()
documents_data = web_reader.load_data(urls)
embedding_model = huggingface.HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
beginTime = time.time()

# Pipeline
pipeline = IngestionPipeline(
    name="rag_pipeline",
    transformations=[
        SentenceSplitter(chunk_size=300,chunk_overlap=50),
        TitleExtractor(),
        embedding_model
    ]
)
# pipeline.persist("./pipeline_storage")
text = pipeline.run(show_progress=True,documents=documents_data)
print(text[0])
print(text[0].embedding)
print(text[0].metadata)
# endTime = time.time() - beginTime
# print(endTime)


