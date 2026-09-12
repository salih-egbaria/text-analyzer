import json
from typing import Union
from utils import *


class TASK1:

    def __init__(self, sentence_path: str, people_path: str, remove_word_path: str):
        """
        :param sentence_path: sentence path
        :param people_path: people path
        :param remove_word_path: unwanted word (remove word path)
        """
        self.words_to_remove: Set[str] = remove_word_file(remove_word_path)
        self.names: List[Dict[str, str]] = names_file(people_path)

        self.names_split: List[List[str]] = []
        self.other_names_split: List[List[List[str]]] = [[] for _ in range(len(self.names))]
        self.sentences_to_words: List[List[str]] = []

        # process names
        for i, person in enumerate(self.names):
            person['Name'] = convert_lowercase(person['Name'])
            person['Name'] = remove_punctuation(person['Name'])
            person['Name'] = remove_unwanted_words(person['Name'], self.words_to_remove)
            person['Name'] = remove_redundant_spaces(person['Name'])
            if person['Name'] == '':
                continue
            self.names_split.append(split_text_to_word(person['Name']))

            # process additional names
            for other_name in person['Other Names'].split(','):
                other_name = convert_lowercase(other_name)
                other_name = remove_punctuation(other_name)
                other_name = remove_unwanted_words(other_name, self.words_to_remove)
                other_name = remove_redundant_spaces(other_name)
                other_name_to_list = other_name.split(' ')
                if other_name_to_list == ['']:
                    continue
                # f
                self.other_names_split[i].append(other_name_to_list)

        for sentence in sentences_file(sentence_path):
            sentence['sentence'] = convert_lowercase(sentence['sentence'])
            sentence['sentence'] = remove_punctuation(sentence['sentence'])
            sentence['sentence'] = remove_unwanted_words(sentence['sentence'], self.words_to_remove)
            sentence['sentence'] = remove_redundant_spaces(sentence['sentence'])
            # i
            if sentence['sentence'] == '':
                continue
            # h
            self.sentences_to_words.append(sentence['sentence'].split(' '))

        # j
        # filter duplicate names
        self.filtered_names_split: List[List] = []
        self.filter_names()

    def filter_names(self) -> None:
        cleared_names: List[str] = [" ".join(name) for name in self.names_split]
        filtered_names: Set[str] = set()

        for i, name in enumerate(cleared_names):
            if name not in filtered_names:
                filtered_names.add(name)
                self.filtered_names_split.append([self.names_split[i]] + [self.other_names_split[i]])

    def print_result(self) -> None:
        print(json.dumps(self.get_processed_data(), indent=4))

    def get_processed_data(self) -> Dict[str, Dict]:
        return {'Question 1': {'Processed Sentences': self.sentences_to_words,
                               'Processed Names': self.filtered_names_split}}
