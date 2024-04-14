from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage
from typing import Union


class OllamaChatModel():
    def __init__(self,model_name: Union[str,None] = "zephyr",temperature: float = 0.8,max_tokens :int = 512):
        # Define variales
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model_name = model_name

        # Define history
        self.history = []

        # Define chat model
        self.chat_model = Ollama(model=self.model_name,temperature=self.temperature)

    def _chat_template(self,system_prompt:str,user_prompt:str):
        # Define chat template for chat
        return [
            ChatMessage(role = "assistant",content = system_prompt),
            ChatMessage(role="user", content=user_prompt),
        ]

    def chat(self,system_prompt:str,user_prompt:str,streaming:bool = False):
        # Get chat template
        chat_template = self._chat_template(system_prompt,user_prompt)
        # Extend history
        self.history.extend(chat_template)

        # Get response ( Specify streaming mode)
        res = self.chat_model.chat(self.history) if not streaming else self.chat_model.stream_chat(self.history)
        return res

    async def achat(self, system_prompt: str, user_prompt: str,streaming:bool = False):
        # Get chat template
        chat_template = self._chat_template(system_prompt, user_prompt,)
        # Extend history
        self.history.extend(chat_template)

        # Get response ( Specify streaming mode)
        if not streaming:
            res = await self.chat_model.achat(self.history)
        else:
            res = await self.chat_model.astream_chat(self.history)
        return res


