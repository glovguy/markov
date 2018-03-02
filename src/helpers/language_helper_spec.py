import unittest
from .language_helper import *
import spacy

_nlp = spacy.load('en_core_web_sm')
nlp = lambda text: add_symbol_balance(_nlp(text))


class test_span_is_only_whitespace(unittest.TestCase):
    def test_it_is_true_for_whitespace(self):
        doc = nlp("\n\t\n")
        self.assertEqual(span_is_only_whitespace(doc[0:]), True)

    def test_it_is_false_for_span_with_characters(self):
        doc = nlp("\n\"And Socrates said...\"\n")
        self.assertEqual(span_is_only_whitespace(doc[0:]), False)


class test_quote_balance(unittest.TestCase):
    def test_regular_sentence(self):
        doc = nlp("\n\"And Socrates said...\"\n")
        self.assertEqual(quote_balance(doc), [('"', 1, 6)])

    def test_quote_between_paragraphs(self):
        doc = nlp('And Socrates said...\"\n\"')
        self.assertEqual(quote_balance(doc), [])
