from abc import ABC, abstractmethod
from typing import List, Dict

from src.utils.nlp.llm_extractor.base_llm_extractor import BaseLLMExtractor


class BaseTripleExtractor(BaseLLMExtractor):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def filter_triples(self, triples_list: Dict[str, List[Dict[str, str | Dict[str,str]]]]) -> List:
        pass

    @abstractmethod
    def extract(self, text: str, _filter: bool) -> List:
        pass