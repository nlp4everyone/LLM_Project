from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent


# define sample Tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and returns the result integer"""
    return a * b


multiply_tool = FunctionTool.from_defaults(fn=multiply)

# initialize llm
llm = Ollama(model="zephyr")
# initialize ReAct agent
agent = ReActAgent.from_tools([multiply_tool], llm=llm, verbose=True)
output =  agent.query("1 multiple 2")
print(output)