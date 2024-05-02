from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModelProvider,ServiceChatModel
from ingestion_modules.custom_storing.simple_storing import SimpleStoring
from ingestion_modules.custom_storing.service_storing import Qdrant_Storing,QdrantMode
from ai_modules.embedding_modules.open_embedding import OpenEmbedding,OpenEmbeddingProvider
# Instanate embeddung
open_embedding = OpenEmbedding(service_name=OpenEmbeddingProvider.FastEmbed)
embedding_model = open_embedding.get_embedding_model()

qdrant_storing = Qdrant_Storing(mode=QdrantMode.LOCALHOST)
index = qdrant_storing.load_index(embedding_model=embedding_model)
# Build index
# simple_storing = SimpleStoring()
# index = simple_storing.load_index(embedding_model)

# Define large language model
service_provider = ServiceChatModel()
llm = service_provider.get_chat_model()

# Query Data
query_engine = index.as_query_engine(llm=llm,streaming=True,verbose=True)
response = query_engine.query("Who is Neymar?")
print(response)