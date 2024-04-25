from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from typing import Union,Optional


class OpenChatModelProvider():
    def __init__(self,model_name: Union[str,None] = "zephyr",temperature: float = 0.8,max_tokens :int = 512):
        # Define variales
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model_name = model_name

        # Define history
        self.history = []

        # Define chat model
        self._chat_model = None
        # Only for Ollama Chat Model
        if self.__class__.__name__ == "OpenChatModelProvider":
            self._chat_model = Ollama(model=self.model_name,temperature=self.temperature)

    def _chat_template(self,system_prompt:str,user_prompt:str):
        # Define chat template for chat
        return [
            ChatMessage(role = "assistant",content = system_prompt),
            ChatMessage(role="user", content=user_prompt),
        ]

    def get_chat_model(self):
        # Return chat model
        return self._chat_model

    def chat(self,user_prompt:str,system_prompt: Optional[str] = "",streaming:bool = False) :
        # Get chat template
        chat_template = self._chat_template(system_prompt,user_prompt)
        # Extend history
        self.history.extend(chat_template)

        # Get response ( Specify streaming mode)
        res = self._chat_model.chat(self.history) if not streaming else self._chat_model.stream_chat(self.history)
        return res

    async def achat(self, user_prompt: str, system_prompt: Optional[str] = "", streaming:bool = False):
        # Get chat template
        chat_template = self._chat_template(system_prompt, user_prompt,)
        # Extend history
        self.history.extend(chat_template)

        # Get response ( Specify streaming mode)
        if not streaming:
            res = await self._chat_model.achat(self.history)
        else:
            res = await self._chat_model.astream_chat(self.history)
        return res


