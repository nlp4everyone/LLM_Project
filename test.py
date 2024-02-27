from components.ingestion_pipeline.local_pipeline import LocalIngestion
from components.loader.web_loader import WebLoader
urls = ["https://en.wikipedia.org/wiki/Data_science"]

# Define documents
documents = WebLoader().load_documents(urls)

# Define ingestion
ingestion = LocalIngestion()
# data = ingestion.run(documents)
# ingestion.save_local_pipeline()
data = ingestion.load_local_pipeline()
print(data)

# print(len(data[0].embedding))
# print("\n")
