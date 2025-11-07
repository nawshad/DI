from typing import Dict, List

from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm.local_llms import LocalLLM


def with_struct_output_given_entity_all_triples(llm, doc, prompt_template, entity_name, triples_list_example):
    # llm = return_models_provided_name(llm_name=llm_model_name)

    chain = llm.with_structured_output(schema={'triples':[{
            'subject':'subject name',
            'relationship': 'relationship name between subject and object',
            'object': 'object name',
        }
    ]}, method="json_mode")

    if entity_name:
        prompt = prompt_template.invoke({"text": doc, "entity": entity_name, "triples_list_example": triples_list_example})
        print(f"prompt in with struct ouput given entity {entity_name} all triples: {prompt}")

    else:
        prompt = prompt_template.invoke({"text": doc, "triples_list_example": triples_list_example})
        print(f"prompt in with struct ouput given entity {entity_name} all triples: {prompt}")

    return chain.invoke(prompt)


def key_given_value(dict: Dict[str, List[str]], value: str) -> str:
    for key, values in dict.items():
        if value in values:
            return key
    return ''


def extract_zero_shot_kg_triples(doc, llm, provided_relations, provided_entities):
    # extract list of triples corresponding to a preprocessed_doc based on zero-shot LLMs.
    mid_tuple = "relationship"  # this does not make any difference if we would use "predicate" instead!

    relations_list = []
    for key, values in provided_relations.items():
        for value in values:
            relations_list.append(value)

    print(f"relations: {relations_list}")

    initiating_prompt = ("You are a networked intelligence helping a human track knowledge triples about all "
                         "relevant people, things, concepts, etc. and integrating them with your knowledge stored within "
                         "your weights as well as that stored in a knowledge graph. Extract all of the knowledge triples "
                         #f"and their corresponding sentence 
                         f"from the text. "
                         f"A knowledge triple is a clause that contains a subject, a {mid_tuple}, and an object. "
                         f"The subject is the entity being described, the {mid_tuple} is the property of the subject that is being "
                         "described, and the object is the value of the property.")


    # relationship_string = ""
    relationship_string = (', ').join(relations_list).strip(', ')
    relationship_string = f" Extract triples for the {mid_tuple}s: {relationship_string}"
    print(f"{mid_tuple} string: {relationship_string}")

    entity_string = (', ').join(provided_entities).strip(', ')

    trailing_text = f"Please return these triples for the following subject or objects: {entity_string}"  # "where, keys are subject, relationship and object and values are their values respectively."
    # The above does not work, because, the provided example is confused as variable names.

    prompt_template_triples = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"{initiating_prompt}"
                f"{relationship_string if relationship_string else ''} "
                f"from the provided text only. Do not provide any {mid_tuple} between "
                f"subject and object, which is not in the provided text. "
                " Please return the triples in a list of json key, value pairs, which"
                " looks like this: {triples_list_example} "
                f"{trailing_text if trailing_text else ''}"
            ),
            ("human", "{text}"),
        ]
    )

    triples_list_example = {
        'triples': [
            {
                'subject': 'subject name',
                f"{mid_tuple}": 'relationship name',
                'object': 'object name',
                #'sentence': 'sentence representing the triple' #to use this uncomment the portion in the initializing prompt.
             }
        ]
    }

    triple_list = with_struct_output_given_entity_all_triples(
        llm,
        doc,
        prompt_template_triples,
        entity_name='',
        triples_list_example=triples_list_example
    )

    print(f"with struct output no given entity triples: {triple_list}")

    filtered_triple_list = []

    try:
        for triple in triple_list['triples']:
            print(f"triple: {triple}, {triple['subject'], triple['object'], triple['relationship']}")
            if triple['subject'] or triple['object'] in provided_entities:
                triple['relation_type'] = key_given_value(provided_relations, triple['relationship'])
                filtered_triple_list.append(triple)
    except Exception as e:
        print(f"exception occured: {e}")

    return filtered_triple_list


if __name__ == "__main__":
    doc = ("James McAndersen lives in Ohio. He is a very "
           "good baseball player. He is 32 years old. McAndersen was "
           "directly related to the homicide case of John.")

    localLLM = LocalLLM(model="llama3.1:8b", model_provider="Ollama")

    provided_relations = {
        'attributes': ['age', 'gender', 'address', 'lives in', 'profession'],
        'criminal_activity': ['killed by', 'killed']
    }

    provided_entities = ["James McAndersen", "Ohio", "McAndersen", "John"]

    triples = extract_zero_shot_kg_triples(
        doc,
        llm=localLLM.model,
        provided_relations=provided_relations,
        provided_entities=provided_entities
    )

    # Filter triples based on the presence of provided entities and relations. The entities
    # will be captured from running spacy/core NLP on the chunk.
    # return the triples with relationship type.

    print(f"Extracted triples: {triples}")





