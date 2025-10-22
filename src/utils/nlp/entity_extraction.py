'''
In this file we write a base abstract class for entity extraction, which
initializes a constructor for different NLP packages or LLM models, takes
a text input and provides a standardized text output (entities with their
type and any extra attributes). For stanza based methods, entity extraction
and their extra attributes is done simultaneously.
'''
import stanza


class EntityExtractor:
    def __init__(self, nlp_object):
        self.nlp_object = nlp_object

    #TODO: input processing is same for both Spacy and Stanza, make LLM input same as well.
    def input_processing(self, text):
        print(f"Here we will do input processing relevant to "
              f"common EntityExtractor, unless overridden for: {self.nlp_object} for: {text}")

    def output_processing(self, text):
        print(f"Here we will do output processing relevant to "
              f"common EntityExtractor, unless overridden for: {self.nlp_object} for: {text}")

class SpacyEntityExtractor(EntityExtractor):
    def input_processing(self, text):
        print(f"Input processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")
    def output_processing(self, text):
        print(f"Output processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")

class StanzaEntityExtractor(EntityExtractor):
    def output_processing(self, text):
        print(f"Output processing Overridden here at "
              f"spacy based processing for: {self.nlp_object} for: {text}")

if __name__ == "__main__":
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
    nlpObjectInit = EntityExtractor(nlp_object=nlp)
    sEE = SpacyEntityExtractor(nlp_object=nlpObjectInit)
    sEE.input_processing(text="input processing for spacy")
    sEE.output_processing(text="output processing for spacy")
