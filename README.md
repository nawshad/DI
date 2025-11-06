### Clean code base for unstructured files analysis tool - DeepInsight
- Here we develop a clean code base for unstructured files analysis.
- Each folder will have their own README.md.
- The basic idea is to make the core components of this development as modular and extendable
as possible.

### Steps: (See the rough sketch of the DB design)
1. Develop docling based extractions and populate relevant database tables, e.g.: doc store,
artifact store.
2. Develop vector store from processed doc store raw data (which is likely to be pre-processed using NLP).
3. Extract data for Triple Store.


### Troubleshooting:
 - Stanza (1.9.2) and Docling does not go well together, to enable stanza with docling do as follows:
    - Change torch.load(), and set weights_only=False in line 56 of pretrained.py and line 301 of model.py