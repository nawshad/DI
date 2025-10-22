### TODO:
- Code for all kinds of Stores Creation, as follows, also, uses
reusuable code from utils based on underlying Store Types:

  - Data Store:
    - doc_id
    - doc_name
    - source_path
    - raw_content
    - raw_text
    - coref_resolved_text
    - summary
    - entity_attribs
    - entity_doc_rel
    - upload_timestamp
    
  - Artifact Store
    - art_id
    - doc_id
    - chunk_id
    - raw_art_content
    - art_content_text
    
  - Vector Store
    - chunk_id
    - doc_id
    - chunk_content
    
  - Triple Store
    - triple_id
    - chunk_id
    - doc_id
    - subject
    - relations
    - object
    - llm_used
    - score
    - extraction_timestamp