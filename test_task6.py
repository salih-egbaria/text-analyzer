import unittest
import json
import os
from task6 import TASK6
from utils import *
from typing import List, Dict


class TestTASK6(unittest.TestCase):
    def test_sentences_file(self):
        """Test reading sentences from a CSV file."""
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nSalih studies AI\nEgbaria develops software\nSalih and Egbaria collaborate on projects\n")
        self.assertEqual(sentences_file("test_sentences.csv"), [
            {"sentence": "Salih studies AI"},
            {"sentence": "Egbaria develops software"},
            {"sentence": "Salih and Egbaria collaborate on projects"}
        ])

    def test_remove_word_file(self):
        """Test loading unwanted words from a file."""
        with open("test_remove_words.csv", "w") as f:
            f.write("and\non\n")
        self.assertEqual(remove_word_file("test_remove_words.csv"), {"and", "on"})

    def test_task6_with_preprocessed_file(self):
        """Test TASK6 initialization using a preprocessed JSON file."""
        preprocessed_data = {
            "Question 1": {
                "Processed Sentences": [["salih", "studies", "ai"], ["egbaria", "develops", "software"],
                                        ["salih", "egbaria", "collaborate", "projects"]],
                "Processed Names": [
                    [["salih"], [["sal"]]],
                    [["egbaria"], [["egb"]]]
                ]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        task = TASK6(window_size=2, threshold=1, preprocessed="test_preprocessed.json")

        expected_sentences = [
            ["salih", "studies", "ai"],
            ["egbaria", "develops", "software"],
            ["salih", "egbaria", "collaborate", "projects"]
        ]
        self.assertEqual(task.processed_sentences, expected_sentences)

if __name__ == "__main__":
    unittest.main()
