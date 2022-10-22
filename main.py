import nltk
from library import Library

nltk.download('punkt')

file = "const.txt"

if __name__ == '__main__':
    lib = Library("library.txt")
    with open(file) as f:
        lines = f.read()
        tokens = nltk.TreebankWordTokenizer().tokenize(lines)
        spans = list(nltk.TreebankWordTokenizer().span_tokenize(lines))

        # foundWords = lib.get_words()
        #
        # for token in tokens:
        #     index = lib.is_word(token)
        #     if index != -1:

        print(lib.get_words())
        print(lib.is_word('Senator'))
        print(tokens)
        print(spans)


