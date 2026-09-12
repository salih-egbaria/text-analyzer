#!/usr/bin/env python3

import argparse
from task1 import TASK1
from task2 import TASK2
from task3 import TASK3
from task4 import TASK4
from task5 import TASK5
from task6 import TASK6
from task7 import TASK7
from task8 import TASK8
from task9 import TASK9
import sys
import os
import json
import csv


def is_valid_csv_path(path: str) -> bool:
    return os.path.isfile(path) and path.endswith('.csv')


def is_valid_json_path(path: str) -> bool:
    return os.path.isfile(path) and path.endswith('.json')


def is_valid_task_number(task: str) -> bool:
    return task.isdigit() and 1 <= int(task) <= 9


def check_columns_in_csv(csv_file, required_columns):
    try:
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)

        missing_columns = [col for col in required_columns if col not in header]

        return len(missing_columns) == 0, missing_columns

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False, []


def readargs(args=None):
    parser = argparse.ArgumentParser(
        prog='Text Analyzer project',
    )
    # General arguments
    parser.add_argument('-t', '--task',
                        help="task number",
                        required=True
                        )
    parser.add_argument('-s', '--sentences',
                        help="Sentence file path",
                        )
    parser.add_argument('-n', '--names',
                        help="Names file path",
                        )
    parser.add_argument('-r', '--removewords',
                        help="Words to remove file path",
                        )
    parser.add_argument('-p', '--preprocessed',
                        action='append',
                        help="json with preprocessed data",
                        )
    # Task specific arguments
    parser.add_argument('--maxk',
                        type=int,
                        help="Max k",
                        )
    parser.add_argument('--fixed_length',
                        type=int,
                        help="fixed length to find",
                        )
    parser.add_argument('--windowsize',
                        type=int,
                        help="Window size",
                        )
    parser.add_argument('--pairs',
                        help="json file with list of pairs",
                        )
    parser.add_argument('--threshold',
                        type=int,
                        help="graph connection threshold",
                        )
    parser.add_argument('--maximal_distance',
                        type=int,
                        help="maximal distance between nodes in graph",
                        )

    parser.add_argument('--qsek_query_path',
                        help="json file with query path",
                        )

    return parser.parse_args()


