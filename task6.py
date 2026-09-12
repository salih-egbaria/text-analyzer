from utils import *
from typing import Optional, Tuple
from task1 import TASK1
import json
from utils import all_names, is_word_in_sentence


class TASK6:
    def __init__(self, window_size: int, threshold: int, sentence_path: Optional[str] = None,
                 people_path: Optional[str] = None, remove_word_path: Optional[str] = None,
                 preprocessed: Optional[str] = None):
        """

        :param window_size: Number of consecutive sentences in which to search for name co-occurrences
        :param threshold:  min number of co-occurrences required to consider a name pair significant
        :param sentence_path: Path to the sentences file
        :param people_path: Path to the names file
        :param remove_word_path: path to unwanted words(remove word) file
        :param preprocessed: Path to a preprocessed JSON file
        """

        self.threshold = threshold

        if sentence_path and people_path and remove_word_path:
            data = TASK1(sentence_path=sentence_path, people_path=people_path,
                         remove_word_path=remove_word_path).get_processed_data()['Question 1']
        elif preprocessed:
            with open(preprocessed) as json_input:
                data = json.load(json_input)['Question 1']

        self.processed_sentences = data['Processed Sentences']
        self.processed_names = data['Processed Names']

        # combine sentence into a text
        sentences = [' '.join(sentence) for sentence in self.processed_sentences]

        self.all_names = all_names(self.processed_names)

        all_windows = []
        for i in range(len(sentences) - window_size + 1):
            all_windows.append(' '.join(sentences[i:i + window_size]))

        # identify names appearing in each window
        self.names_in_window: Dict[str, List[str]] = {}
        for window in all_windows:
            self.names_in_window[window] = []
            for main_name, names in self.all_names.items():
                for name in names:
                    if is_word_in_sentence(name, window):
                        self.names_in_window[window].append(main_name)
                        break

        self.pairs: Dict[Tuple, int] = {}

        for person1 in sorted(self.all_names.keys()):
            for person2 in sorted(self.all_names.keys()):
                if person2 <= person1:
                    continue
                pair_key = tuple([person1, person2])
                for window, names in self.names_in_window.items():
                    if person1 in names and person2 in names:
                        if pair_key in self.pairs.keys():
                            self.pairs[pair_key] += 1
                        else:
                            self.pairs[pair_key] = 1

    def get_result(self):
        return [[key[0].split(), key[1].split()] for key in sorted(self.pairs.keys()) if
                self.pairs[key] >= self.threshold]

    def print_result(self):
        # prints in JSON format
        print(json.dumps({'Question 6': {'Pair Matches': self.get_result()}}, indent=4))
