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

    def test_symbol_label_includes_quote_mark(self):
        doc = nlp("""\"Yes," he replied.""")
        print(doc.user_data)
        print(doc[0])
        print(doc[3])
        self.assertEqual(symbol_label(doc[0]), '"')
        self.assertEqual(symbol_label(doc[3]), '"')

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
        self.assertEqual(stack_label(doc[7]), '"_ccomp')

    def test_stack_label_with_quote_depth(self):
        doc = nlp("""They exclaimed, "no more 'coffee' quote!\"""")
        self.assertEqual(stack_label(doc[6]), '\'"_nmod')
        self.assertEqual(stack_label(doc[4]), '\"_amod')
