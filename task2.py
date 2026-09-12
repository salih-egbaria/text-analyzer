import json
from utils import *
from typing import Optional, Union


class TASK2:
    def __init__(self, k_seq: int, sentence_path: Optional[str] = None, remove_word_path: Optional[str] = None,
                 preprocessed: Optional[str] = None):
        """
        :param k_seq: max seq length
        :param sentence_path: sentence path
        :param remove_word_path: unwanted words(remove word path)
        :param preprocessed: path to a preprocessed JSON file
        """
        self.k_seq: int = k_seq
        self.sentences_to_words: List[List[str]] = []

        # processed sentence
        if sentence_path and remove_word_path:
            for sentence in sentences_file(sentence_path):
                sentence['sentence'] = convert_lowercase(sentence['sentence'])
                sentence['sentence'] = remove_punctuation(sentence['sentence'])
                sentence['sentence'] = remove_unwanted_words(sentence['sentence'], remove_word_file(remove_word_path))
                sentence['sentence'] = remove_redundant_spaces(sentence['sentence'])
                if sentence['sentence'] == '':
                    continue
                self.sentences_to_words.append(sentence['sentence'].split(' '))

        elif preprocessed:
            with open(preprocessed) as json_input:
                self.sentences_to_words = json.load(json_input)['Question 1']['Processed Sentences']

        result: Dict[str, Dict[str, int]] = {}
        for seq_len in range(1, self.k_seq + 1):
            result[f'{seq_len}_seq'] = {}
            for sen in self.sentences_to_words:
                for i in range(len(sen)):
                    sequence = ' '.join(sen[i:i + seq_len])
                    if len(sequence.split()) < seq_len:
                        continue
                    if sequence in result[f'{seq_len}_seq'].keys():
                        result[f'{seq_len}_seq'][sequence] += 1
                    else:
                        result[f'{seq_len}_seq'][sequence] = 1

        self.format_result: List[List[Union[str, List[str]]]] = []
        for seq_length, words_count in result.items():
            to_append: List = []
            for seq in sorted(words_count.keys()):
                to_append.append([seq, words_count[seq]])
            self.format_result.append([seq_length, to_append])

        with open("task2.json", "w") as file:
            json.dump({'Question 2': {f'{self.k_seq}-Seq Counts': self.format_result}}, file, indent=4)

    def print_result(self):
        print(json.dumps({'Question 2': {f'{self.k_seq}-Seq Counts': self.format_result}}, indent=4))

    def get_result(self) -> List[List[Union[str, List[str]]]]:
        return self.format_result
