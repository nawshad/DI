from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from src.utils.debug.decorators import debug_func_decorator
from src.utils.prompts.base_prompt import BasePrompt


class ClassificationPrompt(BasePrompt):
    def __init__(self, init_prompt: str, label_desc: Dict[str,str]):
        super().__init__()
        self.init_prompt  = init_prompt
        self.label_desc_str = ""

        if label_desc:
            # print(f"label_desc: {label_desc}")
            for key, value in label_desc.items():
                self.label_desc_str += f"'{key}' means {value}, "
            label_list_str = (', '.join(label_desc.keys())).strip()
            self.label_desc_str = (f"Please Label the provided text into the most likely labels "
                                   f"which represent the provided text from the following list of labels, "
                                   f"such as: {label_list_str}, where {self.label_desc_str.strip()}")
        else:
            self.label_desc_str = "Please Label the provided text with most likely labels which represent the provided text. "

        # print(f"label_desc_str: {self.label_desc_str}")

    def system_prompt(self):
        system_message = (
            "system",
            "{init_prompt} "
            f"{self.label_desc_str}"
            f" Please provide the labels in a list of json key, value pairs,"
            " which looks like this: {labels_example}. "
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