from config.params import *
from typing import Union
# from llama_index.llms.gradient import GradientBaseModelLLM
from strenum import StrEnum
from ai_modules.chatmodel_modules import BaseChatModel
from system_component import Logger

class ServiceChatModelProvider(StrEnum):
    ANTHROPIC = "ANTHROPIC",
    COHERE = "COHERE",
    GRADIENT = "GRADIENT",
    GROQ = "GROQ",
    LLAMAAPI = "LLAMAAPI",
    OPENAI = "OPENAI",
    PERPLEXITY = "PERPLEXITY",
    TOGETHER = "TOGETHER",
    GEMINI = "GEMINI"

class ServiceChatModel(BaseChatModel):
    def __init__(self,model_name: str = "default",service_name: Union[ServiceChatModelProvider,str] = ServiceChatModelProvider.GEMINI,temperature: float = 0.8,max_tokens :int = 512):
        super().__init__(temperature = temperature,max_tokens = max_tokens)

        # Service support
        self.list_services = list(supported_services.keys())
        # Check service available
        if service_name not in self.list_services:
            service_exception = f"Service {service_name} is not supported!"
            Logger.exception(service_exception)
            raise Exception(service_exception)

        # Define key
        self.api_key = supported_services[service_name]["KEY"]

        # Default model
        self._chat_model = None
        self._model_name = model_name

        # Other service
        if service_name == "ANTHROPIC":
            # Install dependency
            from llama_index.llms.anthropic import Anthropic
            self._chat_model = Anthropic(api_key=self.api_key,max_tokens=self.max_tokens,temperature=self.temperature)

        elif service_name == "COHERE":
            # Install dependency
            from llama_index.llms.cohere import Cohere
            self._chat_model = Cohere(api_key=self.api_key,max_tokens=self.max_tokens,temperature=self.temperature)

        elif service_name == "GRADIENT":
            raise Exception("Temporally not working")
            # self._chat_model = GradientBaseModelLLM(max_tokens=400,access_token=self.api_key,workspace_id="e27efd0c-635f-4113-bee6-80fec5b3aacd_workspace")

        elif service_name == "GROQ":
            # Install dependency
            from llama_index.llms.groq import Groq
            default_model = "llama3-8b-8192"
            self._chat_model = Groq(model=default_model,api_key=self.api_key)

        elif service_name == "LLAMAAPI":
            # Install dependency
            from llama_index.llms.llama_api import LlamaAPI
            self._chat_model = LlamaAPI(temperature=self.temperature,max_tokens=self.max_tokens,api_key=self.api_key)

        elif service_name == "OPENAI":
            # Install dependency
            from llama_index.llms.openai import OpenAI
            self._chat_model = OpenAI(temperature=self.temperature,max_tokens=self.max_tokens,api_key=self.api_key,timeout=15)

        elif service_name == "PERPLEXITY":
            # Install dependency
            from llama_index.llms.perplexity import Perplexity
            self._chat_model = Perplexity(temperature=self.temperature,max_tokens=self.max_tokens,api_key=self.api_key)

        elif service_name == "TOGETHER":
            # Install dependency
            from llama_index.llms.together import TogetherLLM
            self._chat_model = TogetherLLM(api_key=self.api_key)

        elif service_name == "GEMINI":
            # Install dependency
            from llama_index.llms.gemini import Gemini
            self._chat_model = Gemini(api_key=self.api_key,temperature=self.temperature,max_tokens=self.max_tokens)
        else:
            raise Exception(f"Service {service_name} is not supported!")


        # Print message
        Logger.info(f"Launch {service_name} Chat model with temperature {self.temperature}")
