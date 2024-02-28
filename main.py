from components.ingestion_pipeline.local_pipeline import LocalIngestion
from components.loader.web_loader import WebLoader
from components.retrieval.custom_retrieval import BaseRetrieval,CustomRetrieval
import time
urls = ["https://en.wikipedia.org/wiki/Data_science"]

# Define documents
documents = WebLoader().load_documents(urls)

# Define ingestion
ingestion = LocalIngestion()
nodes = ingestion.run(documents)

# Query
query = "What is Data Science"
base_retrieval = BaseRetrieval(nodes=nodes)
refs = base_retrieval.synthesize(query)
print(refs)
# for (i,ref) in enumerate(refs):
#     print(f"Index: {i}")
#     print(ref.text)
#     print("\n")

# custom_retrieval = CustomRetrieval(nodes=nodes)
# ingestion.save_local_pipeline()

# print(len(data[0].embedding))
# print("\n")
