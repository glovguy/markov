from sentence import is_full_sentence, parse_complexity, closing_punct
from stack_markov import *


plato = build_chain(read_file('corpora/apology.txt'))
plato = build_chain(read_file('corpora/republic.txt'), plato)
plato = build_chain(read_file('corpora/symposium.txt'), plato)

def sentence_filter(sent):
    if not is_full_sentence(sent):
        return False
    complexity = parse_complexity(sent)
    if complexity <= 3 and complexity > 10:
        return False
    return True

def is_relevant(sent, keywords):
    if keywords:
        contains_keywords = False
        for w in keywords:
            if w.text in sent.text:
                contains_keywords = True
                break
        if not contains_keywords:
            return False
    return False

while True:
    print('\n')
    input_message = nlp(input("Say something to Plato: "))
    input_keywords = [t for t in input_message if not t.is_stop]

    doc = nlp(generate_message(plato, 5000))
    sentences = sorted(
        [sent for sent in doc.sents if sentence_filter(sent)],
        key=lambda sent: (is_relevant(sent, input_keywords), input_message.similarity(sent))
        )
    print('\n'.join([closing_punct(sent.text) for sent in sentences[:6]]))

