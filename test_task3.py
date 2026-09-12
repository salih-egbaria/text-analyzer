import unittest
import json
import os
from task3 import TASK3
from utils import *
from typing import List, Dict, Set


class TestTASK3(unittest.TestCase):
    def test_count_word_in_sentence(self):
        self.assertEqual(count_word_in_sentence("John", "John is here. John likes coffee."), 2)
        self.assertEqual(count_word_in_sentence("Alice", "Alice went to the park. Alice loves nature."), 2)
        self.assertEqual(count_word_in_sentence("Bob", "Bob went home."), 1)
        self.assertEqual(count_word_in_sentence("Charlie", "This is a test case with no mention of the name."), 0)

    def test_sentences_file(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nJohn is here\nAlice went to the park\n")
        self.assertEqual(sentences_file("test_sentences.csv"), [
            {"sentence": "John is here"},
            {"sentence": "Alice went to the park"}
        ])

    def test_remove_word_file(self):
        with open("test_remove_words.csv", "w") as f:
            f.write("is\nthe\n")
        self.assertEqual(remove_word_file("test_remove_words.csv"), {"is", "the"})

    def test_task3_output_json(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nJohn is here\nAlice went to the park\n")


if __name__ == "__main__":
    unittest.main()
