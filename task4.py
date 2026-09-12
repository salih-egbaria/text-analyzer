import json
from typing import Optional, Union
from collections import defaultdict
from utils import *


class TASK4:
    def __init__(self, sentence_path: Optional[str] = None, remove_word_path: Optional[str] = None,
                 preprocessed: Optional[str] = None):
        """
        :param sentence_path: path to sentence file
        :param remove_word_path: path to unwanted words(remove word) file
        :param preprocessed: path to a preprocessed JSON file
        """
        self.sentences_to_words: List[List[str]] = []
        self.remove_word_path: Optional[str] = remove_word_path

        sentences: List[str] = []
        if sentence_path and remove_word_path:
            for sentence in sentences_file(sentence_path):
                sentence['sentence'] = convert_lowercase(sentence['sentence'])
                sentence['sentence'] = remove_punctuation(sentence['sentence'])
                sentence['sentence'] = remove_unwanted_words(sentence['sentence'], remove_word_file(remove_word_path))
                sentence['sentence'] = remove_redundant_spaces(sentence['sentence'])
                if sentence['sentence'] == '':
                    continue
                sentences.append(sentence['sentence'])
        elif preprocessed:
            with open(preprocessed) as json_input:
                sentences_to_words = json.load(json_input)['Question 1']['Processed Sentences']
                for sentence in sentences_to_words:
                    sentences.append(' '.join(sentence))
        sentences.sort()
        for sen in sentences:
            self.sentences_to_words.append(sen.split(' '))

        self.lookup_table: Dict[str, List[List[str]]] = self.build_lookup_table()

    def build_lookup_table(self) -> Dict[str, List[List[str]]]:
        """
        Build a dictionary where:
        - Key: k_seq (tuple of words)
        - Value: List of sentences containing the sequence
        """
        lookup_table: Dict[str, List[List[str]]] = defaultdict(list)
        seen_sentences: Dict[str, set] = defaultdict(set)

        for sentence in self.sentences_to_words:
            current_max_k = len(sentence)
            for k in range(1, current_max_k + 1):
                for i in range(current_max_k - k + 1):
                    kseq = ' '.join(sentence[i:i + k])
                    sentence_tuple = tuple(sentence)
                    if sentence_tuple not in seen_sentences[kseq]:
                        lookup_table[kseq].append(sentence)
                        seen_sentences[kseq].add(sentence_tuple)
        return lookup_table

    def basic_search(self, qsek_query_path: str):
        """
        :param qsek_query_path: path to query JSON file
        :return: None
        """
        processed_keys: List[str] = []
        with open(qsek_query_path) as json_input:
            keys = json.load(json_input)['keys']
        for key in keys:
            sentence = ' '.join(key)
            sentence = convert_lowercase(sentence)
            sentence = remove_punctuation(sentence)
            if self.remove_word_path:
                sentence = remove_unwanted_words(sentence, remove_word_file(self.remove_word_path))
            sentence = remove_redundant_spaces(sentence)
            if sentence == '':
                continue
            processed_keys.append(sentence)
        processed_keys = list(set(processed_keys))
        processed_keys.sort()

        result: List[List[Union[str, List[list[str]]]]] = []
        for key in processed_keys:
            if key in self.lookup_table:
                result.append([key, self.lookup_table[key]])

        print(json.dumps({'Question 4': {'K-Seq Matches': result}}, indent=4))
