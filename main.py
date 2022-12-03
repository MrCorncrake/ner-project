import nltk

from data.NZ.NZ_evaulation_data import NZ_evaluation_data
from window import window
from ner import EntityLibrary, NamedEntityRecognizer
import os
import sys
from evaluation import accuracy_eval

# nltk.download('punkt')
nltk.download('stopwords')

# Const sample
# file = "const_evaluation.txt"
# lib_file = "library.txt"
# evaluation_data = const_evaluation_data

# NZ sample
file = 'data/NZ/NZ_text.txt'
lib_file = "data/NZ/NZ_lib.txt"
evaluation_data = NZ_evaluation_data


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    lib = EntityLibrary(resource_path(lib_file))
    ner = NamedEntityRecognizer(lib)
    with open(resource_path(file)) as f:
        lines = f.read()

        results = ner.recognize_in(lines, overlapping=False)
        # results = test_spacy_ner()

        # Results
        print(list(results.items()))
        print('')

        accuracy_eval(evaluation_data, results)

        # Visualization
        window(lines, results.items())
