import os
from ai_modules.embedding_modules import open_embedding
from ingestion_modules.custom_loader.pdf_loader import BasePDFReader
from llama_index.core.node_parser import TokenTextSplitter,SentenceSplitter,SemanticSplitterNodeParser
from ai_modules.llm_modules.open_llm import OllamaChatModel
from llama_index.core import VectorStoreIndex
from ai_modules.retrieval_modules import custom_retrieval
from config import params

# Cached folder
os.makedirs(params.cache_folder,exist_ok=True)

# LLM
open_model = OllamaChatModel(temperature=0)
llm = open_model.get_chat_model()

# Embedding model
embedding_model = open_embedding.HFEmbedding.get_embedding_model()

pdf_reader = BasePDFReader()
documents = pdf_reader.read("reference/Loot.pdf")
# print("Before chunking")
# print(f"Total text: {len(documents)}")
# for (i,doc) in enumerate(documents):
#     if i < 20:
#         print(f"Document {i}")
#         print(doc.text)
#         print(len(doc.text))

# print("\n")
# print("After chunking")

# Splitting text
# splitter = SentenceSplitter(chunk_size=1000,chunk_overlap=200)
splitter = SemanticSplitterNodeParser(embed_model=embedding_model)
nodes = splitter.get_nodes_from_documents(documents)
print(f"Number of nodes: {len(nodes)}")
for (i,doc) in enumerate(nodes):
    if i < 2:
        print(f"Document {i}")
        print(doc.text)
        print(doc.metadata)
        print(doc.node_id)

# Retrieve phase
query_engine = custom_retrieval.BaseRetrieval(nodes=nodes,embedding_model=embedding_model,llm=llm)
question = "Revenue sharing of LootBot?"
# results = query_engine.retrieve(question)
# for (i,result) in enumerate(results):
#     print(f"Retrieval document {i}")
#     print(result.text)
#     print("\n")

# Query phase
print("\n")
output = query_engine.query(question)
print("Output")
print(output)

# # vector store
# indexes = VectorStoreIndex(nodes=nodes,embed_model=embedding_model)
# query_engine = indexes.as_query_engine(llm=llm)
# answer = query_engine.query("What is Loot?")
# print(answer)
# print(f"Total chunk {len(chunkers)}")
# for (i,chunk) in enumerate(chunkers):
#     if i < 10:
#         print(f"Chunk {i}")
#         print(chunk.text)
#         print("\n")