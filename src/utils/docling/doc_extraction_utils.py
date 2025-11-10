# A helper function to find the actual item in the main docling document object
from docling_core.types import DoclingDocument
from docling_core.types.doc import NodeItem


def find_item_by_ref(doc: DoclingDocument, ref_id: str) -> NodeItem | None:
    print(f"ref_id: {ref_id}")
    for item, _ in doc.iterate_items():
        if hasattr(item, 'self_ref') and item.self_ref == ref_id:
            return item
    return None