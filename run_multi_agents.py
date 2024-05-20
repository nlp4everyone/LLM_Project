from llama_index.core.agent import AgentRunner,ReActAgent
from ai_modules.chatmodel_modules import ServiceChatModel,ServiceChatModelProvider
from config import tool_params
# Init tool
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.tools.exa import ExaToolSpec
from llama_index.tools.weather import OpenWeatherMapToolSpec

# Define Tavily Search Tool
tavily_tool = TavilyToolSpec(
    api_key=tool_params.TAVILY_API,
)
# Define Exa Search Tool
exa_tool = ExaToolSpec(
    api_key=tool_params.EXA_API,
)
# Define OpenWeather Tool
tool_spec = OpenWeatherMapToolSpec(
    key=tool_params.OPENWEATHER_API
)

# Define chat model
chat_service = ServiceChatModel(service_name=ServiceChatModelProvider.GEMINI)
llm = chat_service.get_chat_model()

# Run agent
agent = AgentRunner.from_llm(tools=tool_spec.to_tool_list(),llm=llm,verbose=True)
res = agent.chat("Weather in Hanoi")
print(res)