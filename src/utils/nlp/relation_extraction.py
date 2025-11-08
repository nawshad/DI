'''
Here we construct the LLM based relation extraction
with the help of re_prompt and local_llms.
'''
from src.utils.general.data_structure import key_given_value
from src.utils.llm.local_llms import LocalLLM
from src.utils.prompts.re_prompt import RelationExtractionPrompt
from src.utils.structured_outputs.llm_output import zeroshot_triple_schema


class TripleLLM:
    def __init__(self, llm, rePrompt, relations, entities, triples_list_schema):
        self.llm = llm
        self.re_prompt = rePrompt
        self.entities = entities
        self.relations = relations
        self.relationship_string = ', '.join(self.relation_string()).strip(', ')
        self.triples_list_schema = triples_list_schema #defines the output structure of the LLM output
        self.entity_string = ', '.join(entities).strip(', ')


    def relation_string(self):
        relations_list = []
        for key, values in self.relations.items():
            for value in values:
                relations_list.append(value)
        return relations_list


    def prompt_chain(self):
        chain = self.llm.with_structured_output(schema=zeroshot_triple_schema, method="json_mode")
        return chain


    def prompt_grounding(self, text):
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
                if triple['subject'] or triple['object'] in self.entities:
                    triple['relation_type'] = key_given_value(self.relations, triple['relationship'])
                    filtered_triple_list.append(triple)
        except Exception as e:
            print(f"exception occured: {e}")
        return filtered_triple_list


    def extract(self, text, _filter=True):
        triples_list = self.prompt_chain().invoke(self.prompt_grounding(text))
        print(f"triples_list: {triples_list}")
        if _filter:
            return self.filter_triples(triples_list=triples_list)
        return triples_list



if __name__ == "__main__":
    doc = ("James McAndersen lives in Ohio. He is a very "
           "good baseball player. He is 32 years old. McAndersen was "
           "directly related to the homicide case of John.")

    llama31 = LocalLLM(model="llama3.1:8b", model_provider="Ollama")

    provided_relations = {
        'attributes': ['age', 'gender', 'address', 'lives in', 'profession'],
        'criminal_activity': ['killed by', 'killed']
    }

    provided_entities = ["James McAndersen", "Ohio", "McAndersen", "John"]


    init_prompt = (
        "You are a networked intelligence helping a human track knowledge triples about all "
         "relevant people, things, concepts, etc. and integrating them with your knowledge stored within "
         "your weights as well as that stored in a knowledge graph. Extract all of the knowledge triples "
         f"from the text. "
         f"A knowledge triple is a clause that contains a subject, a relationship, and an object. "
         f"The subject is the entity being described, the relationship is the property of the subject that is being "
         "described, and the object is the value of the property."
    )

    rePrompt = RelationExtractionPrompt(init_prompt = init_prompt)
    print(rePrompt.final_prompt())

    tripleLLM = TripleLLM(
        llm=llama31.model,
        rePrompt=rePrompt,
        relations=provided_relations,
        entities=provided_entities,
        triples_list_schema=zeroshot_triple_schema
    )

    print(f"Extracted triples: {tripleLLM.extract(doc)}")