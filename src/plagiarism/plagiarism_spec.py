import unittest
from .plagiarism import *
import spacy

nlp = spacy.load('en_core_web_sm')


class test_build_plagiarism_trie(unittest.TestCase):
    def test_words_generator(self):
        words_gen = words(next(nlp("I coughed.").sents))
        self.assertEqual(next(words_gen).norm_, 'i')
        self.assertEqual(next(words_gen).norm_, 'coughed')
        self.assertEqual(next(words_gen).norm_, '.')
        final_iter = next(words_gen)
        self.assertEqual(final_iter.norm_, 'END')
        self.assertTrue(isinstance(final_iter, EndIter))

    def test_add_words_to_trie(self):
        test_sent = next(nlp("I want coffee.").sents)
        expected_trie = {
            'i': {'want': {'coffee': {'.': 'END'}}}
        }
        received_trie = add_words_to_trie(
            words(test_sent),
            {}
        )
        self.assertEqual(received_trie, expected_trie)

    def test_add_words_to_trie_combines_properly(self):
        trie_to_combine_with = {
            'a': {'b': 'END'},
            'i': {'want': {'to': {'help': {'!': 'END'}}}}
        }
        second_trie = add_words_to_trie(
            words(next(nlp('I want coffee.').sents)),
            trie_to_combine_with
        )
        expected_second_trie = {
            'a': {'b': 'END'},
            'i': {
                'want': {
                    'coffee': {'.': 'END'},
                    'to': {'help': {'!': 'END'}}
                }
            }
        }
        self.assertEqual(second_trie, expected_second_trie)

    def test_build_plagiarism_trie(self):
        test_doc = nlp('This is best. This is the best outcome.')
        result_trie = build_plagiarism_trie(test_doc)
        expected_trie = {
            'this': {'is': {
                'best': {'.': 'END'},
                'the': {'best': {'outcome': {'.': 'END'}}}
            }}
        }
        self.assertEqual(result_trie, expected_trie)

    def test_build_plagiarism_trie_combines_properly(self):
        test_doc = nlp('This is best. This is the best outcome.')
        initial_trie = {'this': {'one': {'time': 'END'}}}
        result_trie = build_plagiarism_trie(test_doc, initial_trie)
        expected_trie = {
            'this': {
                'is': {
                    'best': {'.': 'END'},
                    'the': {'best': {'outcome': {'.': 'END'}}}
                },
                'one': {'time': 'END'}
            }
        }
        self.assertEqual(result_trie, expected_trie)

    def test_is_sent_plagiarized(self):
        test_sent = next(nlp("I want coffee.").sents)
        test_trie = {
            'this': {
                'is': {
                    'best': {'.': 'END'},
                    'the': {'best': {'outcome': {'.': 'END'}}}
                },
                'one': {'time': 'END'}
            }
        }
        result = is_sent_plagiarized(test_sent, test_trie)
        self.assertFalse(result)

    def test_is_sent_plagiarized(self):
        test_sent1 = next(nlp("This is the best outcome.").sents)
        test_sent2 = next(nlp("this one time").sents)
        test_trie = {
            'this': {
                'is': {
                    'best': {'.': 'END'},
                    'the': {'best': {'outcome': {'.': 'END'}}}
                },
                'one': {'time': 'END'}
            }
        }
        result1 = is_sent_plagiarized(test_sent1, test_trie)
        result2 = is_sent_plagiarized(test_sent2, test_trie)
        self.assertTrue(result1)
        self.assertTrue(result2)
