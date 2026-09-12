import unittest
from utils import *
from typing import List, Dict, Set


class TestTASK1(unittest.TestCase):
    def test_convert_lowercase(self):
        self.assertEqual(convert_lowercase("Hello World"), "hello world")
        self.assertEqual(convert_lowercase("PYTHON"), "python")

    def test_remove_redundant_spaces(self):
        self.assertEqual(remove_redundant_spaces("  Hello    World  "), "Hello World")
        self.assertEqual(remove_redundant_spaces("Test  String"), "Test String")

    def test_remove_consecutive_spaces(self):
        self.assertEqual(remove_consecutive_spaces("Hello    World"), "Hello World")
        self.assertEqual(remove_consecutive_spaces("  Test    String  "), "Test String")

    def test_remove_prefix_suffix_spaces(self):
        self.assertEqual(remove_prefix_suffix_spaces("  Hello World  "), "Hello World")
        self.assertEqual(remove_prefix_suffix_spaces("Test"), "Test")

    def test_split_text_to_word(self):
        self.assertEqual(split_text_to_word("Hello World"), ["Hello", "World"])
        self.assertEqual(split_text_to_word("Python Unit Test"), ["Python", "Unit", "Test"])

    def test_remove_unwanted_words(self):
        words_to_remove = {"the", "is"}
        self.assertEqual(remove_unwanted_words("This is the test case", words_to_remove), "This test case")
        self.assertEqual(remove_unwanted_words("the quick brown fox", words_to_remove), "quick brown fox")

    def test_strs_to_seqs(self):
        self.assertEqual(strs_to_seqs(["Hello World", "Python Test"]), [["Hello", "World"], ["Python", "Test"]])
        self.assertEqual(strs_to_seqs(["Unit Testing", "Works"]), [["Unit", "Testing"], ["Works"]])

    def test_is_word_in_sentence(self):
        self.assertTrue(is_word_in_sentence("hello", "hello world"))
        self.assertFalse(is_word_in_sentence("python", "hello world"))

    def test_count_word_in_sentence(self):
        self.assertEqual(count_word_in_sentence("hello", "hello world hello"), 2)
        self.assertEqual(count_word_in_sentence("test", "this is a test case"), 1)

    def test_remove_word_file(self):
        with open("test_remove_words.csv", "w") as f:
            f.write("hello\nworld\n")
        self.assertEqual(remove_word_file("test_remove_words.csv"), {"hello", "world"})

    def test_sentences_file(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nHello world\n")
        self.assertEqual(sentences_file("test_sentences.csv"), [{"sentence": "Hello world"}])


if __name__ == "__main__":
    unittest.main()

