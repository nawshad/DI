import json
import re
from typing import List

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_huggingface.llms import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
load_dotenv()

'''
# Lets think about the following classes:
- LLMLoading:
    - This will load different LLMs and set
    different parameters related to initialization
    and inference.
- ChainCreation:
    - This will return chain suitable for various task
- StructuredGeneration:
    - This will generate structured text based on task type.
'''


def struct_output_with_chain():
    llm = ChatOllama(model="llama3.1:8b", validate_model_on_init=True)
    class MyStructuredOutput(BaseModel):
        name: str = Field(description="The name of the entity.")
        age: int = Field(description="The age of the entity.")
        is_active: bool = Field(description="Whether the entity is active.")

    #llm = ChatOpenAI(model="gpt-4o")  # Or your preferred LLM
    structured_llm = llm.with_structured_output(MyStructuredOutput, method="json_mode")
    template = """Extract name, age and is_active from the provided text in json format"""
    prompt = PromptTemplate.from_template(template)

    chain = prompt | structured_llm
    text = ("John lives with his brother Aron in a nearby hotel. "
            "Both are 12 years old. John is still working")
    print(chain.invoke({"text": text}))


def pydantic_output_parser():
    # llm = ChatOpenAI(model="gpt-4o")
    llm = ChatOllama(model="llama3.1:8b")
    class Person(BaseModel):
        """Information about a person."""

        name: str = Field(..., description="The name of the person")
        height_in_meters: float = Field(
            ..., description="The height of the person expressed in meters."
        )

    class People(BaseModel):
        """Identifying information about all people in a text."""

        people: List[Person]

    # Set up a parser
    parser = PydanticOutputParser(pydantic_object=People)

    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user query. Wrap the output in `json` tags\n{format_instructions}",
            ),
            ("human", "{query}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    query = "Anna is 23 years old and she is 6 feet tall"

    print(prompt.invoke({"query": query}).to_string())

    chain = prompt | llm | parser

    print(chain.invoke({"query": query}))


def pydantic_output_parser_custom():
    llm = ChatOllama(model="llama3.1:8b")
    # llm = ChatOpenAI(model="gpt-4o")
    # llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
    class Person(BaseModel):
        """Information about a person."""

        name: str = Field(..., description="The name of the person")
        height_in_meters: float = Field(
            ..., description="The height of the person expressed in meters."
        )

    class People(BaseModel):
        """Identifying information about all people in a text."""

        people: List[Person]

    # Prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer the user query. Output your answer as JSON that  "
                "matches the given schema: \`\`\`json\n{schema}\n\`\`\`. "
                "Make sure to wrap the answer in \`\`\`json and \`\`\` tags",
            ),
            ("human", "{query}"),
        ]
    ).partial(schema=People.model_json_schema())

    # Custom parser
    def extract_json(message: AIMessage) -> List[dict]:
        """Extracts JSON content from a string where JSON is embedded between \`\`\`json and \`\`\` tags.

        Parameters:
            text (str): The text containing the JSON content.

        Returns:
            list: A list of extracted JSON strings.
        """
        text = message.content
        # Define the regular expression pattern to match JSON blocks
        pattern = r"\`\`\`json(.*?)\`\`\`"

        # Find all non-overlapping matches of the pattern in the string
        matches = re.findall(pattern, text, re.DOTALL)

        # Return the list of matched JSON strings, stripping any leading or trailing whitespace
        try:
            return [json.loads(match.strip()) for match in matches]
        except Exception:
            raise ValueError(f"Failed to parse: {message}")

    query = "Anna is 23 years old and she is 6 feet tall"

    print(prompt.format_prompt(query=query).to_string())

    chain = prompt | llm | extract_json

    print(chain.invoke({"query": query}))


if __name__ == "__main__":
    # LocalLLMs
    # llm = ChatOllama(model="llama3.1:8b", validate_model_on_init=True)
    # template = """Question: {question}
    #    Answer: Let's think step by step."""
    # prompt = PromptTemplate.from_template(template)
    #
    # chain = prompt | llm
    # question = "What is electroencephalography?"
    # print(chain.invoke({"question": question}))
    #
    # # HF LLMs
    # model_id = "gpt2"
    # tokenizer = AutoTokenizer.from_pretrained(model_id)
    # model = AutoModelForCausalLM.from_pretrained(model_id)
    # pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)
    # hf = HuggingFacePipeline(pipeline=pipe)
    #
    # chain = prompt | hf
    # question = "What is electroencephalography?"
    # print(chain.invoke({"question": question}))
    #

    # Structured LLM
    # struct_output_with_chain()
    # The following function only works with certain Langchain models , such as ChatOpenAI.
    pydantic_output_parser()
    pydantic_output_parser_custom()



