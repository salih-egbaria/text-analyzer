import unittest
import json
import os
from task2 import TASK2
from utils import *
from typing import List, Dict, Set


class TestTASK2(unittest.TestCase):
    def test_convert_lowercase(self):
        self.assertEqual(convert_lowercase("Hello World"), "hello world")
        self.assertEqual(convert_lowercase("PYTHON"), "python")

    def test_remove_redundant_spaces(self):
        self.assertEqual(remove_redundant_spaces("  Hello    World  "), "Hello World")
        self.assertEqual(remove_redundant_spaces("Python    is   great"), "Python is great")

    def test_remove_unwanted_words(self):
        words_to_remove = {"is", "the"}
        self.assertEqual(remove_unwanted_words("This is the test case", words_to_remove), "This test case")
        self.assertEqual(remove_unwanted_words("the quick brown fox", words_to_remove), "quick brown fox")

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

    def test_task2_with_sentence_file(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nHello world\nPython is great\n")

        with open("test_remove_words.csv", "w") as f:
            f.write("is\n")

        task = TASK2(k_seq=2, sentence_path="test_sentences.csv", remove_word_path="test_remove_words.csv")
        result = task.get_result()
        expected_result = [
            ["1_seq", [["great", 1], ["hello", 1], ["python", 1], ["world", 1]]],
            ["2_seq", [["hello world", 1], ["python great", 1]]]
        ]
        self.assertEqual(result, expected_result)

    def test_task2_with_preprocessed_file(self):
        preprocessed_data = {
            "Question 1": {
                "Processed Sentences": [["hello", "world"], ["python", "great"]]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        task = TASK2(k_seq=2, preprocessed="test_preprocessed.json")
        result = task.get_result()
        expected_result = [
            ["1_seq", [["great", 1], ["hello", 1], ["python", 1], ["world", 1]]],
            ["2_seq", [["hello world", 1], ["python great", 1]]]
        ]
        self.assertEqual(result, expected_result)

    def test_task2_output_json(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nHello world\nPython is great\n")

        with open("test_remove_words.csv", "w") as f:
            f.write("is\n")

        task = TASK2(k_seq=2, sentence_path="test_sentences.csv", remove_word_path="test_remove_words.csv")

        self.assertTrue(os.path.exists("task2.json"), "task2.json was not created")

        with open("task2.json", "r") as f:
            data = json.load(f)

        self.assertIn("Question 2", data)
        self.assertIn("2-Seq Counts", data["Question 2"])
        self.assertEqual(data["Question 2"]["2-Seq Counts"], task.get_result())


if __name__ == "__main__":
    unittest.main()
