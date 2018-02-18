import pickle
from src.markov import regular_markov, stack_markov


with open('data/pickles/plato_regular_chain.pkl', 'br') as myf:
    regular_chain = pickle.load(myf)

with open('data/pickles/plato_stack_chain.pkl', 'br') as myf:
    stack_chain = pickle.load(myf)

def gen_r():
    print(regular_markov.generate_message(regular_chain))

def gen_s():
    print(stack_markov.generate_message(stack_chain))


if __name__ == "__main__":
    print("\n")
    print("Regular markov chain:")
    gen_r()
    print("\n")
    print("Stack markov chain:")
    gen_s()
