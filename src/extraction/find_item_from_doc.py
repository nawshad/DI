import json
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HierarchicalChunker
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.types.doc.labels import DocItemLabel
from docling_core.types.doc.document import TableItem, DoclingDocument
import os
from dotenv import load_dotenv
load_dotenv()


# A helper function to find the actual item in the main document
def find_item_by_ref(doc, ref_id):
    print(f"ref_id: {ref_id}")
    for item, _ in doc.iterate_items():
        if hasattr(item, 'self_ref') and item.self_ref == ref_id:
            return item
    return None


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
    dldoc = DoclingDocument.model_validate(doc)

    # 2. Chunk the document
    chunker = HybridChunker()
    chunks = list(chunker.chunk(dldoc))

    for i, chunk in enumerate(chunks):
        # Access the metadata for each chunk
        meta = chunk.meta

        # Check if the chunk contains table items
        for item_ref in meta.doc_items:
            if item_ref.label == DocItemLabel.TABLE:
                # You've found a reference to a table item
                # The 'self_ref' within item_ref can be used to pinpoint the exact item
                print(f"Chunk {i} contains a table.")
                # print(f"Table reference ID: {item_ref.self_ref}")


    for i, chunk in enumerate(chunks):
        for item_ref in chunk.meta.doc_items:
            if item_ref.label == DocItemLabel.TABLE:
                # Retrieve the original TableItem
                table_item = find_item_by_ref(dldoc, item_ref.self_ref)
                if table_item and isinstance(table_item, TableItem):
                    print(f"Table item: {table_item.export_to_markdown(doc=dldoc)}")


