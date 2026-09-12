import unittest
import json
import os
from task4 import TASK4
from utils import *
from typing import List, Dict, Set


class TestTASK4(unittest.TestCase):

    def test_sentences_file(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nHello world\nPython is great\n")
        self.assertEqual(sentences_file("test_sentences.csv"), [
            {"sentence": "Hello world"},
            {"sentence": "Python is great"}
        ])

    def test_remove_word_file(self):
        with open("test_remove_words.csv", "w") as f:
            f.write("is\nthe\n")
        self.assertEqual(remove_word_file("test_remove_words.csv"), {"is", "the"})

    def test_task4_with_sentence_file(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nHello world\nPython is great\n")

        with open("test_remove_words.csv", "w") as f:
            f.write("is\n")

        task = TASK4(sentence_path="test_sentences.csv", remove_word_path="test_remove_words.csv")

        expected_sentences = [
            ["hello", "world"],
            ["python", "great"]
        ]
        self.assertEqual(task.sentences_to_words, expected_sentences)

    def test_task4_with_preprocessed_file(self):
        preprocessed_data = {
            "Question 1": {
                "Processed Sentences": [["hello", "world"], ["python", "great"]]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        task = TASK4(preprocessed="test_preprocessed.json")
        expected_sentences = [
            ["hello", "world"],
            ["python", "great"]
        ]
        self.assertEqual(task.sentences_to_words, expected_sentences)

    def test_build_lookup_table(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nHello world\nPython is great\n")

        with open("test_remove_words.csv", "w") as f:
            f.write("is\n")

        task = TASK4(sentence_path="test_sentences.csv", remove_word_path="test_remove_words.csv")
        lookup_table = task.build_lookup_table()

        expected_lookup_table = {
            "hello": [["hello", "world"]],
            "world": [["hello", "world"]],
            "python": [["python", "great"]],
            "great": [["python", "great"]],
            "hello world": [["hello", "world"]],
            "python great": [["python", "great"]]
        }
        self.assertEqual(lookup_table, expected_lookup_table)

if __name__ == "__main__":
    unittest.main()
