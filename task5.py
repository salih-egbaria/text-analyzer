from task1 import TASK1
from typing import Optional, List, Dict
import json

from utils import strs_to_seqs, all_names


class TASK5:
    def __init__(self, sentence_path: Optional[str] = None, people_path: Optional[str] = None,
                 remove_word_path: Optional[str] = None, preprocessed: Optional[str] = None, max_k: int = 3):
        """
        :param sentence_path: Path to the sentences file
        :param people_path: Path to the names file
        :param remove_word_path: path to unwanted words(remove word) file
        :param preprocessed: Path to a preprocessed JSON file
        :param max_k: max seq length
        """
        if sentence_path and people_path and remove_word_path:
            data = TASK1(sentence_path=sentence_path, people_path=people_path,
                         remove_word_path=remove_word_path).get_processed_data()['Question 1']
        elif preprocessed:
            with open(preprocessed) as json_input:
                data = json.load(json_input)['Question 1']

        self.processed_sentences = data['Processed Sentences']
        self.processed_names = data['Processed Names']
        self.max_k = max_k

        # generate k-sequence dictionary
        self.sentence_to_kseq: Dict['str', List[str]] = {}
        self.sentence_to_kseq_dictionary()

        # convert processed names to dictionary
        self.processed_names_dict: Dict[str, List[str]] = all_names(self.processed_names)

        self.mentions: Dict[str, List[str]] = {}

        for main_name, names in self.processed_names_dict.items():
            for name in names:
                for sentence in sorted(self.sentence_to_kseq.keys()):
                    if name in sentence:
                        if main_name in self.mentions.keys():
                            self.mentions[main_name].extend([*self.sentence_to_kseq[sentence]])
                        else:
                            self.mentions[main_name] = [*self.sentence_to_kseq[sentence]]
            if main_name in self.mentions.keys():
                self.mentions[main_name] = list(set(self.mentions[main_name]))
                self.mentions[main_name].sort()

        print(json.dumps({'Question 5': {
            'Person Contexts and K-Seqs': [[key, strs_to_seqs(self.mentions[key])] for key in
                                           sorted(self.mentions.keys())]}}, indent=4))

    def sentence_to_kseq_dictionary(self) -> None:
        # convert processed sentences to k_seq dict
        for sentence in self.processed_sentences:
            key = ' '.join(sentence)
            self.sentence_to_kseq[key] = []
            for seq_len in range(1, self.max_k + 1):
                for i in range(len(sentence) - seq_len + 1):
                    sequence = ' '.join(sentence[i:i + seq_len])
                    self.sentence_to_kseq[key].append(sequence)
            self.sentence_to_kseq[key].sort()

