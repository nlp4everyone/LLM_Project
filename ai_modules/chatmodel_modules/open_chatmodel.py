from llama_index.llms.ollama import Ollama
from typing import Union
from ai_modules.chatmodel_modules.base_chatmodel import BaseChatModel


class OpenChatModel(BaseChatModel):
    def __init__(self, model_name: Union[str, None] = "zephyr",temperature: float = 0.8,max_tokens :int = 512):
        super().__init__(temperature = temperature,max_tokens = max_tokens)
        # Set model
        self._model_name = model_name
        self._chat_model = Ollama(model=self._model_name, temperature=self.temperature)

        print(f"Launch Chat Model with temperature {self.temperature}")