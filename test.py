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
import torch

