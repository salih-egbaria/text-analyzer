import unittest
import json
import os
from task9 import TASK9
from utils import *
from typing import List, Dict


class TestTASK9(unittest.TestCase):
    def test_sentences_file(self):
        """Test reading sentences from a CSV file."""
        with open("test_sentences.csv", "w") as f:
            f.write("sentence\nSalih loves AI\nEgbaria studies AI\nAI is powerful\n")
        self.assertEqual(sentences_file("test_sentences.csv"), [
            {"sentence": "Salih loves AI"},
            {"sentence": "Egbaria studies AI"},
            {"sentence": "AI is powerful"}
        ])

    def test_remove_word_file(self):
        """Test loading unwanted words from a file."""
        with open("test_remove_words.csv", "w") as f:
            f.write("is\n")
        self.assertEqual(remove_word_file("test_remove_words.csv"), {"is"})

    def test_task9_with_preprocessed_file(self):
        """Test TASK9 initialization using a preprocessed JSON file."""
        preprocessed_data = {
            "Question 1": {
                "Processed Sentences": [
                    ["salih", "loves", "ai"],
                    ["egbaria", "studies", "ai"],
                    ["ai", "powerful"]
                ]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        task = TASK9(threshold=1, preprocessed="test_preprocessed.json")

        expected_sentences = [
            ["salih", "loves", "ai"],
            ["egbaria", "studies", "ai"],
            ["ai", "powerful"]
        ]
        self.assertEqual(task.sentences_to_words, expected_sentences)

    def test_sort_groups(self):
        preprocessed_data = {
            "Question 1": {
                "Processed Sentences": [
                    ["ai", "powerful"],
                    ["salih", "loves", "ai"],
                    ["egbaria", "studies", "ai"]
                ]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        task = TASK9(threshold=1, preprocessed="test_preprocessed.json")
        task.sort_groups()

        expected_sorted_groups = [
            ["ai powerful", "egbaria studies ai", "salih loves ai"]
        ]
        self.assertEqual(task.groups_sentences, expected_sorted_groups)


if __name__ == "__main__":
    unittest.main()
