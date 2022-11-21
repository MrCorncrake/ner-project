import nltk
from library import Library
from window import window
from ner import NamedEntityRecognizer
import os, sys

# nltk.download('punkt')
nltk.download('stopwords')

file = "const.txt"


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
        print(lib.get_entities())
        print(lib.get_t_entities())
        print(lib.get_phrase_tokens())
        print('')
        print(list(results.items()))
        print('')
        for key in results:
            print(key + ": " + str(len(results[key])))
        # Visualization
        window(lines, results.items())
