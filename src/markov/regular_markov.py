import random
from ..helpers.language_helper import stringify


def build_chain(doc, chain = {}):
    index = 2
    doc_wo_spaces = [w for w in doc if not w.is_space]
    for word in doc_wo_spaces[index:]:
        key = (stringify(doc_wo_spaces[index - 2]), stringify(doc_wo_spaces[index - 1]))
        value = stringify(word)
        if key in chain:
            chain[key].append(value)
        else:
            chain[key] = [value]
        index += 1
    return chain


def generate_message(chain, count = 100):
    starting_place = random.choice(list(chain.keys()))
    while not (starting_place[0].isalpha() and starting_place[1].isalpha()):
        starting_place = random.choice(list(chain.keys()))
    word1 = starting_place[0]
    word2 = starting_place[1]

    message = word1.capitalize() + ' ' + word2
    prev_tuple = starting_place
    word3 = ''
    message_list = [word1, word2]

    while len(message.split(' ')) < count or not (next_word == '.' or next_word == '!' or next_word == '?'):
        if chain.get(prev_tuple):
            next_word = random.choice(chain[prev_tuple])
        else:
            next_word = random.choice(list(chain.keys()))
            while next_word.isalpha():
                next_word = random.choice(list(chain.keys()))
        if not next_word.isalpha() and not next_word.islower():
            message += next_word
        elif "'" in next_word[:2]:
            message += next_word
        elif prev_tuple[-1:] == '.' or prev_tuple[-1:] == '?' or prev_tuple[-1:] == '!':
            message += next_word.capitalize()
        else:
            message += ' ' + next_word

        message_list.append(next_word)

        prev_tuple = prev_tuple[1:] + tuple([next_word])
        if len(message.split(' ')) > count+50:
            message += '.'
            break

    return message
