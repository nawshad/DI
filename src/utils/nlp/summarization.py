''''
Saliency Based Summarization.
    -Word Based Summarization:
        - Word saliency based summarization,
        where word saliency can be calculated
        based on their frequency in the document,
        better to use tf-idf. Find top_k most
        common words.

        - Score the sentences based summing the frequency
        of the common words.

    - Entity based summarization:
        - Find the frequency of the most common named entities
        - Score the sentences based summing the frequency
        of those entity frequency.

    - Take the top_k sentence as the summary.
    - Sentence Bases Saliency:
        - Find sentence based attention scores
        - Take top-k salient sentences as a summary

LLM based summarization:
- Using prompt to summarize a document, we can
also provide word or entity saliency from the
above provided methods.



Other libs:
- Gensim has its own summarization
'''