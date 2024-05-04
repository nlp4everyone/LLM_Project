from llama_index.core.llms import ChatMessage
from typing import Optional
from system_component.system_logging import Logger

class BaseChatModel():
    def __init__(self,temperature: float = 0.8,max_tokens :int = 512):
        # Default params
        self.temperature = temperature
        self.max_tokens = max_tokens
        # Define history
        self.history = []

        # Default model
        self._chat_model = None

    def _chat_template(self,system_prompt:str,user_prompt:str):
        # Define chat template for chat
        return [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role = "user",content = user_prompt),
        ]

    def get_chat_model(self):
        # Return chat model
        return self._chat_model

    def chat(self,user_prompt:str,system_prompt: str = "",streaming:bool = False) :
        # Check state
        if self._chat_model == None:
            exception_message = "Chat model cannot be None"
            # Print exception
            Logger.exception(exception_message)
            raise Exception(exception_message)

        # Get chat template
        chat_template = self._chat_template(system_prompt,user_prompt)
        # Add to history
        self.history.extend(chat_template)

        # Get response ( Specify streaming mode)
        res = self._chat_model.chat(self.history) if not streaming else self._chat_model.stream_chat(self.history)
        # Add answer to history
        self.history.extend(ChatMessage(role="assistant", content=res))
        return res

    async def achat(self, user_prompt: str, system_prompt: Optional[str] = "", streaming:bool = False):
        # Check state
        if self._chat_model == None:
            exception_message = "Chat model cannot be None"
            # Print exception
            Logger.exception(exception_message)
            raise Exception("Chat model cannot be None")

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