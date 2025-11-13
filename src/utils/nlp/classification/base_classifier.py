from abc import ABC, abstractmethod
from typing import List


class BaseClassifier(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def classify(self, text: str) -> List[str]:
        pass

