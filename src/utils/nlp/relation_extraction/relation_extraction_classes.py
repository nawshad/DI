'''
Here we construct the LLM based relation extraction
with the help of re_prompt and local_llms.
'''
from typing import List, Any, Sequence, Dict
from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseChatModel
from src.utils.debug.decorators import debug_func_decorator
from src.utils.general.data_structure_utils import key_given_value
from src.utils.llm.local_llms import LocalLLM
from src.utils.nlp.relation_extraction.base_triple_extractor import BaseTripleExtractor
from src.utils.prompts.re_prompt import RelationExtractionPrompt
from src.utils.structured_outputs.llm_output import zeroshot_triple_schema


class LLMTripleExtractor(BaseTripleExtractor):
    def __init__(self, llm:  BaseChatModel | _ConfigurableModel, rePrompt: RelationExtractionPrompt,
                 relations: Dict[str, List[str]],
                 entities: List[str],
                 triples_list_schema: Dict[str, List[Dict[str, str]]]
                 ):
        super().__init__()
        self.llm = llm
        self.re_prompt = rePrompt
        self.entities = entities
        self.relations = relations
        self.relationship_string = ', '.join(self.relation_string()).strip(', ')
        self.triples_list_schema = triples_list_schema #defines the output structure of the LLM output
        self.entity_string = ', '.join(entities).strip(', ')

    def relation_string(self) -> List:
        relations_list = []
        for key, values in self.relations.items():
            for value in values:
                relations_list.append(value)
        return relations_list

    def prompt_chain(self):
        chain = self.llm.with_structured_output(
            schema=zeroshot_triple_schema,
            method="json_mode"
        )
        return chain

    def prompt_grounding(self, text) :
        gr_prompt = self.re_prompt.final_prompt().invoke({
            'init_prompt': self.re_prompt.init_prompt,
            'relationship_string': self.relationship_string,
            'triples_list_schema': self.triples_list_schema,
            'entity_string' : self.entity_string,
            'text': text
        })

        print(f"grounded prompt: {gr_prompt}")
        return gr_prompt

    def filter_triples(self, triples_list):
        filtered_triple_list = []
        try:
            for triple in triples_list['triples']:
                print(f"triple: {triple}, {triple['subject'], triple['object'], triple['relationship']}")
                metadata = {}
                if triple['subject'] or triple['object'] in self.entities:
                    metadata['relation_type'] = key_given_value(self.relations, triple['relationship'].strip())
                    metadata['llm_used'] = self.llm.model
                    triple['metadata'] = metadata
                    filtered_triple_list.append(triple)
        except Exception as e:
            print(f"exception occured: {e}")
        return filtered_triple_list

    @debug_func_decorator
    def extract(self, text, _filter=True):
        triples_list = self.prompt_chain().invoke(self.prompt_grounding(text))
        print(f"triples_list: {triples_list}")
        if _filter:
            return self.filter_triples(triples_list=triples_list)
        return triples_list


def test():
    doc = ("James McAndersen lives in Ohio. He is a very "
           "good baseball player. He is 32 years old. McAndersen was "
           "directly related to the homicide case of John.")


    # model_name = "smollm:latest"
    # model_name = "tinyllama:latest"
    # model_name = "deepseek-r1:7b"
    model_name = "llama3.1:8b"
    # model_name = "deepseek-r1:8b"

    llama31 = LocalLLM(model=model_name, model_provider="Ollama")

    print(f"llama31 attributes: {llama31.model}")

    provided_relations = {
        'attributes': ['age', 'gender', 'address', "lives in", 'profession'],
        'criminal_activity': ["killed by", 'killed']
    }

    provided_entities = ["James McAndersen", 'Ohio', "McAndersen", 'John']

    init_prompt = (
        "You are a networked intelligence helping a human track knowledge triples about all "
        "relevant people, things, concepts, etc. and integrating them with your knowledge stored within "
        "your weights as well as that stored in a knowledge graph. Extract all of the knowledge triples "
        "from the text. "
        "A knowledge triple is a clause that contains a subject, a relationship, and an object. "
        "The subject is the entity being described, the relationship is the property of the subject that is being "
        "described, and the object is the value of the property."
    )

    rePrompt = RelationExtractionPrompt(init_prompt=init_prompt)
    print(f"rePrompt final_prompt(): {rePrompt.final_prompt()}")

    llmTriple = LLMTripleExtractor(
        llm=llama31.model,
        rePrompt=rePrompt,
        relations=provided_relations,
        entities=provided_entities,
        triples_list_schema=zeroshot_triple_schema
    )

    print(f"Extracted triples: {llmTriple.extract(doc)}")


if __name__ == "__main__":
    test()