'''
Doc categorizer
using different NLP
libraries.
'''
from src.utils.nlp.classification.base_classifier import BaseClassifier

# See Lab for some ideas

class SpacyMultiLabel(BaseClassifier):
    def __init__(self):
        super().__init__()

    def classify(self):
        pass