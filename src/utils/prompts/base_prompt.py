from abc import ABC
from langchain_core.prompts import ChatPromptTemplate

class BasePrompt(ABC):
    def __init__(self):
        pass

    def system_prompt(self):
        pass

    def human_prompt(self):
        pass

    def ai_prompt(self):
        pass

    def final_prompt(self):
        pass


if __name__ == "__main__":

    prompt_template_triples = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "{initiating_prompt}"
                    "{relationship_string} "
                    f"from the provided text only. Do not provide any between "
                    f"subject and object, which is not in the provided text. "
                    " Please return the triples in a list of json key, value pairs, which"
                    " looks like this: {triples_list_example} "
                    "Please return these triples for the following subject or objects: {entity_list}"
                ),
                ("human", "{text}"),
            ]
        )

    initiating_prompt = "Initiating prompt goes here"
    relationship_string = " rel1, rel2, rel3 "
    entity_list = 'sample entity list'
    # trailing_text = " trailing text goes here {entity_list}"
    text = " Hello!"

    triples_list_example = {
        'triples': [
            {
                'subject': 'subject name',
                'relationship': 'relationship name',
                'object': 'object name',
            }
        ]
    }

    print(prompt_template_triples.invoke({
        'initiating_prompt': initiating_prompt,
        'relationship_string': relationship_string,
        'triples_list_example': triples_list_example,
        'entity_list' : entity_list,
        # 'trailing_text': trailing_text,
        'text': text
    }))
