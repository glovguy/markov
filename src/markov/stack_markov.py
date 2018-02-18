import random
from language_helper import stack_transition


# ( 1st-gram, 2nd-gram, dep-level )
#               |
#               V
#      ( 1-gram, dep_level )

def build_chain(doc, chain = {}):
    index = 2
    doc_wo_spaces = [w for w in doc if not w.is_space]
    for word in doc_wo_spaces[index:]:
        key = (stringify(doc_wo_spaces[index-2]), stringify(doc_wo_spaces[index-1]), stack_transition(doc_wo_spaces[index-1]))
        value = (stringify(word), stack_transition(word))
        if key in chain:
            chain[key].append(value)
        else:
            chain[key] = [value]
        index += 1
    return chain


def generate_message(chain, count = 100):
    starting_place = random.choice(list(chain.keys()))
    while not starting_place[0].isalpha() and not starting_place[1].isalpha():
        starting_place = random.choice(list(chain.keys()))
    word1 = starting_place[0]
    word2 = starting_place[1]

    message = word1.capitalize() + ' ' + word2
    prev_tuple = starting_place
    word3 = ''

    while len(message.split(' ')) < count or not (word3 == '.' or word3 == '!' or word3 == '?'):
        if chain.get(prev_tuple):
            current_tuple = random.choice(chain[prev_tuple])
        else:
            current_tuple = random.choice(list(chain.keys()))
            while not current_tuple[0].isalpha():
                current_tuple = random.choice(list(chain.keys()))
        word3 = current_tuple[0]
        if not word3.isalpha() and not word3.islower():
            message += word3
        elif current_tuple[-1:] == ' "' or current_tuple[-1:] == " '":
            message += word3
        elif "'" in word3[:2]:
            message += word3
        elif prev_tuple[1] == '.' or prev_tuple[1] == '?' or prev_tuple[1] == '!':
            message += ' ' + word3.capitalize()
        else:
            message += ' ' + word3

        prev_tuple = (prev_tuple[1], word3, current_tuple[1])
        if len(message.split(' ')) > count+50:
            message += '.'
            break

    return message
