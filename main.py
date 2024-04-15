from ingestion_modules.ingestion_pipeline import LocalIngestion
from ingestion_modules.custom_loader.web_loader import WebLoader
# from ai_modules.retrieval_modules.custom_retrieval import BaseRetrieval

urls = ["https://en.wikipedia.org/wiki/Data_science"]

# Define documents
documents = WebLoader().load_documents(urls)

# Define ingestion
ingestion = LocalIngestion()
nodes = ingestion.run(documents)
print(len(nodes))
print(nodes[0].text)

# Query
# query = "What is Data Science"
# base_retrieval = BaseRetrieval(nodes=nodes)

