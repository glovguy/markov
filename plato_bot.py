import spacy
from src.helpers.language_helper import is_full_sentence, parse_complexity, closing_punct
from src.markov.stack_markov import *
from src.plagiarism.plagiarism import is_sent_plagiarized
from data.pickles import unpickle

nlp = spacy.load('en_core_web_sm')
plato = unpickle('data/pickles/plato_stack_chain.pkl')
plato_trie = unpickle('data/pickles/plato_plagiarism_trie.pkl')


def sentence_filter(sent):
    if not is_full_sentence(sent):
        return False
    if is_sent_plagiarized(sent, plato_trie):
        return False
    complexity = parse_complexity(sent)
    if complexity <= 3 and complexity > 10:
        return False
    return True

def is_relevant(sent, keywords):
    if keywords:
        contains_keywords = False
        for w in keywords:
            if w.text.lower() in sent.text.lower():
                contains_keywords = True
                break
        if not contains_keywords:
            return False
    return False

while True:
    print('\n')
    input_message = nlp(input("Say something to Plato: "))
    print('\n')
    input_keywords = [t for t in input_message if not t.is_stop]
    input_complexity = parse_complexity(input_message)

    doc = nlp(generate_message(plato, 5000))
    sentences = sorted(
        [sent for sent in doc.sents if sentence_filter(sent)],
        key=lambda sent: (is_relevant(sent, input_keywords))
        )
    print('\n'.join([closing_punct(sent.text) for sent in sentences[:input_complexity]]))

