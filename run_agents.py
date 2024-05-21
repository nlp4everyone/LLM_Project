from llama_index.core.agent import AgentRunner,ReActAgent
from ai_modules.chatmodel_modules import ServiceChatModel,ServiceChatModelProvider
from config import params
# Init index
from ingestion_modules.custom_vectorstore import QdrantService
from llama_index.core.tools import QueryEngineTool,ToolMetadata
# Init embedding model
from ai_modules.embedding_modules import ServiceEmbedding
from ai_modules.agent_modules import tavily_tool,open_weather_tool
from llama_index.core import Settings
from llama_index.core.callbacks import CallbackManager
from callbacks_modules import TokenCounter,LangFuseTracer

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
    query_engine = index.as_query_engine(llm=llm),
    metadata = ToolMetadata(
        description="Useful when ask about Neymar information",
        name="neymar_tool"
    )
)

# Run agent
agent = AgentRunner.from_llm(tools=[tavily_tool,query_tool,open_weather_tool],llm=llm,verbose=True)
res = agent.chat("Who is Neymar?")

TokenCounter.print_properties()