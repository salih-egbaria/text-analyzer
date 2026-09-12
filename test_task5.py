import unittest
import json
import os
from task5 import TASK5
from utils import *
from typing import List, Dict


class TestTASK5(unittest.TestCase):
    def test_sentences_file(self):
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nSalih studies AI\nEgbaria develops software\n")
        self.assertEqual(sentences_file("test_sentences.csv"), [
            {"sentence": "Salih studies AI"},
            {"sentence": "Egbaria develops software"}
        ])

    def test_remove_word_file(self):
        """Test loading unwanted words from a file."""
        with open("test_remove_words.csv", "w") as f:
            f.write("studies\ndevelops\n")
        self.assertEqual(remove_word_file("test_remove_words.csv"), {"studies", "develops"})

    def test_task5_with_preprocessed_file(self):
        preprocessed_data = {
            "Question 1": {
                "Processed Sentences": [["salih", "ai"], ["egbaria", "software"]],
                "Processed Names": [
                    [["salih"], [["egbaria"]]],
                    [["egbaria"], [["salih"]]]
                ]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        task = TASK5(preprocessed="test_preprocessed.json", max_k=3)

        expected_sentences = [
            ["salih", "ai"],
            ["egbaria", "software"]
        ]
        self.assertEqual(task.processed_sentences, expected_sentences)


if __name__ == "__main__":
    unittest.main()
