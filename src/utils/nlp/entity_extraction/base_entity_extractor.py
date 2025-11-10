from abc import ABC, abstractmethod
from typing import List, Dict


class BaseEntityExtractor(ABC):
    # Define generic variables initialization if required
    def __init__(self):
        pass

    # Generic Input processing applicable for all Extractors,
    # can be overridden inside the child class, or augmented
    # inside the child class, by calling it through super().
    def input_processing(self, text:str) -> str:
        pass

    # Generic Output processing applicable for all Extractors,
    # can be overridden inside the child class, or augmented
    # inside the child class, by calling it through super().
    @abstractmethod
    def extract(self, text: str, entity_types: List)-> Dict[str,str]:
        pass