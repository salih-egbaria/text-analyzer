import unittest
import json
import os
from task8 import TASK8
from utils import *
from typing import List, Dict


class TestTASK8(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
