# https://docs.langchain.com/oss/python/langchain/models#using-a-configurable-model-declaratively

import os
from abc import ABC, abstractmethod
from typing import Any, Dict
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import dotenv
from langchain_core.messages import AIMessage
load_dotenv()


class BaseLLM(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def input(self, text:str) -> AIMessage :
        '''
        Any input processing required before feeding the raw input
        to the model or just raw input.
        :return:
        '''
        pass