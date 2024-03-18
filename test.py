from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import BasePromptTemplate
chat_model = Ollama(model="zephyr").stream()