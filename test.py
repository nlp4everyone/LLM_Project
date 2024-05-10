from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from ingestion_modules.custom_vectorstore.qdrant_service import QdrantService

client = QdrantClient("http://localhost:6060")



# client.create_collection(
#     collection_name="{huantest1}",
#     vectors_config=models.VectorParams(size=100, distance=models.Distance.COSINE),
# )
qdrant_service = QdrantService(mode="local")

vector_store = QdrantVectorStore(client=client, collection_name="huantest2")



collection = client.get_collections()

collection_name = [collection.collections[i].name for i in range(len(collection.collections))]
print(collection_name)