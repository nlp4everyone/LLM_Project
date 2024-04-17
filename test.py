# from llama_index.core.tools import FunctionTool
# from llama_index.llms.ollama import Ollama
# from llama_index.core.agent import ReActAgent
#
# # define sample Tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two integers and returns the result integer"""
#     return a * b
#
#
# multiply_tool = FunctionTool.from_defaults(fn=multiply)
#
# # initialize llm
# llm = Ollama(model="zephyr")
# # initialize ReAct agent
# agent = ReActAgent.from_tools([multiply_tool], llm=llm, verbose=True)
# output =  agent.query("1 multiple 2")
# print(output)
import os

# from ai_modules.llm_modules.service_llm import ServiceChatModel
# # from ai_modules.llm_modules.open_llm import OllamaChatModel
# service_llm = ServiceChatModel(model_name="GRADIENT",temperature=0.9)
# res = service_llm.chat(system_prompt="Be a userful chatbot",user_prompt="Who you are?")



#
# response = llm.complete("Explain the importance of low latency LLMs")
# print(response)

# import torch
# from llama_index.core import PromptTemplate
# from llama_index.llms.huggingface import HuggingFaceLLM
# # This will wrap the default prompts that are internal to llama-index
# # taken from https://huggingface.co/Writer/camel-5b-hf
# query_wrapper_prompt = PromptTemplate(
#     "Below is an instruction that describes a task. "
#     "Write a response that appropriately completes the request.\n\n"
#     "### Instruction:\n{query_str}\n\n### Response:"
# )
#
# llm = HuggingFaceLLM(
#     context_window=2048,
#     max_new_tokens=256,
#     generate_kwargs={"temperature": 0.25, "do_sample": False},
#     query_wrapper_prompt=query_wrapper_prompt,
#     tokenizer_name="Writer/camel-5b-hf",
#     model_name="Writer/camel-5b-hf",
#     device_map="auto",
#     tokenizer_kwargs={"max_length": 2048},
#     # uncomment this if using CUDA to reduce memory usage
#     # model_kwargs={"torch_dtype": torch.float16}
# )
# print(dir(llm))

# from llama_index.core import Document
# doc1 = Document(text="Whales Market is a unique trading platform designed to make swapping assets across different blockchains easy and secure. It tackles the common problem of scams and fraud in peer-to-peer (P2P) cryptocurrency trading of pre-launch tokens and points before TGE.",metadata={"category":"Whales Market","type":"definition"})
# doc2 = Document(text="Current price of Whales is 3$",metadata={"category":"Whales Market","type":"price"})
# doc3 = Document(text="Neymar da Silva Santos Júnior (born 5 February 1992), also known as Neymar Júnior, is a Brazilian professional footballer who plays as a forward for Saudi Pro League club Al Hilal and the Brazil national team",metadata={"category":"Neymar","type":"definition"})
#
# from ai_modules.chatmodel_modules.service_chatmodel import ServiceChatModel
# from config import params
# os.environ["OPENAI_API_KEY"] = params.OPENAI_KEY
# print(params.OPENAI_KEY)
# # service_chatmodel = ServiceChatModel(service_name="GEMINI")
# # chat_model = service_chatmodel.get_chat_model()
# doc = [doc1,doc2,doc3]
# from llama_index.core import VectorStoreIndex
# index = VectorStoreIndex.from_documents(doc)
# query_engine = index.as_query_engine()
# ans = query_engine.query("Who is Neymar?")
# print(ans)

from ingestion_modules.custom_loader.custom_web_loader import CustomWebLoader,WebProvider
# Load data
web_loader = CustomWebLoader(web_provider=WebProvider.TRAFILATURA)
docs = web_loader.load_data("https://en.wikipedia.org/wiki/Neymar")
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_index.core.node_parser import SemanticSplitterNodeParser,SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from ingestion_modules.text_splitter.custom_splitter import SemanticTextSplitter
# embedding = OpenAIEmbedding()
# Ingestion
from llama_index.core.ingestion import IngestionPipeline
# semantic_splitter = SemanticTextSplitter()
# semantic_docs = semantic_splitter.from_documents(docs)
# for (i,doc) in enumerate(semantic_docs):
#     print(f"Document {i}:")
#     if i < 5: print(doc)

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1000, chunk_overlap=200),
    ],
)
docs = pipeline.run(documents=docs)



