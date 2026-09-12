import json
from task7 import TASK7
from typing import Optional, Set, List


class TASK8:
    def __init__(self, window_size: int, threshold: int, pairs_file: str, fixed_length: int,
                 sentence_path: Optional[str] = None, people_path: Optional[str] = None,
                 remove_word_path: Optional[str] = None, preprocessed: Optional[str] = None):
        """
        :param window_size: Number of consecutive sentences in which to search for name co-occurrences
        :param threshold:  min number of co-occurrences required to consider a name pair significant
        :param pairs_file: pairs of names to check connection
        :param fixed_length: the exact num of steps
        :param sentence_path: Path to the sentences file
        :param people_path: Path to the names file
        :param remove_word_path: path to unwanted words(remove word) file
        :param preprocessed: Path to a preprocessed JSON file
        """
        task = TASK7(window_size=window_size, threshold=threshold, pairs_file=pairs_file,
                     sentence_path=sentence_path, people_path=people_path, remove_word_path=remove_word_path,
                     preprocessed=preprocessed)
        self.fixed_length: int = fixed_length
        self.pairs_to_check = task.pairs_to_check
        self.direct_connection_dict = task.direct_connection_dict
        self.result: List = []
        self.fill_result()
        self.print_result()

    def fill_result(self):
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
        if source not in self.direct_connection_dict.keys():
            return False
        if length == self.fixed_length:
            return target == source

        visited.add(source)

        for person in self.direct_connection_dict[source]:
            if person not in visited:
                if self.find_connection(person, target, length + 1, visited):
                    return True

        visited.remove(source)
        return False

    def print_result(self):
        # prints the result in JSON format
        print(json.dumps({'Question 8': {'Pair Matches': self.result}}, indent=4))
