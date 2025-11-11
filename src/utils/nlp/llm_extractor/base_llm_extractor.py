from abc import ABC, abstractmethod
from typing import Sequence, Any
from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable

'''
Base class for LLM Extraction
for various downstream tasks, including
Entity Extraction, Relation Extraction, Classification
and summarization.
'''

class BaseLLMExtractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def prompt_chain(self) -> Runnable[PromptValue | str | Sequence[BaseMessage | list[str] | tuple[str, str] | str | dict[str, Any]], dict | Any]:
        pass

    @abstractmethod
    def prompt_grounding(self, text: str) -> str:
        pass
