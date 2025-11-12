''''
Saliency Based Summarization.
    -Word Based Summarization:
        - Word saliency based summarization,
        where word saliency can be calculated
        based on their frequency in the document,
        better to use tf-idf. Find top_k most
        common words.

        - Score the sentences based summing the frequency
        of the common words.

    - Entity based summarization:
        - Find the frequency of the most common named entities
        - Score the sentences based summing the frequency
        of those entity frequency.

    - Take the top_k sentence as the summary.
    - Sentence Based Saliency:
        - Find sentence based attention scores
        - Take top-k salient sentences as a summary

LLM based summarization:
- Using prompt to summarize a document, we can
also provide word or entity saliency from the
above provided methods.



Other libs:
- Gensim has its own summarization
'''
from typing import Dict

from langchain.chat_models.base import _ConfigurableModel
from langchain_core.language_models import BaseChatModel

from src.utils.debug.decorators import debug_func_decorator
from src.utils.nlp.llm_extractor.base_llm_extractor import BaseLLMExtractor
from src.utils.nlp.summarization.base_summarizer import BaseSummarizer
from src.utils.prompts.summ_prompt import SummarizationPrompt
from src.utils.structured_outputs.llm_output import zeroshot_summary_schema


class LLMSummarzier(BaseSummarizer, BaseLLMExtractor):
    def __init__(self, llm:  BaseChatModel | _ConfigurableModel,
                 summPrompt: SummarizationPrompt,
                 summarization_schema: Dict[str,str],
                 num_sents: int
                 ):
        super().__init__()
        self.llm = llm
        self.summPrompt = summPrompt
        self.summarization_schema = summarization_schema
        self.num_sents = num_sents

    def prompt_chain(self):
        chain = self.llm.with_structured_output(
            schema=zeroshot_summary_schema,
            method="json_mode"
        )
        return chain

    def prompt_grounding(self, text) :
        gr_prompt = self.summPrompt.final_prompt().invoke({
            'init_prompt': self.summPrompt.init_prompt,
            'num_sentences': self.num_sents,
            'summary_example': self.summarization_schema,
            'text': text
        })

        print(f"grounded prompt: {gr_prompt}")
        return gr_prompt

    @debug_func_decorator
    def summarize(self, text):
        summary = self.prompt_chain().invoke(self.prompt_grounding(text))
        return summary