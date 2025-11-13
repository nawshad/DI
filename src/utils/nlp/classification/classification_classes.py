'''
Doc categorizer
using different NLP
libraries.
'''
from typing import Sequence, Any

from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import Runnable

from src.utils.debug.decorators import debug_func_decorator
from src.utils.nlp.classification.base_classifier import BaseClassifier
from src.utils.nlp.llm_extractor.base_llm_extractor import BaseLLMExtractor
from src.utils.prompts.classify_prompt import ClassificationPrompt
from src.utils.structured_outputs.llm_output import zeroshot_classify_schema


# See Lab for some ideas

class SpacyMultiLabelClassifier(BaseClassifier):
    def __init__(self):
        super().__init__()

    @debug_func_decorator
    def classify(self, text):
        pass


class LLMMultiLabelClassifier(BaseClassifier, BaseLLMExtractor):
    '''
    This class will generate multiple label for a
    given document and predefined labels as a dictionary
    like this: {'label_1':'desc_of_label_1', 'label_2':'desc_of_label_2'}
    The output will be a List of labels for a document.
    '''
    def __init__(self, llm:  BaseChatModel | _ConfigurableModel, classifyPrompt: ClassificationPrompt):
        super().__init__()
        self.llm = llm
        self.classifyPrompt = classifyPrompt

    def prompt_chain(self):
        chain = self.llm.with_structured_output(
            schema=zeroshot_classify_schema,
            method="json_mode"
        )
        return chain

    def prompt_grounding(self, text):
        gr_prompt = self.classifyPrompt.final_prompt().invoke({
            'init_prompt': self.classifyPrompt.init_prompt,
            'labels_example': zeroshot_classify_schema,
            'text': text
        })
        print(f"grounded prompt: {gr_prompt}")
        return  gr_prompt

    @debug_func_decorator
    def classify(self, text):
        labels = self.prompt_chain().invoke(self.prompt_grounding(text))
        # print(f"labels_list: {labels}")
        return labels
