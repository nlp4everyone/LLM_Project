from llama_index.core.callbacks import LlamaDebugHandler

# Used for tracing log of LLM
class LlamaDebug(LlamaDebugHandler):
    debugger = LlamaDebugHandler(print_trace_on_end=True)