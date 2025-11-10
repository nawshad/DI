### Deep Insight: A Configurable AI Framework for Unstructured Document Extraction and Analysis

### Clean code base for unstructured files analysis tool - DeepInsight
- Here we develop a clean code base for unstructured files analysis.
- Each folder will have their own README.md.
- The basic idea is to make the core components of this development as modular and extendable
as possible.

### Steps: (See the rough sketch of the DB design and storage/README.md in my sketchbook)
1. Develop docling based extractions and populate relevant database tables, e.g.: doc store,
artifact store.
2. Develop vector store from processed doc store raw data (which is likely to be pre-processed using NLP).
3. Extract data for Triple Store.

### API endpoints development:
1. I will have all the persistence resources in data.
2. I will then have functions that will be in api_endpoint and api_caller.
3. This will use some of the utils.
4. I will share these code for AI Search integration.

### Troubleshooting:
 - Stanza (1.9.2) and Docling does not go well together, to enable stanza with docling do as follows:
    - Change torch.load(), and set weights_only=False in line 56 of pretrained.py and line 301 of model.py