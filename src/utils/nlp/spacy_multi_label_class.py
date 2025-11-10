'''
Doc categorizer
using spacy
'''
import spacy
from spacy.tokens import DocBin
from spacy.training import Example


'''
The following example shows how we can train a spacy
model for any categories and therefore categorize 
a document.
'''

def multi_label_classification():
    # 1. Define your training data
    # Each entry is a tuple of (text, dictionary of labels)
    # Labels are represented as a dictionary where keys are category names and values are booleans.
    TRAIN_DATA = [
        ("This movie is a fantastic sci-fi thriller with great acting.",
         {"SCI_FI": True, "THRILLER": True, "COMEDY": False}),
        ("A hilarious comedy that will make you laugh out loud.", {"SCI_FI": False, "THRILLER": False, "COMEDY": True}),
        ("A deep philosophical drama, but a bit slow-paced.", {"DRAMA": True, "PHILOSOPHY": True, "COMEDY": False}),
        ("This film has no clear genre, just a confusing mess.",
         {"SCI_FI": False, "THRILLER": False, "COMEDY": False, "DRAMA": False, "PHILOSOPHY": False}),
        ("An action-packed thriller with stunning visuals.", {"THRILLER": True, "ACTION": True, "SCI_FI": False}),
        ("A thought-provoking sci-fi masterpiece.", {"SCI_FI": True, "PHILOSOPHY": True, "DRAMA": False}),
    ]

    # 2. Create a blank spaCy model and add the textcat_multilabel pipe
    nlp = spacy.blank("en")
    textcat = nlp.add_pipe("textcat_multilabel", last=True)

    # 3. Add labels to the text categorizer
    for _, annotations in TRAIN_DATA:
        for label in annotations.keys():
            print(f"label: {label}")
            textcat.add_label(label)

    # 4. Prepare the training examples
    examples = []
    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, {"cats": annotations})
        examples.append(example)

    # 5. Train the model
    optimizer = nlp.begin_training()
    for i in range(20):  # Train for a few iterations
        losses = {}
        nlp.update(examples, sgd=optimizer, losses=losses)
        print(f"Iteration {i}, Losses: {losses}")

    # 6. Test the trained model
    test_text = "This is a fast-paced action movie with some sci-fi elements."
    doc = nlp(test_text)
    print(f"\nText: {test_text}")
    print("Predicted Categories:")
    for category, score in doc.cats.items():
        print(f"- {category}: {score:.4f}")

    test_text_2 = "A lighthearted comedy about everyday life."
    doc_2 = nlp(test_text_2)
    print(f"\nText: {test_text_2}")
    print("Predicted Categories:")
    for category, score in doc_2.cats.items():
        print(f"- {category}: {score:.4f}")

if __name__ == "__main__":
    multi_label_classification()