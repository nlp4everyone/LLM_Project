from ai_modules.llm_modules.open_llm import OllamaChatModel
from llama_index.core import VectorStoreIndex

chat_model = OllamaChatModel()
res1 = chat_model.chat(user_prompt="My name is Phong")
print(res1)
res2 = chat_model.chat(user_prompt="What is my name?")
print(res2)
