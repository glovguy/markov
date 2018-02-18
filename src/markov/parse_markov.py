import random


def build_parse_chain(doc, chain = {}):
    index = 2
    doc_wo_spaces = [w for w in doc if not w.is_space]
    for word in doc_wo_spaces[index:]:
        key = (doc_wo_spaces[index - 2].dep, doc_wo_spaces[index - 1].dep)
        if key in chain:
            chain[key].append(word.i)
        else:
            chain[key] = [word.i]
        index += 1
    return chain


def generate_parse_message(chain, doc, count = 100):
    prev_tuple = random.choice(list(chain.keys()))
    all_word_indices = [item for sublist in chain.values() for item in sublist]
    word1 = random.choice([i for i in all_word_indices if doc[i].dep == prev_tuple[0]])
    word2 = random.choice([i for i in all_word_indices if doc[i].dep == prev_tuple[1]])

    message = doc[word1].orth_.capitalize() + ' ' + doc[word2].orth_
    word3 = doc[word2]

    while len(message.split(' ')) < count: # or not (word3.orth_ == '.' or word3.orth_ == '!' or word3.orth_ == '?' or word3.orth_ == ';'):
        if chain.get(prev_tuple):
            w3 = random.choice(chain[prev_tuple])
            word3 = doc[w3]
        else:
            raise Exception
        if word3.is_punct:
            message += word3.orth_
        elif "'" in word3.orth_[:2] and not word3.is_punct:
            message += word3.orth_
        else:
            message += ' ' + word3.orth_

        prev_tuple = (prev_tuple[1], word3.dep)
        if len(message.split(' ')) > count+50:
            message += '.'
            break

    return message
