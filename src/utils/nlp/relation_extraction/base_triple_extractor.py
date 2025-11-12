from abc import ABC, abstractmethod
from typing import List, Dict

class BaseTripleExtractor(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def filter_triples(self, triples_list: Dict[str, List[Dict[str, str | Dict[str,str]]]]) -> List:
        pass

    @abstractmethod
    def extract(self, text: str, _filter: bool) -> List:
        pass
