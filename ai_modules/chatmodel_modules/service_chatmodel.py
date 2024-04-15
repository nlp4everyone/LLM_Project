from config.params import *
from typing import Union,Literal
from ai_modules.chatmodel_modules.open_chatmodel import OllamaChatModel
from llama_index.llms.cohere import Cohere
from llama_index.llms.ai21 import AI21
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.gradient import GradientBaseModelLLM
from llama_index.llms.groq import Groq
from llama_index.llms.konko import Konko
from llama_index.llms.llama_api import LlamaAPI
from llama_index.llms.openai import OpenAI
from llama_index.llms.perplexity import Perplexity
from llama_index.llms.together import TogetherLLM
from llama_index.llms.gemini import Gemini

class ServiceChatModel(OllamaChatModel):
    def __init__(self,model_name: Union[str,None] = None,service_name: str = "AI21",temperature: float = 0.8,max_tokens :int = 512):
        super().__init__()
        # Define variales
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Define history
        self.history = []
        #
        # Service support
        self.list_services = list(supported_services.keys())
        # Check service available
        if service_name not in self.list_services: raise Exception(f"Service {service_name} is not supported!")

        # Define key
        self.api_key = supported_services[service_name]["KEY"]

        # Default model
        self._chat_model = AI21(api_key=self.api_key,maxTokens=self.max_tokens,temperature=self.temperature)

        # Other service
        if service_name == "ANTHROPIC":
            self._chat_model = Anthropic(api_key=self.api_key,max_tokens=self.max_tokens,temperature=self.temperature)
        elif service_name == "COHERE":
            self._chat_model = Cohere(api_key=self.api_key,max_tokens=self.max_tokens,temperature=self.temperature)
        elif service_name == "GRADIENT":
            self._chat_model = GradientBaseModelLLM(max_tokens=400,access_token=self.api_key,workspace_id="e27efd0c-635f-4113-bee6-80fec5b3aacd_workspace")
        elif service_name == "GROQ":
            self._chat_model = Groq(api_key=self.api_key)
        elif service_name == "KONKO":
            self._chat_model = Konko(temperature=self.temperature,max_tokens=self.max_tokens,konko_api_key=KONKO_KEY)
        elif service_name == "LLAMAAPI":
            self._chat_model = LlamaAPI(temperature=self.temperature,max_tokens=self.max_tokens,api_key=self.api_key)
        elif service_name == "OPENAI":
            self._chat_model = OpenAI(temperature=self.temperature,max_tokens=self.max_tokens,api_key=self.api_key)
        elif service_name == "PERPLEXITY":
            self._chat_model = Perplexity(temperature=self.temperature,max_tokens=self.max_tokens,api_key=self.api_key)
        elif service_name == "TOGETHER":
            self._chat_model = TogetherLLM(api_key=self.api_key)
        elif service_name == "GEMINI":
            self._chat_model = Gemini(api_key=self.api_key,temperature=self.temperature,max_tokens=self.max_tokens)