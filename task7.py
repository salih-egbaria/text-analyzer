import json
from task6 import TASK6
from typing import Optional, Set, Dict, List


class TASK7:
    def __init__(self, window_size: int, threshold: int, pairs_file: str,
                 sentence_path: Optional[str] = None, people_path: Optional[str] = None,
                 remove_word_path: Optional[str] = None, preprocessed: Optional[str] = None):
        """
        :param window_size: Number of consecutive sentences in which to search for name co-occurrences
        :param threshold:  min number of co-occurrences required to consider a name pair significant
        :param sentence_path: Path to the sentences file
        :param people_path: Path to the names file
        :param remove_word_path: path to unwanted words(remove word) file
        :param preprocessed: Path to a preprocessed JSON file
        """

        self.maximal_distance: int = 0

        if preprocessed is None:
            self.connections = TASK6(window_size=window_size, threshold=threshold, sentence_path=sentence_path,
                                     people_path=people_path, remove_word_path=remove_word_path).get_result()
        else:
            with open(preprocessed, 'r') as json_file:
                self.connections = json.load(json_file)['Question 6']['Pair Matches']

        # load pairs
        with open(pairs_file, 'r') as json_file:
            self.pairs_to_check = json.load(json_file)['keys']
            self.pairs_to_check = sorted(tuple(sorted(pair)) for pair in self.pairs_to_check)

        valid_pairs = [(' '.join(pair[0]), ' '.join(pair[1])) for pair in self.connections]

        # dict to store direct connection
        self.direct_connection_dict: Dict[str, Set] = {}
        for p1, p2 in valid_pairs:
            if p1 not in self.direct_connection_dict.keys():
                self.direct_connection_dict[p1] = set()
            if p2 not in self.direct_connection_dict.keys():
                self.direct_connection_dict[p2] = set()
            self.direct_connection_dict[p1].add(p2)
            self.direct_connection_dict[p2].add(p1)

        self.result: List = []

    def fill_result(self, maximal_distance: int):
        """
        :param maximal_distance: max steps between 2 names to considered to be connected
        """
        self.maximal_distance = maximal_distance
        for pair in self.pairs_to_check:
            self.result.append([pair[0], pair[1], self.find_connection(pair[0], pair[1], 0, set())])

    def find_connection(self, source: str, target: str, length: int, visited: Set[str]):
        """
        :param source: start name
        :param target: the target name
        :param length: cur depth in search
        :param visited: to prevent cycles
        :return: True if connection exist ,False if not(otherwise)
        """
        if source == target:
            return True
        if length >= self.maximal_distance:
            return False
        if source not in self.direct_connection_dict.keys():
            return False

        visited.add(source)

        for person in self.direct_connection_dict[source]:
            if person not in visited:
                if self.find_connection(person, target, length + 1, visited):
                    return True

        visited.remove(source)
        return False

    def print_result(self):
        # prints in JSON format
        print(json.dumps({'Question 7': {'Pair Matches': self.result}}, indent=4))
