from dotenv import load_dotenv
import os
load_dotenv()
cache_folder = "local_cache"

# Model config
AI21_KEY = os.getenv("AI21_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY") # Max usage 10$
CLARIFAI_KEY = os.getenv("CLARIFAI_KEY")
COHERE_KEY = os.getenv("COHERE_KEY") # Cohere limited calls per minutes
GRADIENT_KEY = os.getenv("GRADIENT_KEY") # Cohere limited calls per minutes
GROQ_KEY = os.getenv("GROQ_KEY") # 30 requests/min

# Define service
supported_services = {
    "AI21":{
        "MODELS":[],
        "KEY" : AI21_KEY
    },
    "ANTHROPIC_KEY":{
        "MODELS":["claude-3-opus-20240229","claude-3-sonnet-20240229","claude-3-haiku-20240307"],
        "KEY": ANTHROPIC_KEY
    },
    "CLARIFAI_KEY":{
        "MODELS":[],
        "KEY": CLARIFAI_KEY
    },
    "COHERE_KEY":{
        "MODELS":["command-light","command","command-r","command-r-plus"],
        "KEY": COHERE_KEY
    },
    "GRADIENT_KEY":{
        "MODELS":[],
        "KEY": GRADIENT_KEY
    },
    "GROQ_KEY":{
        "MODELS":["llama2-70b-4096","mixtral-8x7b-32768","gemma-7b-it"],
        "KEY": GROQ_KEY
    }
}