import unittest
from .stack_markov import *
import spacy

_nlp = spacy.load('en_core_web_sm')
nlp = lambda text: add_symbol_balance(_nlp(text))


class test_stack_labels(unittest.TestCase):
    def test_symbol_label_of_non_quoted_sentence(self):
        doc = nlp("I've always thought it wasn't a good idea.")
        for eachToken in doc:
            self.assertEqual(symbol_label(eachToken), '')

    def test_symbol_label_of_one_depth(self):
        doc = nlp("""He said "pretty please," but I just said 'no way!'""")
        self.assertEqual(symbol_label(doc[3]), '"')
        self.assertEqual(symbol_label(doc[12]), "'")

    def test_symbol_label_transition(self):
        doc = nlp("""\"Yes," he replied.""")
        self.assertEqual(symbol_label(doc[0]), 'in_"')
        self.assertEqual(symbol_label(doc[3]), 'out_"')

    def test_symbol_label_with_depth(self):
        doc = nlp("""He said "no reason to 'hate' on me like that!\"""")
        self.assertEqual(symbol_label(doc[7]), '\'"')


class test_parse_label(unittest.TestCase):
    def test_parse_label(self):
        doc = nlp("I want that coffee.")
        self.assertEqual(parse_label(doc[1]), 'ROOT')
        self.assertEqual(parse_label(doc[2]), 'dobj')
        self.assertEqual(parse_label(doc[3]), 'dobj')


class test_stack_label(unittest.TestCase):
    def test_stack_label_with_no_symbol_label(self):
        doc = nlp("It's far too late for that.")
        self.assertEqual(stack_label(doc[1]), 'ROOT')
        self.assertEqual(stack_label(doc[5]), 'prep')

    def test_stack_label_with_a_quote(self):
        doc = nlp("""I want to say, "I want coffee," but that should be obvious.""")
        self.assertEqual(stack_label(doc[0]), 'ROOT')
        self.assertEqual(stack_label(doc[7]), '"__ccomp')

    def test_stack_label_with_quote_depth(self):
        doc = nlp("""They exclaimed, "no more 'coffee' quote!\"""")
        self.assertEqual(stack_label(doc[7]), '\'"__nmod')
        self.assertEqual(stack_label(doc[4]), '\"__amod')

class test_is_valid_quote_mark(unittest.TestCase):
    def test_invalid_quote(self):
        token = nlp('One "two" three" four')[5]
        all_quote_points = [1, 3]
        self.assertEqual(is_valid_quote_mark(token, all_quote_points), False)

    def test_valid_quotes(self):
        doc = nlp('One "two" three" four')
        add_symbol_balance(doc)
        token1 = doc[1]
        token2 = doc[3]
        all_quote_points = [1, 3]
        self.assertEqual(is_valid_quote_mark(token1, all_quote_points), True)
        self.assertEqual(is_valid_quote_mark(token2, all_quote_points), True)
