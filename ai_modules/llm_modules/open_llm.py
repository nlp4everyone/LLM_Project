from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

class OllamaChatModel():
    def __init__(self,model_name="zephyr"):
        self.model_name = model_name
        self.history = []
        try:
            self.chat_model = Ollama(model=self.model_name)
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

    def chat(self,system_prompt="",user_prompt=str,stream=False):
        # Define current message
        current_message = self._default_prompt(system_prompt,user_prompt)
        # Add message to history
        self.history.extend(current_message)
        # Stream mode
        res = self.chat_model.chat(self.history) if stream is False else self.chat_model.stream_chat(self.history)
        return res



