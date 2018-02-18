import pickle


def unpickle(filename):
    with open(filename, 'br') as myf:
        return pickle.load(myf)
