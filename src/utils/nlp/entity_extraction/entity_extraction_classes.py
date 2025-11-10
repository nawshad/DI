'''
In this file we write a base abstract class for entity extraction, which
initializes a constructor for different NLP packages or LLM models, takes
a text input and provides a standardized text output (entities with their
type and any extra attributes). For stanza based methods, entity extraction
and their extra attributes is done simultaneously.
'''
from typing import Dict, List
import spacy
import stanza
from transformers import pipeline
from src.utils.debug.decorators import debug_func_decorator
from src.utils.nlp.entity_extraction.base_entity_extractor import BaseEntityExtractor

class SpacyEntityExtractor(BaseEntityExtractor):
    def __init__(self, nlp_object):
        super().__init__() # required to override parent attributes
        self.nlp_object = nlp_object

    @debug_func_decorator
    def extract(self, text: str, entity_types: List):
        # print(f"Output processing Overridden here at "
        #       f"spacy based processing for: {self.nlp_object} for: {text}")
        doc = self.nlp_object(text)
        entity_attribs = {}
        for ent in doc.ents:
            if ent.label_ in entity_types:
                entity_attribs[ent.text] = ent.label_
        return entity_attribs


class StanzaEntityExtractor(BaseEntityExtractor):
    def __init__(self, nlp_object):
        super().__init__()  # required to override parent attributes
        self.nlp_object = nlp_object

    @debug_func_decorator
    def extract(self, text: str, entity_types: List):
        # print(f"Output processing Overridden here at "
        #       f"spacy based processing for: {self.nlp_object} for: {text}")
        doc = self.nlp_object(text)
        entity_attribs = {}
        for ent in doc.ents:
            if ent.type in entity_types:
                entity_attribs[ent.text] = ent.type
        return entity_attribs


class BERTEntityExtractor(BaseEntityExtractor):
    def __init__(self, nlp_object):
        super().__init__()  # required to override parent attributes
        self.nlp_object = nlp_object

    @debug_func_decorator
    def extract(self, text: str, entity_types: List):
        entity_attribs = {}
        entities = self.nlp_object(text)
        for entity in entities:
            if entity['entity_group'] in entity_types:
                entity_attribs[entity['word']] = entity['entity_group']
        return entity_attribs


def test():
    text = (
        "Apple Inc. is a technology company based in "
        "Cupertino, California. John Anderson used to work there. "
        "Not sure, John still works there, but his brother "
        "Andy works there."
    )

    entity_types = ['ORG', 'PERSON', 'LOC', 'GPE']

    # Spacy based Entity Extraction
    nlp = spacy.load("en_core_web_sm")     # nlp = spacy.blank("en")
    spacEE = SpacyEntityExtractor(nlp_object=nlp)
    print(f"Spacy output: {spacEE.extract(text=text, entity_types=entity_types)}")

    # BERT based Entity Extraction
    nlp = pipeline(
        task="ner",
        model="dbmdz/bert-large-cased-finetuned-conll03-english",
        aggregation_strategy="simple"
    )

    BertEE = BERTEntityExtractor(nlp_object=nlp)
    print(f"BERT output: {BertEE.extract(text=text, entity_types=entity_types)}")

    nlp = stanza.Pipeline(
        lang='en',
        weights_only=False,
        use_gpu=False,
        processors=
        'tokenize,'
        'lemma,'
        'pos,'
        'ner,'
        'coref',
    )

    stanEE = StanzaEntityExtractor(nlp_object=nlp)
    print(f"Stanza output: {stanEE.extract(text=text, entity_types=entity_types)}")


if __name__ == "__main__":
   test()