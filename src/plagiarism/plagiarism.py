
def build_plagiarism_trie(doc, trie = {}):
    i = 0
    for sent in doc.sents:
        trie = add_words_to_trie(words(sent), trie)
    return trie


def add_words_to_trie(words, trie):
    if trie is 'END':
        return trie
    word = next(words)
    if word.norm_ is 'END':
        return 'END'
    subtrie = trie.get(word.norm_, {})
    trie[word.norm_] = add_words_to_trie(words, subtrie)
    return trie


class EndIter(object):
    def __init__(self):
        self.norm_ = 'END'


def words(sent):
    for word in sent:
        yield word
    yield EndIter()


def is_sent_plagiarized(sent, trie):
    subtrie = trie
    for word in sent:
        subtrie = subtrie.get(word.norm_, 'GOOD')
        if subtrie is 'GOOD': return False
        if subtrie is 'END': return True
    raise Exception
