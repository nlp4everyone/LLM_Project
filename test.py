from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent, AgentRunner
from ai_modules.chatmodel_modules import ServiceChatModel
from ingestion_modules.custom_vectorstore import QdrantService

qdrant_service = QdrantService()
index = qdrant_service.load_index()

# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

def add(a: int, b: int) -> int:
    """add two integers and returns the result integer"""
    return a + b

multiply_tool = FunctionTool.from_defaults(fn=multiply)
chat_service = ServiceChatModel()
llm = chat_service.get_chat_model()

# # initialize llm
# llm = OpenAI(model="gpt-3.5-turbo-0613")

# initialize ReAct agent
agent = AgentRunner.from_llm([multiply_tool], llm=llm, verbose=True)

res = agent.chat("What is 2330 * 215123")
print(res)

# res = chat_model.chat("What is 2123 * 215123")
# print(res)