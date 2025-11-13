trailing_command = "Please do not provide any extra information which was not requested to you."


RE_INIT_PROMPT = (
    "You are a networked intelligence helping a human track knowledge triples about all "
    f"relevant people, things, concepts, etc. Extract all of the knowledge triples "
    "from the text. A knowledge triple is a clause that contains a subject, a relationship, and an object. "
    "The subject is the entity being described, the relationship is the property of the subject that is being "
    "described, and the object is the value of the property."
    f" {trailing_command} "
)

SUMM_INIT_PROMPT = (
    "You are an efficient text summarizer. Your task is "
    "to carefully read a given text and"
    " concisely summarize it without losing "
    "any information."
    f" {trailing_command} "
)


CLASSIFY_INIT_PROMPT = (
    "You are an efficient text labeler. Your task is "
    "to carefully read a given text and"
    " accurately label it."
    f" {trailing_command} "
)