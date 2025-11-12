from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate

class BasePrompt(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def system_prompt(self) -> tuple[str, str]:
        pass

    @abstractmethod
    def human_prompt(self) -> tuple[str, str]:
        pass

    def ai_prompt(self):
        pass

    @abstractmethod
    def final_prompt(self) -> ChatPromptTemplate:
        pass


