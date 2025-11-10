from langchain_core.prompts import ChatPromptTemplate
from src.utils.prompts.base_prompt import BasePrompt


class RelationExtractionPrompt(BasePrompt):
    def __init__(self, init_prompt: str):
        super().__init__()
        self.init_prompt  = init_prompt

    def system_prompt(self):
        system_message = (
            "system",
            "{init_prompt}"
            " Extract triples for the relationships: {relationship_string} "
            "from the provided text only. Do not provide any relationship between "
            "subject and object, which is not in the provided text. "
            " Please return the triples in a list of json key, value pairs, which"
            " looks like this: {triples_list_schema}. "
            "Please return these triples for the following subject or objects: {entity_string}"
        )

        return system_message

    def human_prompt(self):
        human_message = ("human", "{text}")
        return human_message


    def final_prompt(self):
        prompt_template = ChatPromptTemplate.from_messages([
            self.system_prompt(),
            self.human_prompt()
            ]
        )
        return prompt_template
