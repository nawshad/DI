### TODO:
- Here we create extraction class (based on Docling for now):
  - which will use different extractors for different file types:
    - Starting with pdf files.
    - Later, HTML, CSV etc
    - Start with Docling/Langchain Docling with different:
      - Hybrid Chunking:
        - https://docling-project.github.io/docling/concepts/chunking/#basic-usage
        - How to limit the hybrid chunking based on token size, how does it handle context?
      - Advanced docling chunking with atrtifacts (table, image) serializers:
        - https://docling-project.github.io/docling/examples/advanced_chunking_and_serialization/#setup
        - How can we extract chunk related artifacts?
  - Optimization strategies for large scale file loading.
  