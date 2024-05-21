# Init tool
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.tools.exa import ExaToolSpec
from llama_index.tools.weather import OpenWeatherMapToolSpec
from config import tool_params
from llama_index.core.tools import FunctionTool
from pydantic import Field

# # Define Exa Search Tool
# exa_tool = ExaToolSpec(
#     api_key=tool_params.EXA_API,
# )
# # Define OpenWeather Tool
# weather_tool = OpenWeatherMapToolSpec(
#     key=tool_params.OPENWEATHER_API
# )

# Define function
def tavily_search(query: str, max_results :int = 10):
    # Define Tavily Search Tool
    tavily_spec = TavilyToolSpec(api_key=tool_params.TAVILY_API)
    results = tavily_spec.search(query = query,max_results=max_results)
    return results

def open_weather_search(location: str):
    # Define Tavily Search Tool
    open_weather_spec = OpenWeatherMapToolSpec(key=tool_params.OPENWEATHER_API)
    results = open_weather_spec.weather_at_location(location=location)
    return results

# Define tool
tavily_tool = FunctionTool.from_defaults(
    fn = tavily_search,
    name="search_tool",
    description="Useful when ask about general question"
)

open_weather_tool = FunctionTool.from_defaults(
    fn= open_weather_search,
    name="weather_tool",
    description="Useful when ask about weather of specific location"
)