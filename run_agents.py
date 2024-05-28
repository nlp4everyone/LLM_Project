from llama_index.core.agent import AgentRunner,ReActAgent
from ai_modules.chatmodel_modules import ServiceChatModel,ServiceChatModelProvider
from config import params
# Init index
from ingestion_modules.custom_vectorstore import QdrantService
from llama_index.core.tools import QueryEngineTool,ToolMetadata
# Init embedding model
from ai_modules.embedding_modules import ServiceEmbedding
# from ai_modules.agent_modules import tavily_tool,open_weather_tool
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from callbacks_modules import TokenCounter,LangFuseTracer
import asyncio

# Define embedding model
embedding_service = ServiceEmbedding(model_name=params.embedding_model_name,service_name=params.embedding_service)
embedding_model  = embedding_service.get_embedding_model()

# Setting callbacks
Settings.callback_manager = CallbackManager([TokenCounter.counter,LangFuseTracer.tracer])

# Define chat model
chat_service = ServiceChatModel(service_name=ServiceChatModelProvider.GEMINI)
llm = chat_service.get_chat_model()

# DB Service
qdrant_service = QdrantService()
index = qdrant_service.load_index(embedding_model=embedding_model)

# Define query tool
query_tool = QueryEngineTool(
    query_engine = index.as_query_engine(llm = llm,use_async = True),
    metadata = ToolMetadata(
        description="Useful when ask about Neymar information",
        name="neymar_tool"
    )
)

# Run agent
async def get_response(question : str):
    agent = AgentRunner.from_llm(tools = [query_tool],llm = llm,verbose = True)
    res = await agent.achat(question)
    return res

# Get answer
asyncio.run(get_response("Who is Neymar?"))

# TokenCounter.print_properties()