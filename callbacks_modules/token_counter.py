import tiktoken
from llama_index.core.callbacks import TokenCountingHandler

# Used for counting token from prompt
class TokenCounter(TokenCountingHandler):
    counter = TokenCountingHandler(
        tokenizer=tiktoken.encoding_for_model("gpt-4").encode
    )
    @staticmethod
    def print_properties():
        print("Embedding Tokens: ",TokenCounter.counter.total_embedding_token_count,"\n",
              "LLM Prompt Tokens: ",TokenCounter.counter.prompt_llm_token_count,"\n",
              "LLM Completion Tokens: ",TokenCounter.counter.completion_llm_token_count,"\n",
              "Total LLM Token Count: ",TokenCounter.counter.total_llm_token_count,"\n",)

