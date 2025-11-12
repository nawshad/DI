from typing import List

from langchain_core.prompts import ChatPromptTemplate
from src.utils.debug.decorators import debug_func_decorator
from src.utils.prompts.base_prompt import BasePrompt


class SummarizationPrompt(BasePrompt):
    def __init__(self, init_prompt: str, entity_list: List):
        super().__init__()
        self.init_prompt  = init_prompt
        self.entity_list_text = ""
        if entity_list:
            entity_list_string = ', '.join(entity_list).strip()
            self.entity_list_text = (
                f"In your summary please include "
                f"information regarding the following "
                f"entities: {entity_list_string}."
            )

    def system_prompt(self):
        system_message = (
            "system",
            "{init_prompt} "
            "Summarize the provided text in {num_sentences} sentences. "
            "Please do not lose any information regarding the entities "
            "present in the text. Please provide the summary as a key, value "
            "pair, which looks like this: {summary_example}. "
            f"{self.entity_list_text}"
        )
        return system_message

    def human_prompt(self):
        human_message = ("human", "{text}")
        return human_message


    @debug_func_decorator
    def final_prompt(self):
        prompt_template = ChatPromptTemplate.from_messages([
            self.system_prompt(),
            self.human_prompt()
            ]
        )
        return prompt_template