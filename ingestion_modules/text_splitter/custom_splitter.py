from semantic_text_splitter import TextSplitter
from typing import Union,List,Tuple
from enum import Enum
from tokenizers import Tokenizer

# Reference (https://pypi.org/project/semantic-text-splitter/)
class Splitter_Type(Enum):
    CHARACTER_MODE = 0,
    TIKTOKEN_MODE = 1,
    HUGGINGFACE_MODE = 2

class AdvanceTextSplitter():
    def __init__(self,splitter_mode = Splitter_Type.CHARACTER_MODE):
        # Base mode
        self.splitter = TextSplitter()
        if splitter_mode == Splitter_Type.HUGGINGFACE_MODE:
            tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
            self.splitter = TextSplitter.from_huggingface_tokenizer(tokenizer)
        elif splitter_mode == Splitter_Type.TIKTOKEN_MODE:
            self.splitter = TextSplitter.from_tiktoken_model("gpt-3.5-turbo")

    def from_text(self,input:Union[str,List[str]], max_characters : Union[int,Tuple[int]]= (100,1000)):
        if not type(input) == str:
            raise Exception("Please insert list of string")
        return self.splitter.chunks(input,max_characters)