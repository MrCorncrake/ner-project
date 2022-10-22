import nltk
from library import Library

nltk.download('punkt')

file = "const.txt"

if __name__ == '__main__':
    lib = Library("library.txt")
    with open(file) as f:
        lines = f.read()
        tokens = nltk.word_tokenize(lines)

        print(lib.get_words())
        print(tokens)

