

def stringify(token):
    if token.orth_ == 'I':
        return token.orth_
    elif token.ent_type_ == '':
        return token.lower_
    else:
        return token.orth_


def parse_stack(token): #should add balancing for parentheses, etc.
    stack = []
    if token.n_lefts + token.n_rights > 0:
        stack.append(token.dep_)
    child = token
    parent = child.head
    while parent != child:
        stack.append(parent.dep_)
        child = parent
        parent = child.head
    if len(stack) == 0:
        return ['']
    return stack


def stack_transition(token):
    current_stack = parse_stack(token)
    if len(current_stack[:1]) == 0: #THIS DOESN"T SEEM RIGHT
        print(token)
        print(token.i)
    base_dep = current_stack[:1][0]
    if token.is_sent_start or token.i == 0:
        return 'in_' + base_dep
    if token.i == len(token.doc)-1:
        return 'out_' + base_dep
    prev_stack = parse_stack(token.nbor(-1))
    next_stack = parse_stack(token.nbor(1))
    if len(prev_stack) < len(current_stack):
        return 'in_' + base_dep
    if len(current_stack) > len(next_stack):
        return 'out_' + base_dep
    return base_dep


def is_full_sentence(span):
    subject_present = False
    verb_present = False
    for token in span:
        if token.dep_ == 'nsubj':
            subject_present = True
        if token.pos_ == 'VERB':
            verb_present = True
        if subject_present and verb_present:
            return True
    return False


def closing_punct(sent):
    final_word = sent[-1:]
    if not (final_word == '.' or final_word == '!' or final_word == '?'):
        return sent + '.'
    return sent


def parse_complexity(span):
    return len(set([parse_stack(t)[0] for t in span]))