from dotenv import load_dotenv
import os
load_dotenv()

# Elastic Search
TAVILY_API = os.getenv("TAVILY_API")
EXA_API = os.getenv("OPENWEATHER_API")
OPENWEATHER_API = os.getenv("OPENWEATHER_API")