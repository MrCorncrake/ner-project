import nltk

from evaluationData import evaluationData
from library import Library
from window import window
from ner import NamedEntityRecognizer
import os
import sys
from functools import reduce

# nltk.download('punkt')
nltk.download('stopwords')

file = "const_evaluation.txt"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    lib = Library(resource_path("library.txt"))
    ner = NamedEntityRecognizer(lib)
    with open(resource_path(file)) as f:
        lines = f.read()
        results = ner.recognize_in(lines)

        # Results
        print(list(results.items()))
        print('')
        # for key in results:
        #     print(key + ": " + str(len(results[key])))

        total_are = 0
        total_found = 0

        for word in evaluationData:
            total_are += len(word[1])
            print(word[0] + ": " + str(len(word[1])))
            if word[0] in results:
                print(word[0] + ": " + str(len(results[word[0]])))
                total_found += len(results[word[0]])
            else:
                print(word[0] + ": 0")

        all_letters = 0
        matching_letters = 0

        for word in evaluationData:
            if word[0] in results:
                for word_position in word[1]:
                    found = 0
                    for found_word_position in results[word[0]]:
                        if not(
                                found_word_position[0] < word_position[0] and found_word_position[1] < word_position[1]
                                or found_word_position[0] > word_position[0] and found_word_position[1] > word_position[1]
                        ):
                            found += 1
                            all_letters += word_position[1] - word_position[0]
                            matching_letters += word_position[1] - word_position[0] \
                                                - max(0, found_word_position[0] - word_position[0]) \
                                                - max(0, word_position[1] - found_word_position[1])
                    if found == 0:
                        all_letters += word_position[1] - word_position[0]
            else:
                all_letters += reduce(lambda total, position: total + position[1] - position[0], word[1])

        print("word accuracy: " + str(total_found / total_are))
        print("letter accuracy: " + str(matching_letters / all_letters))
        # Visualization
        window(lines, results.items())
