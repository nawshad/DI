'''
Here we will try our planned algorithm
for chunk extraction based on entity and
their coref extent.

Rough algo:

We will be calling the following function for each doc, so
we already know the doc_ids.

def text_chunk_with_metadata(entity_list: List, token_budget=200):
    chunks = []
    for each entity in entity_list do:
        chunk = []
        start_idx = start_sent_idx(entity) //the very first sentence
        end_idx = end_sent_idx(entity) //this is the coref extent of the entity: the last sentence.
        coref_rel_sents = '. 'join(sents[start_idx, end_idx)
        current_token_budget = [token for token in coref_rel_sents]
        if current_token_budget <= token_budget:
            chunk.append(coref_rel_sent)
        chunks.append('chunk': chunk, 'metadata' : {'rel_art_ids' : art_ids(rel_chunks_for_coref_rel_sents(coref_rel_sent_idx))})


'''