# from llama_index.core.tools import FunctionTool
# from llama_index.llms.ollama import Ollama
# from llama_index.core.agent import ReActAgent
#
# # define sample Tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two integers and returns the result integer"""
#     return a * b
#
#
# multiply_tool = FunctionTool.from_defaults(fn=multiply)
#
# # initialize llm
# llm = Ollama(model="zephyr")
# # initialize ReAct agent
# agent = ReActAgent.from_tools([multiply_tool], llm=llm, verbose=True)
# output =  agent.query("1 multiple 2")
# print(output)



# from ai_modules.llm_modules.service_llm import ServiceChatModel
# # from ai_modules.llm_modules.open_llm import OllamaChatModel
# service_llm = ServiceChatModel(model_name="GRADIENT",temperature=0.9)
# res = service_llm.chat(system_prompt="Be a userful chatbot",user_prompt="Who you are?")



#
# response = llm.complete("Explain the importance of low latency LLMs")
# print(response)

# import torch
# from llama_index.core import PromptTemplate
# from llama_index.llms.huggingface import HuggingFaceLLM
# # This will wrap the default prompts that are internal to llama-index
# # taken from https://huggingface.co/Writer/camel-5b-hf
# query_wrapper_prompt = PromptTemplate(
#     "Below is an instruction that describes a task. "
#     "Write a response that appropriately completes the request.\n\n"
#     "### Instruction:\n{query_str}\n\n### Response:"
# )
#
# llm = HuggingFaceLLM(
#     context_window=2048,
#     max_new_tokens=256,
#     generate_kwargs={"temperature": 0.25, "do_sample": False},
#     query_wrapper_prompt=query_wrapper_prompt,
#     tokenizer_name="Writer/camel-5b-hf",
#     model_name="Writer/camel-5b-hf",
#     device_map="auto",
#     tokenizer_kwargs={"max_length": 2048},
#     # uncomment this if using CUDA to reduce memory usage
#     # model_kwargs={"torch_dtype": torch.float16}
# )
# print(dir(llm))

from llama_index.llms.gemini import Gemini
import os

GOOGLE_API_KEY = "AIzaSyASWApYD-MHcEW2FHpEe9FmuW5GsQpWbqY"  # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
resp = Gemini().complete("Write a poem about a magic backpack")
print(resp)