from langfuse.llama_index import LlamaIndexCallbackHandler
from config import service_params


class LangFuseTracer(LlamaIndexCallbackHandler):
    # Define params
    _langfuse_public_key = service_params.LANGFUSE_PUBLIC_KEY
    _langfuse_secret_key = service_params.LANGFUSE_SECRET_KEY
    _langfuse_host = service_params.LANGFUSE_HOST

    # Define handler
    tracer = LlamaIndexCallbackHandler(
        public_key=_langfuse_public_key,
        secret_key=_langfuse_secret_key,
        host=_langfuse_host
    )