from abc import ABC, abstractmethod


class BaseClassifier(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def classify(self, text: str):
        pass

