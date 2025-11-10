from abc import ABC, abstractmethod

class BaseSummarizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def summarize(self):
        pass
