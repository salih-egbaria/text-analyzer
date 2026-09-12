import csv
from typing import List, Set, Dict
import re

NUMBERS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyz"


# a
def convert_lowercase(text: str) -> str:
    # Convert to lowercase
    text = text.lower()
    return text


# b
def remove_punctuation(text: str) -> str:
    # Replace punctuation with spaces
    res = []
    for char in text:
        if char in NUMBERS or char in LETTERS:
            res.append(char)
        else:
            res.append(" ")
    text_with_string = ''.join(res).strip()
    return text_with_string


def remove_redundant_spaces(text: str) -> str:
    # remove redundant spaces
    return remove_consecutive_spaces(remove_prefix_suffix_spaces(text))


# d
def remove_consecutive_spaces(text: str) -> str:
    # Remove Consecutive Whitespaces:
    if "  " in text:
        while "  " in text:
            text = text.replace("  ", " ")
    return text.strip()


# e
def remove_prefix_suffix_spaces(data: str) -> str:
    # remove whitespace suffix and prefix
    data = data.strip()
    return data


def split_text_to_word(text: str) -> List[str]:
    # split the text into words
    return text.split(' ')


def names_file(people_path: str) -> List[Dict[str, str]]:
    with open(people_path, 'r') as file:
        return list(csv.DictReader(file))


def remove_word_file(remove_word_path: str) -> Set[str]:
    result: Set[str] = set()
    with open(remove_word_path, 'r') as file:
        words = csv.reader(file)
        for word in words:
            if len(word) > 0:
                result.add(word[0].strip().lower())
    return result


def sentences_file(sentence_path: str) -> List[Dict[str, str]]:
    with open(sentence_path, 'r') as file:
        return list(csv.DictReader(file))


def remove_unwanted_words(text: str, words_to_remove: set[str]) -> str:
    # filter unwanted words
    words: List[str] = text.split()
    filtered_words: List[str] = [word for word in words if word not in words_to_remove]
    return " ".join(filtered_words)


def strs_to_seqs(text: List[str]) -> List[List[str]]:
    # convert list into seq
    return [str_seq.split() for str_seq in text]


def all_names(processed_names) -> Dict[str, List[str]]:
    # Extract all name variations
    processed_names_dict: Dict[str, List[str]] = {}
    for person in processed_names:
        main_name = ' '.join(person[0])
        processed_names_dict[main_name] = []

        processed_names_dict[main_name] += [' '.join(other_name) for other_name in person[1]]
        for j in range(1, len(person[0])):
            for i in range(len(person[0])):
                if i + j > len(person[0]):
                    break
                processed_names_dict[main_name].append(' '.join(person[0][i:i + j]))
        processed_names_dict[main_name].append(main_name)
        processed_names_dict[main_name].reverse()
    return processed_names_dict


def is_word_in_sentence(word: str, sentence: str) -> bool:
    # check if word exist in sentence
    return bool(re.search(rf'\b{re.escape(word)}\b', sentence))


def count_word_in_sentence(word: str, sentence: str) -> int:
    return len(re.findall(rf'\b{re.escape(word)}\b', sentence))
