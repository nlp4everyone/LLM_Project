from llama_index.callbacks.wandb import WandbCallbackHandler
# wandb.init args
run_args = dict(
    project="llamaindex",
)

class WandbTracer(WandbCallbackHandler):
    tracer = WandbCallbackHandler(run_args=run_args)