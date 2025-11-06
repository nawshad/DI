'''
All the local llm sub class are declared here
'''
from typing import Dict, Any

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from src.utils.llm.base_llm import BaseLLM
import os
load_dotenv()


class LocalLLM(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = init_chat_model(**kwargs)

    def input(self, text:str) -> AIMessage:
        return self.model.invoke(text)


class HFLocalLLM(BaseLLM):
    def __init__(self, **kwargs):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(**kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(**kwargs)
        pipe = pipeline(task="text-generation", model=self.model, tokenizer=self.tokenizer, max_new_tokens=100)
        self.hf = HuggingFacePipeline(pipeline=pipe)

    def input(self, text:str) -> str:
        return self.hf.invoke(text)



if __name__ == "__main__":
    localLLM = LocalLLM(model="llama3.1:8b", model_provider="Ollama")
    print(localLLM.input("Hi!").content)

    hfLocalLLM = HFLocalLLM(pretrained_model_name_or_path="gpt2")
    print(hfLocalLLM.input("Hi!"))
