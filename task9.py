from utils import *
from typing import Optional
import json


class TASK9:
    def __init__(self, threshold: int, sentence_path: Optional[str] = None, remove_word_path: Optional[str] = None,
                 preprocessed: Optional[str] = None):
        """
        :param threshold:  min number of co-occurrences required to consider a name pair significant
        :param sentence_path: Path to the sentences file
        :param remove_word_path: path to unwanted words(remove word) file
        :param preprocessed: Path to a preprocessed JSON file
        """

        self.threshold = threshold
        self.sentences_to_words: List[List[str]] = []

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

        # create a graph of sentence connection
        sentences_num = len(self.sentences_to_words)
        self.graph: Dict[int, List[int]] = {i: [] for i in range(sentences_num)}
        for i in range(sentences_num):
            for j in range(i + 1, sentences_num):
                if self.check_union(self.sentences_to_words[i], self.sentences_to_words[j]):
                    self.graph[i].append(j)
                    self.graph[j].append(i)

        self.groups = []
        self.visited: Set = set()
        for i in range(sentences_num):
            if i not in self.visited:
                self.groups.append(self.build_group([i]))

        # convert into sentence text
        self.groups_sentences: List[List[str]] = []
        for group in self.groups:
            group_sentences = [' '.join(self.sentences_to_words[sen_idx]) for sen_idx in group]
            self.groups_sentences.append(sorted(group_sentences))

        self.sort_groups()

        self.result = []
        for i, grp in enumerate(self.groups_sentences):
            sentences = [sentence.split() for sentence in grp]
            self.result.append([f'Group {i+1}', sentences])

        # save the result
        with open("task9.json", "w") as file:
            json.dump({'Question 9': {'group Matches': self.result}}, file, indent=4)

    def print_result(self):
        # prints into JSON file
        print(json.dumps({'Question 9': {'group Matches': self.result}}, indent=4))

    def check_union(self, sentence1: List[str], sentence2: List[str]) -> bool:
        """
        Checks if two sentences share at least `threshold` words.
        :param sentence1: first sentence
        :param sentence2: second sentence
        :return: True if the number of common words meets the threshold, otherwise False
        """
        sen1_set = set(sentence1)
        sen2_set = set(sentence2)
        return len(sen1_set.intersection(sen2_set)) >= self.threshold

    def build_group(self, nodes: List[int]) -> List[int]:
        """
        :param nodes: list of sentence
        :return: List of indices forming a connected group
        """
        group: List[int] = []
        while len(nodes) > 0:
            current_node = nodes.pop()
            if current_node not in self.visited:
                group.append(current_node)
                self.visited.add(current_node)
                nodes += self.graph[current_node]
        return group

    def sort_groups(self):
        for i in range(len(self.groups_sentences)):
            for j in range(i + 1, len(self.groups_sentences)):
                if len(self.groups_sentences[i]) > len(self.groups_sentences[j]) or (
                        len(self.groups_sentences[i]) == len(self.groups_sentences[j]) and self.groups_sentences[i] >
                        self.groups_sentences[j]):
                    self.groups_sentences[i], self.groups_sentences[j] = self.groups_sentences[j], \
                        self.groups_sentences[i]
