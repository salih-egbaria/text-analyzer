import unittest
import json
import os
from task7 import TASK7
from utils import *
from typing import List, Dict


class TestTASK7(unittest.TestCase):
    def test_load_pairs_file(self):
        pairs_data = {
            "keys": [
                [["salih"], ["egbaria"]],
                [["ahmed"], ["mohammed"]]
            ]
        }
        with open("test_pairs.json", "w") as f:
            json.dump(pairs_data, f)

        with open("test_pairs.json", "r") as f:
            data = json.load(f)

        expected_pairs = sorted(tuple(sorted(pair)) for pair in pairs_data["keys"])
        self.assertEqual(expected_pairs, sorted(tuple(sorted(pair)) for pair in data["keys"]))

    def test_task7_with_preprocessed_file(self):
        preprocessed_data = {
            "Question 6": {
                "Pair Matches": [
                    [["salih"], ["egbaria"]],
                    [["ahmed"], ["mohammed"]]
                ]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        pairs_data = {
            "keys": [
                [["salih"], ["egbaria"]],
                [["ahmed"], ["mohammed"]]
            ]
        }
        with open("test_pairs.json", "w") as f:
            json.dump(pairs_data, f)

        task = TASK7(window_size=2, threshold=1, pairs_file="test_pairs.json", preprocessed="test_preprocessed.json")

        expected_connections = [
            [["salih"], ["egbaria"]],
            [["ahmed"], ["mohammed"]]
        ]
        self.assertEqual(task.connections, expected_connections)

    def test_direct_connection_dict(self):
        preprocessed_data = {
            "Question 6": {
                "Pair Matches": [
                    [["salih"], ["egbaria"]],
                    [["ahmed"], ["mohammed"]]
                ]
            }
        }
        with open("test_preprocessed.json", "w") as f:
            json.dump(preprocessed_data, f)

        pairs_data = {
            "keys": [
                [["salih"], ["egbaria"]],
                [["ahmed"], ["mohammed"]]
            ]
        }
        with open("test_pairs.json", "w") as f:
            json.dump(pairs_data, f)

        task = TASK7(window_size=2, threshold=1, pairs_file="test_pairs.json", preprocessed="test_preprocessed.json")

        expected_direct_connections = {
            "salih": {"egbaria"},
            "egbaria": {"salih"},
            "ahmed": {"mohammed"},
            "mohammed": {"ahmed"}
        }
        self.assertEqual(task.direct_connection_dict, expected_direct_connections)

if __name__ == "__main__":
    unittest.main()
