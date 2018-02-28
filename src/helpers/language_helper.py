

def stringify(token):
    if token.orth_ == 'I':
        return token.orth_
    elif token.ent_type_ == '':
        return token.lower_
    else:
        return token.orth_


def parse_stack(token):
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


def add_symbol_balance(doc):
    balance_points = _quote_balance(doc) #+ _punct_balance(doc)
    doc.user_data['balance_points'] = balance_points
    return doc


def _quote_balance(doc):
    balance_points = []
    quote_hash = {}
    for t in doc:
        if t.is_quote and quote_hash.get(t.orth) is None:
            quote_hash[t.orth] = t.i
        elif t.is_quote and quote_hash.get(t.orth) is not None:
            balance_points.append( (t.orth_, quote_hash[t.orth], t.i) )
            quote_hash[t.orth] = None
    return balance_points


def _punct_balance(doc):
    balance_points = []
    symbol_hash = {}
    for t in doc:
        if t.is_left_punct and not t.is_quote:
            symbol_hash[t.orth] = t.i
        elif t.is_right_punct and not t.is_quote:
            symbol = sorted(symbol_hash, key=lambda entry: symbol_hash[entry], reverse=True)[0]
            balance_points.append( (t.orth_, symbol_hash[symbol], t.i) )
            symbol_hash[symbol] = None
    return balance_points


def symbol_stack(token):
    balance_points = sorted(token.doc.user_data['balance_points'], key=lambda bal: bal[1], reverse=True)
    ti = token.i
    return [bal[0] for bal in balance_points if bal[1] <= ti and bal[2] >= ti]
