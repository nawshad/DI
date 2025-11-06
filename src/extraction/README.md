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

