import pickle
import spacy
from src.markov import stack_markov, regular_markov

nlp = spacy.load('en_core_web_sm')

def read_file(filename):
    with open(filename, "r") as file:
        raw_text = file.read()
        contents = nlp(raw_text)
    return contents


eitherOr = read_file('data/corpora/EitherOr.txt')

apology = read_file('data/corpora/apology.txt')
republic = read_file('data/corpora/republic.txt')
symposium = read_file('data/corpora/symposium.txt')


regular_chain = regular_markov.build_chain(symposium)
regular_chain = regular_markov.build_chain(republic, regular_chain)
regular_chain = regular_markov.build_chain(apology, regular_chain)

with open('data/pickles/plato_regular_chain.pkl', 'wb') as myf:
    pickle.dump(regular_chain, myf)


stack_chain = stack_markov.build_chain(symposium)
stack_chain = stack_markov.build_chain(republic, stack_chain)
stack_chain = stack_markov.build_chain(apology, stack_chain)

with open('data/pickles/plato_stack_chain.pkl', 'wb') as myf:
    pickle.dump(stack_chain, myf)
