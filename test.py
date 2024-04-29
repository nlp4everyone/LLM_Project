from ai_modules.embedding_modules.service_embedding import ServiceEmbedding

open_embedding = ServiceEmbedding(service_name="NOMIC")
embedding = open_embedding.get_text_embedding("Hello")
print(embedding)


