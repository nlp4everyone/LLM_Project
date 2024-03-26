from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

class OllamaChatModel():
    def __init__(self,model_name: str ="zephyr",temperature: float = 0.5):
        self.model_name = model_name
        self.temperature = temperature
        self.history = []
        try:
            self.chat_model = Ollama(model=self.model_name,temperature=self.temperature)
        except:
            raise Exception("Cannot init chat model")

    def _default_prompt(self,system_prompt,user_prompt):
        messages = [
            ChatMessage(
                role="system", content=system_prompt
            ),
            ChatMessage(role="user", content=user_prompt),
        ]
        return messages

    def get_chat_model(self):
        return self.chat_model

    def chat(self,system_prompt="",user_prompt=str,stream=False):
        # Define current message
        current_message = self._default_prompt(system_prompt,user_prompt)
        # Add message to history
        self.history.extend(current_message)
        # Stream mode
        res = self.chat_model.chat(self.history) if stream is False else self.chat_model.stream_chat(self.history)
        return res



