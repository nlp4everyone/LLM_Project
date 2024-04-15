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
KONKO_KEY = os.getenv("KONKO_KEY") # 5$ starter bundle
LLAMAAPI_KEY = os.getenv("LLAMAAPI_KEY") # 5$ starter bundle
OPENAI_KEY = os.getenv("OPENAI_KEY") # 5$ starter bundle
PERPLEXITY_KEY = os.getenv("PERPLEXITY_KEY") # Required payment
TOGETHER_KEY = os.getenv("TOGETHER_KEY") # 25$ starter bundle
GEMINI_KEY = os.getenv("GEMINI_KEY") # Free to use

# Define service
supported_services = {
    "AI21":{
        "MODELS":[],
        "KEY" : AI21_KEY
    },
    "ANTHROPIC_KEY":{
        "MODELS":["claude-3-opus-20240229","claude-3-sonnet-20240229","claude-3-haiku-20240307"],
        "KEY": ANTHROPIC_KEY
        # List models: https://docs.anthropic.com/claude/docs/models-overview
    },
    "CLARIFAI_KEY":{
        "MODELS":[],
        "KEY": CLARIFAI_KEY
    },
    "COHERE_KEY":{
        "MODELS":["command-light","command","command-r","command-r-plus"],
        "KEY": COHERE_KEY
        # List models: https://docs.cohere.com/docs/command-beta
    },
    "GRADIENT_KEY":{
        "MODELS":[],
        "KEY": GRADIENT_KEY
    },
    "GROQ_KEY":{
        "MODELS":["llama2-70b-4096","mixtral-8x7b-32768","gemma-7b-it"],
        "KEY": GROQ_KEY
    },

    "KONKO_KEY":{
        "MODELS":["meta-llama/llama-2-13b-chat","mistralai/mixtral-8x7b-instruct-v0.1","zero-one-ai/yi-34b-chat"],
        "KEY": KONKO_KEY
        # List model: https://docs.konko.ai/docs/list-of-models
    },
    "LLAMAAPI_KEY":{
        "MODELS":[],
        "KEY": LLAMAAPI_KEY
    },
    "OPENAI_KEY":{
        "MODELS":["gpt-4-turbo-2024-04-09","gpt-4-0125-preview","gpt-4-32k","gpt-4","gpt-3.5-turbo-0125","gpt-3.5-turbo-instruct"],
        "KEY": OPENAI_KEY
        # List model: https://platform.openai.com/docs/models/continuous-model-upgrades
    },
    "PERPLEXITY_KEY":{
        "MODELS":["llama-2-13b-chat","llama-2-70b-chat","mistral-7b-instruct","pplx-7b-chat-alpha","pplx-70b-chat-alpha"],
        "KEY": PERPLEXITY_KEY
        # List model: https://docs.perplexity.ai/docs/model-cards
    },
    "TOGETHER_KEY":{
        "MODELS":["zero-one-ai/Yi-34B-Chat","cognitivecomputations/dolphin-2.5-mixtral-8x7b","mistralai/Mistral-7B-Instruct-v0.2","NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO","Qwen/Qwen1.5-32B-Chat"],
        "KEY": TOGETHER_KEY
        # List model: https://docs.together.ai/docs/inference-models
    },
    "GEMINI_KEY":{
        "MODELS":["models/gemini-1.5-pro-latest","models/gemini-pro","models/gemini-pro-vision"],
        "KEY": GEMINI_KEY
        # List model: https://ai.google.dev/models/gemini
        # Gemini Pro 60 requests/min
    }
}