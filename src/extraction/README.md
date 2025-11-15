### TODO:
- Here we create extraction class (based on Docling for now):
  - which will use different extractors for different file types:
    - Start with Docling/Langchain Docling with different:
      - Hybrid Chunking:
        - https://docling-project.github.io/docling/concepts/chunking/#basic-usage
        - How to limit the hybrid chunking based on token size, how does it handle context?
          - Token size can be specified
          - We need to find how to seperate text content of a chunk from other elements, such as: tables, images
          and save those in doc_store, art_store and vector_store.
          - Advanced docling chunking with artifacts (table, image) serializers:
            - https://docling-project.github.io/docling/examples/advanced_chunking_and_serialization/#setup 
  - Optimization strategies for large scale file loading.
    - Parallel batch processing.
    
- Develop all the functions that we will perform while extraction using nlp utils:
  - coref_resolution based chunking 
  - different other chunkings (for langchain based chunking)
  - entity_doc_rel
  
### Docling Wisdom:
-  See the docling parsed json for more info:
-  A document object has following major components:
  - Root
    - schema name
    - version
    - name: <file_name>
  - origin
    - mimetype
    - binary_hash
    - filename
  - furniture 
    - Not sure what are its children, seems empty everytime!
  - body
    - Under root, no parent.
    - Any of the following items below can be its children.
  - groups
     - Usually body is its parent.
     - This is the grouping of different elements below.
  - texts
    - Usually body is its parent.
    - This is the text elements
    - has provenance based on page no and location in the page
  - pictures
    - Usually body is its parent.
    - This is the picture elements
    - has provenance based on page no and location in the page
  - tables
    - Usually body is its parent.
    - This is the picture elements
    - has provenance based on page no and location in the page
  - key_value_items
    - Not sure yet what is it?
  - form_items
    - Not sure yet what is it?
  - pages
    - images of each page if it was a pdf file, otherwise this is empty.

- When a document is chunked, it is chunked based on grounded (text or otherwise)
chunks with reference to each element which are referenced from the chunk.

