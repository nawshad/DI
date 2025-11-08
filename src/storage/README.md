### TODO:
- Code for all kinds of Stores Creation, as follows, also, uses
reusuable code from utils based on underlying Store Types:
- Number in parentheses beside the name of the Table is the order of processing. 

## Tables for DI
  - DocStore (1)
    - doc_id --pk 
    - case_id --fk ref Cases(case_id) 
    - doc_name (unique name of a doc based on location) 
    - source_path (exact doc path) 
    - raw_content (docling object) 
    - file_type
    - raw_text 
    - summary -- 2 (update from chunk summaries)
    - timestamp

  - EntityStore (1/2)
    - entity_id --pk
    - doc_id --fk ref DocStore(doc_id)
    - entity_name
    - entity_type
    - entity_extra_attribs 
    - entity_doc_rel ({'entity' : 'doc text related to entity'})
    - entity_assoc ({'related_entities in descending order of relevance from NE association' : [])
    - timestamp
    
  - ArtifactStore (1)
    - art_id --pk
    - doc_id --fk ref DocStore(doc_id)
    - chunk_id
    - raw_art_content (from docling chunk)
    - art_content_text (from docling chunk)
    - caption (if available)
    - timestamp
    
  - VectorStore (1)
    - chunk_id --pk
    - doc_id --fk ref DocStore(doc_id)
    - art_ids --fk ref ArtStore(art_id)
    - chunk_content_text / chunk_content_coref text (we can use the chunks with entities only for this processing)
    - summary
    - timestamp
    
  - TripleStore (1/2)
    - triple_id --pk
    - chunk_id --fk ref VectorStore(chunk_id)
    - doc_id --fk ref DocStore(doc_id)
    - subject_id --fk ref EntityStore(entity_id)
    - subject
    - relationship
    - object_id --fk ref EntityStore(entity_id)
    - object
    - llm_used
    - score
    - timestamp

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