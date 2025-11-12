from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm.local_llms import LocalLLM
from src.utils.prompts.init_prompt_store import SUMM_INIT_PROMPT, RE_INIT_PROMPT
from src.utils.structured_outputs.llm_output import zeroshot_summary_schema


def test_re_prompt():
    prompt_template_triples = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "{initiating_prompt}"
                " Extract triples for the relationships: {relationship_string} "
                f"from the provided text only. Do not provide any between "
                f"subject and object, which is not in the provided text. "
                " Please return the triples in a list of json key, value pairs, which"
                " looks like this: {triples_list_example} "
                "Please return these triples for the following subject or objects: {entity_list}"
            ),
            ("human", "{text}"),
        ]
    )

    initiating_prompt = RE_INIT_PROMPT
    relationship_string = f"'age', 'gender', 'address', 'lives in', 'profession'"
    entity_list = f" John, James, Richard"

    triples_list_example = {
        'triples': [
            {
                'subject': 'subject name',
                'relationship': 'relationship name',
                'object': 'object name',
            }
        ]
    }

    grounded_prompt = prompt_template_triples.invoke({
        'initiating_prompt': initiating_prompt,
        'relationship_string': relationship_string,
        'triples_list_example': triples_list_example,
        'entity_list': entity_list,
        'text': text
    })

    print(f"grounded_prompt: {grounded_prompt}")

    chain = llama31.with_structured_output(
        schema=triples_list_example,
        method="json_mode"
    )

    triples = chain.invoke(grounded_prompt)
    print(f"triples: {triples}")


def test_summarization_prompt():
    entity_list = ["John", "James", "Richard"]
    entity_list_text = ""
    if entity_list:
        entity_list_text = f"Please include information for the following entities: {entity_list} in your summary."

    summary_example = zeroshot_summary_schema

    prompt_template_triples = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "{initiating_prompt} "
                "Summarize the provided text in {num_sentence} sentences. "
                "Please do not lose any information regarding the entities "
                "present in the text. Please provide the summary as a key, value "
                "pair, which looks like this: {summary_example}. "
                f"{entity_list_text}"
            ),
            ("human", "{text}"),
        ]
    )
    initiating_prompt  = SUMM_INIT_PROMPT

    num_sents = 2


    grounded_prompt = prompt_template_triples.invoke({
        'initiating_prompt': initiating_prompt,
        'num_sentence' : num_sents,
        'summary_example': summary_example,
        'entity_list': entity_list,
        'text': text
    })

    print(f"grounded_prompt: {grounded_prompt}")

    chain = llama31.with_structured_output(
        schema=summary_example,
        method="json_mode"
    )

    summary = chain.invoke(grounded_prompt)

    print(f"summary: {summary}")


if __name__ == "__main__":
    # model_name = "llama3.1:8b"
    model_name = "deepseek-r1:8b"

    text = ("John and James are two brothers. They used live in "
            "New York. After James was murdered, John left "
            "New York and moved to California. There he is now a "
            "Professor in the University of Los "
            "Angeles where he met with Richard another"
            "Professor but in the different department.")

    llama31 = LocalLLM(model=model_name, model_provider="Ollama").model
    test_re_prompt()
    test_summarization_prompt()