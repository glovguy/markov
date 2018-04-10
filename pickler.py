import pickle
import spacy
from src.markov import stack_markov, regular_markov
from src.plagiarism.plagiarism import build_plagiarism_trie


nlp = spacy.load('en_core_web_sm')

def read_file(filename):
    with open(filename, "r") as file:
        raw_text = file.read()
        contents = nlp(raw_text)
    return contents


eitherOr = read_file('data/corpora/EitherOr.txt')

symposium = read_file('data/corpora/symposium.txt')
republic = read_file('data/corpora/republic.txt')
apology = read_file('data/corpora/apology.txt')


# Regular Markov Chain
regular_chain = regular_markov.build_chain(symposium)
regular_chain = regular_markov.build_chain(republic, regular_chain)
regular_chain = regular_markov.build_chain(apology, regular_chain)

with open('data/pickles/plato_regular_chain.pkl', 'wb') as myf:
    pickle.dump(regular_chain, myf)


# Stack Markov Chain
stack_chain = stack_markov.build_chain(symposium)
stack_chain = stack_markov.build_chain(republic, stack_chain)
stack_chain = stack_markov.build_chain(apology, stack_chain)

with open('data/pickles/plato_stack_chain.pkl', 'wb') as myf:
    pickle.dump(stack_chain, myf)


# Plagiarism Trie
plato_trie = build_plagiarism_trie(symposium)
plato_trie = build_plagiarism_trie(republic, plato_trie)
plato_trie = build_plagiarism_trie(apology, plato_trie)

with open('data/pickles/plato_plagiarism_trie.pkl', 'wb') as myf:
    pickle.dump(plato_trie, myf)

kierkegaard_trie = build_plagiarism_trie(eitherOr)

with open('data/pickles/kierkegaard_plagiarism_trie.pkl', 'wb') as myf:
    pickle.dump(kierkegaard_trie, myf)
