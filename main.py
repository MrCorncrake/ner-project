import nltk
from library import Library
from window import window
from ner import NamedEntityRecognizer

# nltk.download('punkt')
nltk.download('stopwords')

file = "const.txt"

if __name__ == '__main__':
    lib = Library("library.txt")
    ner = NamedEntityRecognizer(lib)
    with open(file) as f:
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
