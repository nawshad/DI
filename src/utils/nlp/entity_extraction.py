'''
In this file we write a base abstract class for entity extraction, which
initializes a constructor for different NLP packages or LLM models, takes
a text input and provides a standardized text output (entities with their
type and any extra attributes). For stanza based methods, entity extraction
and their extra attributes is done simultaneously.
'''
import warnings
from typing import Dict
import spacy
import stanza
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline


# from transformers import AutoTokenizer, AutoModelForTokenClassification
# from transformers import pipeline


class EntityExtractor:
    def __init__(self, nlp_object):
        self.nlp_object = nlp_object

    #TODO: input processing is same for both Spacy and Stanza, make LLM input same as well.
    def input_processing(self, text:str) -> str:
        clean_text = ''
        print(f"Here we will do input processing relevant to "
              f"common EntityExtractor, unless overridden for: {self.nlp_object} for: {text}")
        return clean_text
    def output_processing(self, text: str)-> Dict[str,str]:
        entity_attribs = {}
        print(f"Here we will do output processing relevant to "
              f"common EntityExtractor, unless overridden for: {self.nlp_object} for: {text}")
        return entity_attribs


class SpacyEntityExtractor(EntityExtractor):
    def output_processing(self, text: str)->Dict[str,str]:
        print(f"Output processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")
        doc = self.nlp_object(text)
        entity_attribs = {}
        for ent in doc.ents:
            entity_attribs[ent.text] = ent.label_
        return entity_attribs


class StanzaEntityExtractor(EntityExtractor):
    def output_processing(self, text: str)->Dict[str,str]:
        print(f"Output processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")
        doc = self.nlp_object(text)
        entity_attribs = {}
        for ent in doc.ents:
            entity_attribs[ent.text] = ent.type
        return entity_attribs


class BERTEntityExtractor(EntityExtractor):
    def output_processing(self, text: str)->Dict[str,str]:
        entity_attribs = {}
        entities = self.nlp_object(text)
        for entity in entities:
            entity_attribs[entity['word']] = entity['entity_group']
        return entity_attribs


if __name__ == "__main__":

    text = ("Apple Inc. is a technology company based in Cupertino, California. John Anderson used to work there. "
            "Not sure, John still works there, but his brother Andy works there.")
    # # #
    # # #
    nlp = spacy.load("en_core_web_sm")
    spacy_nlp = EntityExtractor(nlp_object=nlp)
    spacEE = SpacyEntityExtractor(nlp_object=spacy_nlp.nlp_object)
    print(f"Spacy output: {spacEE.output_processing(text=text)}")


    nlp = pipeline(task= "ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple")
    #
    bert_nlp = EntityExtractor(nlp_object=nlp)
    BertEE = BERTEntityExtractor(nlp_object=bert_nlp.nlp_object)
    print(f"BERT output: {BertEE.output_processing(text=text)}")

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

    stanza_nlp = EntityExtractor(nlp_object=nlp)
    stanEE = StanzaEntityExtractor(nlp_object=stanza_nlp.nlp_object)
    print(f"Stanza output: {stanEE.output_processing(text=text)}")