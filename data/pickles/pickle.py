import pickle
import stack_markov
import markov


kierk = read_file('corpora/EitherOr.txt')

apology = markov.read_file('corpora/apology.txt')
republic = markov.read_file('corpora/republic.txt')
symposium = markov.read_file('corpora/symposium.txt')


regular_chain = markov.build_chain(symposium)
regular_chain = markov.build_chain(republic, regular_chain)
regular_chain =  markov.build_chain(apology, regular_chain)

with open('plato_regular_chain', 'wb') as myf:
    pickle.dump(regular_chain, myf)


stack_chain = stack_markov.build_chain(symposium)
stack_chain = stack_markov.build_chain(republic, stack_chain)
stack_chain =  stack_markov.build_chain(apology, stack_chain)

with open('plato_stack_chain', 'wb') as myf:
    pickle.dump(regular_chain, myf)