def main():
    try:
        args = readargs()
        if not args.task:
            # -1 is error in general arguments, otherwise the error indicates the arguments with the task number
            sys.exit(-1)

        if not is_valid_task_number(args.task):
            sys.exit(-1)
        preprocessed_data = {}
        preprocessed = False
        if args.preprocessed:
            preprocessed = True
            if len(args.preprocessed) < 1:
                sys.exit(-1)
            if not is_valid_json_path(args.preprocessed[0]):
                sys.exit(-1)

            with open(args.preprocessed[0], 'r') as f:
                preprocessed_data = json.load(f)

        if preprocessed:
            if args.task != '7' and args.task != '8':
                if not preprocessed_data.get("Question 1", {}).get("Processed Sentences") or \
                        not preprocessed_data.get("Question 1", {}).get("Processed Names"):
                    print("ERROR: Preprocessed file does not contain 'Processed Sentences' or "
                          "'Processed Names'. Falling back to original data.")
                    sys.exit(-1)
            else:
                if not preprocessed_data.get("Question 6", {}).get("Pair Matches"):
                    print("ERROR: Preprocessed file does not contain 'Pair Matches'. Falling back to original data.")
                    sys.exit(-1)

        if not preprocessed:
            if not args.removewords or not args.sentences:
                sys.exit(-1)
            if not is_valid_csv_path(args.removewords) or not is_valid_csv_path(args.sentences):
                sys.exit(-1)
            exists, missing = check_columns_in_csv(args.removewords, ['words'])
            if not exists:
                print(f"Missing columns: {missing} in remove words file")
                sys.exit(-1)
            exists, missing = check_columns_in_csv(args.sentences, ['sentence'])
            if not exists:
                print(f"Missing columns: {missing} in sentences file")
                sys.exit(-1)

        if args.task == '1':
            if preprocessed:
                print('Error: should not include preprocessed flag')
                sys.exit(1)
            if not args.names or not is_valid_csv_path(args.names):
                sys.exit(1)
            exists, missing = check_columns_in_csv(args.names, ['Name', 'Other Names'])
            if not exists:
                print(f"Missing columns: {missing} in names file")
                sys.exit(1)
            TASK1(sentence_path=args.sentences, people_path=args.names,
                  remove_word_path=args.removewords).print_result()

        elif args.task == '2':
            if not args.maxk or int(args.maxk) < 0:
                sys.exit(2)
            if preprocessed:
                TASK2(k_seq=args.maxk, preprocessed=args.preprocessed[0]).print_result()
            else:
                TASK2(k_seq=args.maxk, sentence_path=args.sentences, remove_word_path=args.removewords).print_result()

        elif args.task == '3':
            if preprocessed:
                TASK3(preprocessed=args.preprocessed[0])
            else:
                if not args.names or not is_valid_csv_path(args.names):
                    sys.exit(3)
                exists, missing = check_columns_in_csv(args.names, ['Name', 'Other Names'])
                if not exists:
                    print(f"Missing columns: {missing} in names file")
                    sys.exit(3)
                TASK3(sentence_path=args.sentences, people_path=args.names, remove_word_path=args.removewords)

        elif args.task == '4':
            if not args.qsek_query_path or not is_valid_json_path(args.qsek_query_path):
                sys.exit(4)
            if preprocessed:
                TASK4(preprocessed=args.preprocessed[0]).basic_search(qsek_query_path=args.qsek_query_path)
            else:
                TASK4(sentence_path=args.sentences, remove_word_path=args.removewords).basic_search(
                    qsek_query_path=args.qsek_query_path)

        elif args.task == '5':
            if not args.maxk or int(args.maxk) < 0:
                sys.exit(5)
            if preprocessed:
                TASK5(max_k=args.maxk, preprocessed=args.preprocessed[0])
            else:
                if not args.names or not is_valid_csv_path(args.names):
                    sys.exit(5)
                exists, missing = check_columns_in_csv(args.names, ['Name', 'Other Names'])
                if not exists:
                    print(f"Missing columns: {missing} in names file")
                    sys.exit(5)
                TASK5(max_k=args.maxk, sentence_path=args.sentences, people_path=args.names,
                      remove_word_path=args.removewords)

        elif args.task == '6':
            if not args.windowsize or not args.threshold or int(args.windowsize) < 0 or int(args.threshold) < 0:
                sys.exit(6)
            if preprocessed:
                TASK6(preprocessed=args.preprocessed[0], window_size=args.windowsize,
                      threshold=args.threshold).print_result()
            else:
                if not args.names or not is_valid_csv_path(args.names):
                    sys.exit(6)
                exists, missing = check_columns_in_csv(args.names, ['Name', 'Other Names'])
                if not exists:
                    print(f"Missing columns: {missing} in names file")
                    sys.exit(6)
                TASK6(sentence_path=args.sentences, people_path=args.names, remove_word_path=args.removewords,
                      window_size=args.windowsize, threshold=args.threshold).print_result()

        elif args.task == '7':
            if not args.windowsize or not args.threshold or not args.pairs or not args.maximal_distance:
                sys.exit(7)
            if int(args.windowsize) < 0 or int(args.threshold) < 0 or int(args.maximal_distance) < 0:
                sys.exit(7)
            if not is_valid_json_path(args.pairs):
                sys.exit(7)
            if preprocessed:
                task = TASK7(preprocessed=args.preprocessed[0], window_size=args.windowsize, threshold=args.threshold,
                             pairs_file=args.pairs)
            else:
                if not args.names or not is_valid_csv_path(args.names):
                    sys.exit(7)
                exists, missing = check_columns_in_csv(args.names, ['Name', 'Other Names'])
                if not exists:
                    print(f"Missing columns: {missing} in names file")
                    sys.exit(7)
                task = TASK7(sentence_path=args.sentences, people_path=args.names, remove_word_path=args.removewords,
                             window_size=args.windowsize, threshold=args.threshold, pairs_file=args.pairs)
            task.fill_result(maximal_distance=args.maximal_distance)
            task.print_result()

        elif args.task == '8':
            if not args.windowsize or not args.threshold or not args.pairs or not args.fixed_length:
                sys.exit(8)
            if int(args.windowsize) < 0 or int(args.threshold) < 0 or int(args.fixed_length) < 0:
                sys.exit(7)
            if not is_valid_json_path(args.pairs):
                sys.exit(8)
            if preprocessed:
                TASK8(fixed_length=args.fixed_length, window_size=args.windowsize, threshold=args.threshold,
                      preprocessed=args.preprocessed[0], pairs_file=args.pairs)
            else:
                if not args.names or not is_valid_csv_path(args.names):
                    sys.exit(8)
                exists, missing = check_columns_in_csv(args.names, ['Name', 'Other Names'])
                if not exists:
                    print(f"Missing columns: {missing} in names file")
                    sys.exit(8)
                TASK8(sentence_path=args.sentences, people_path=args.names, remove_word_path=args.removewords,
                      window_size=args.windowsize, threshold=args.threshold, pairs_file=args.pairs,
                      fixed_length=args.fixed_length)

        elif args.task == '9':
            if not args.threshold or int(args.threshold) < 0:
                sys.exit(9)
            if preprocessed:
                TASK9(threshold=args.threshold, preprocessed=args.preprocessed[0]).print_result()
            else:
                TASK9(threshold=args.threshold, sentence_path=args.sentences,
                      remove_word_path=args.removewords).print_result()

    except FileNotFoundError:
        print('Error')

    except SystemExit as e:
        print('invalid input')


if __name__ == '__main__':
    main()
