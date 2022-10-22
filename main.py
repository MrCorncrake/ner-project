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

        word_list = lib.get_words()

        words_positions = {}
        token_spans = list(zip(tokens, spans))

        for token_span in token_spans:
            token_word = token_span[0]
            start_idx = token_span[1][0]
            if lib.is_word(token_word) > -1:
                if token_word not in words_positions:
                    words_positions[token_word] = [start_idx]
                else:
                    words_positions[token_word].append(start_idx)

        print(words_positions.items())



