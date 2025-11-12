import json
import stanza
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.types.doc import PictureItem
from docling_core.types.doc.labels import DocItemLabel
from docling_core.types.doc.document import TableItem, DoclingDocument
import os
from dotenv import load_dotenv

from src.utils.docling.doc_extraction_utils import find_item_by_ref
from src.utils.llm.local_llms import LocalLLM
from src.utils.nlp.entity_extraction.entity_extraction_classes import StanzaEntityExtractor
from src.utils.nlp.relation_extraction.relation_extraction_classes import LLMTripleExtractor
from src.utils.nlp.summarization.summarization_classes import LLMSummarzier
from src.utils.prompts.init_prompt_store import RE_INIT_PROMPT, SUMM_INIT_PROMPT
from src.utils.prompts.re_prompt import RelationExtractionPrompt
from src.utils.prompts.summ_prompt import SummarizationPrompt
from src.utils.structured_outputs.llm_output import zeroshot_triple_schema, zeroshot_summary_schema

load_dotenv()


if __name__ == "__main__":
    # 1. Convert your document to a DoclingDocument object
    # converter = DocumentConverter()
    # result = converter.convert("your_document.pdf")
    # doc = result.document
    data_folder = os.environ["DATA_ROOT"]

    # batch_file_extraction(data_folder, input_doc_paths)
    # file_path = data_folder + "/extracted_data/2023_UCR_Manual_EN_final.json"

    file_path = data_folder + "/extracted_data/Homicide_KG.json"
    # file_path = data_folder + "extracted_data/nihms-362971-trunc.json"

    with open(file_path, "r") as fp:
        doc = json.loads(fp.read())

    # Recreate the DoclingDocument object
    dlDoc = DoclingDocument.model_validate(doc)

    # 2. Chunk the document
    chunker = HybridChunker()
    chunks = list(chunker.chunk(dlDoc))

    nlp = stanza.Pipeline(
        lang='en',
        weights_only=False,
        use_gpu=False,
        processors=
        'tokenize,'
        'lemma,'
        'pos,'
        'ner,'
        'coref',
    )

    EE = StanzaEntityExtractor(nlp_object=nlp)
    # nlp = spacy.load("en_core_web_sm")
    # EE = SpacyEntityExtractor(nlp_object=nlp)
    # print(f"Stanza output: {stanEE.extract(text=text)}")


    # for i, chunk in enumerate(chunks):
    #     # Access the metadata for each chunk
    #     print(f"chunk text: {chunk.text}")
    #     print(f"chunk text: {stanEE.extract(text=chunk.text)}")
    #
    #     meta = chunk.meta
    #
    #     # Check if the chunk contains table items
    #     for item_ref in meta.doc_items:
    #         if item_ref.label == DocItemLabel.TABLE:
    #             # You've found a reference to a table item
    #             # The 'self_ref' within item_ref can be used to pinpoint the exact item
    #             print(f"Chunk {i} contains a table.")
    #             # print(f"Table reference ID: {item_ref.self_ref}")

    localLLM = LocalLLM(model="llama3.1:8b", model_provider="Ollama")

    provided_relations = {
        'attributes': ['age', 'gender', 'address', 'profession'],
        'criminal_activity': ['killed by', 'killed']
    }

    entity_types = ['ORG', 'PERSON', 'LOC', 'GPE']

    init_re_prompt = RE_INIT_PROMPT

    rePrompt = RelationExtractionPrompt(init_prompt=init_re_prompt)

    init_summ_prompt = SUMM_INIT_PROMPT

    for i, chunk in enumerate(chunks):
        # Access the metadata for each chunk
        print(f"chunk text: {chunk.text}")
        chunk_entities = list(EE.extract(text=chunk.text, entity_types=entity_types).keys())

        if chunk_entities: # reducing formatting errors, needs to be handled inside the function as well!
            print(f"chunk entities: {chunk_entities}")

            llmTriple = LLMTripleExtractor(
                llm=localLLM.model,
                rePrompt=rePrompt,
                relations=provided_relations,
                entities=chunk_entities,
                triples_list_schema=zeroshot_triple_schema
            )

            print(f"triples: {llmTriple.extract(chunk.text)}")

            summPrompt = SummarizationPrompt(init_prompt=init_summ_prompt, entity_list=chunk_entities)

            llmSummarizer = LLMSummarzier(
                llm=localLLM.model,
                summarization_schema=zeroshot_summary_schema,
                summPrompt=summPrompt,
                num_sents=2
            )

            print(f"Summary: {llmSummarizer.summarize(chunk.text)}")

        for item_ref in chunk.meta.doc_items:
            if item_ref.label == DocItemLabel.TABLE:
                # Retrieve the original TableItem
                table_item = find_item_by_ref(dlDoc, item_ref.self_ref)
                if table_item and isinstance(table_item, TableItem):
                    print(f"Table item: {table_item.export_to_markdown(doc=dlDoc)}")

            if item_ref.label == DocItemLabel.PICTURE:
                # Retrieve the original TableItem
                pic_item = find_item_by_ref(dlDoc, item_ref.self_ref)
                if pic_item and isinstance(pic_item, PictureItem):
                    print(f"Image item: {pic_item.export_to_markdown(doc=dlDoc)}")


