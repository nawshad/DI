'''
In this file we write a base abstract class for entity extraction, which
initializes a constructor for different NLP packages or LLM models, takes
a text input and provides a standardized text output (entities with their
type and any extra attributes). For stanza based methods, entity extraction
and their extra attributes is done simultaneously.
'''
import warnings
from abc import ABC, abstractmethod
from typing import Dict
import spacy
import stanza
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline

class EntityExtractor(ABC):
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
    def extract(self, text: str)-> Dict[str,str]:
        pass


class SpacyEntityExtractor(EntityExtractor):
    def __init__(self, nlp_object):
        super().__init__() # required to override parent attributes
        self.nlp_object = nlp_object

    def extract(self, text: str)->Dict[str,str]:
        print(f"Output processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")
        doc = self.nlp_object(text)
        entity_attribs = {}
        for ent in doc.ents:
            entity_attribs[ent.text] = ent.label_
        return entity_attribs


class StanzaEntityExtractor(EntityExtractor):
    def __init__(self, nlp_object):
        super().__init__()  # required to override parent attributes
        self.nlp_object = nlp_object

    def extract(self, text: str)->Dict[str,str]:
        print(f"Output processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")
        doc = self.nlp_object(text)
        entity_attribs = {}
        for ent in doc.ents:
            entity_attribs[ent.text] = ent.type
        return entity_attribs


class BERTEntityExtractor(EntityExtractor):
    def __init__(self, nlp_object):
        super().__init__()  # required to override parent attributes
        self.nlp_object = nlp_object

    def extract(self, text: str)->Dict[str,str]:
        entity_attribs = {}
        entities = self.nlp_object(text)
        for entity in entities:
            entity_attribs[entity['word']] = entity['entity_group']
        return entity_attribs


if __name__ == "__main__":
    text = (
        "Apple Inc. is a technology company based in "
        "Cupertino, California. John Anderson used to work there. "
        "Not sure, John still works there, but his brother "
        "Andy works there."
    )

    # Spacy based Entity Extraction
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.blank("en")
    spacEE = SpacyEntityExtractor(nlp_object=nlp)
    print(f"Spacy output: {spacEE.extract(text=text)}")


    # BERT based Entity Extraction
    nlp = pipeline(
        task="ner",
        model="dbmdz/bert-large-cased-finetuned-conll03-english",
        aggregation_strategy="simple"
    )

    BertEE = BERTEntityExtractor(nlp_object=nlp)
    print(f"BERT output: {BertEE.extract(text=text)}")

    nlp = stanza.Pipeline(
        lang='en',
        use_gpu=False,
        processors=
        'tokenize,'
        'lemma,'
        'pos,'
        'ner,'
        'coref'
    )

    stanEE = StanzaEntityExtractor(nlp_object=nlp)
    print(f"Stanza output: {stanEE.extract(text=text)}")

