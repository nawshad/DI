### TODO:
- Code for all kinds of Stores Creation, as follows, also, uses
reusuable code from utils based on underlying Store Types:

## Tables for DI
  - DocStore
    - doc_id --pk
    - case_id --fk ref Cases(case_id)
    - doc_name
    - source_path
    - raw_content
    - raw_text
    - file_type
    - coref_resolved_text
    - summary
    - entity_attribs
    - entity_doc_rel
    - entity_assoc
    - upload_timestamp
    
  - ArtifactStore
    - art_id --pk
    - doc_id --fk ref DocStore(doc_id)
    - chunk_id
    - raw_art_content (?? chunked ??)
    - art_content_text (?? chunked ??)
    - caption
    
  - VectorStore
    - chunk_id --pk
    - doc_id --fk ref DocStore(doc_id)
    - chunk_content_text
    - summary
    
  - TripleStore
    - triple_id --pk
    - chunk_id --fk ref VectorStore(chunk_id)
    - doc_id --fk ref DocStore(doc_id)
    - subject
    - relationship
    - object
    - llm_used
    - score
    - extraction_timestamp

  - ApplicationLogs:
    - id --pk
    - user_id 
    - session_id
    - user_query
    - gpt_response
    - model
    - timestamp

### Tables for AI Search
  - Searches
    - search_id --pk
    - user_id --fk ref Users(id)
    - title
    - description
    - tags
    - metadata
    - mock_file_type ??
    - isFavorite
    - created_at
    - updated_at
    
  - SearchPrompts
    - prompt_internal_id --pk,
    - search_id --fk ref Searches(search_id) INDEXED
    - prompt
    - response
    - response_text
    - timestamp

  - Users
    - id --pk
    - username
    - password
    - role
    - email
    
  - Cases
    - case_id --pk
    - user_id --fk ref Users(id) INDEXED, ON DELETE CASCADE  ?? (ensures a user's access to a specific case)
    - name
    - description
    - folder_path
    - file_data ?? (not sure, may be placeholder)
    - created_at
    - updated_at