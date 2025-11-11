'''
Doc categorizer
using different NLP
libraries.
'''
from src.utils.debug.decorators import debug_func_decorator
from src.utils.nlp.classification.base_classifier import BaseClassifier

# See Lab for some ideas

class SpacyMultiLabel(BaseClassifier):
    def __init__(self):
        super().__init__()

    @debug_func_decorator
    def classify(self, text):
        pass