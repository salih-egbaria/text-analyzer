from task1 import TASK1
from typing import Optional, Dict, List, Union
import json
from utils import count_word_in_sentence


class TASK3:
    def __init__(self, sentence_path: Optional[str] = None, people_path: Optional[str] = None,
                 remove_word_path: Optional[str] = None, preprocessed: Optional[str] = None):
        """
        :param sentence_path:  path to sentence file
        :param people_path:  path to people file
        :param remove_word_path:  path to unwanted words(remove word) file
        :param preprocessed: path to a preprocessed JSON file
        """
        if sentence_path and people_path and remove_word_path:
            data = TASK1(sentence_path=sentence_path, people_path=people_path,
                         remove_word_path=remove_word_path).get_processed_data()['Question 1']
        elif preprocessed:
            with open(preprocessed) as json_input:
                data = json.load(json_input)['Question 1']

        # combine all the list of words into a single string
        full_text: str = ''
        for sentence in data['Processed Sentences']:
            full_text += ' '.join(sentence)
            full_text += ' '

        result_count: Dict[str, int] = {}  # A list where we will save for each main name the count of appearances
        for person in data['Processed Names']:
            main_name = ' '.join(person[0])  # get the full name
            result_count[main_name] = 0

            all_names = []
            all_names += [' '.join(other_name) for other_name in person[1]]
            for j in range(1, len(person[0])):
                for i in range(len(person[0])):
                    if i + j > len(person[0]):
                        break
                    all_names.append(' '.join(person[0][i:i + j]))
            all_names.append(main_name)
            all_names.reverse()  # The main name comes first, then its partials, lastly the other names

            text_copy = full_text
            for name in all_names:
                result_count[main_name] += count_word_in_sentence(name, text_copy)
                text_copy.replace(name, '')  # remove the appearance so smaller partials don't count more than one

        # remove names that were not found in the text
        result_count = {name: count for name, count in result_count.items() if count != 0}

        result_to_print: List[List[Union[str, int]]] = []
        for name in sorted(result_count.keys()):
            result_to_print.append([name, result_count[name]])

        print(json.dumps({'Question 3': {'Name Mentions': result_to_print}}, indent=4))
