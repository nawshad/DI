import spacy
from spacy_experimental.coref.coref_component import DEFAULT_COREF_MODEL
from spacy_experimental.coref.coref_util import DEFAULT_CLUSTER_PREFIX


'''
ERROR: Failed building wheel for spacy_experimental
Failed to build spacy_experimental                                                                                                                                                                                                         
error: failed-wheel-build-for-install
'''

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    config = {
        "model": DEFAULT_COREF_MODEL,
        "span_cluster_prefix": DEFAULT_CLUSTER_PREFIX,
    }
    nlp.add_pipe("experimental_coref", config=config)
    nlp.initialize()
    text = "Nawshad lives in Dhaka, he has a brother, Rubaiyat, who lives in Trento."
    doc = nlp(text)
    print(f"doc: {doc}")