import nltk
from library import Library
from window import window

# nltk.download('punkt')
nltk.download('stopwords')

file = "const.txt"

if __name__ == '__main__':
    lib = Library("library.txt")
    with open(file) as f:
        lines = f.read()
        tokens = nltk.TreebankWordTokenizer().tokenize(lines)
        spans = list(nltk.TreebankWordTokenizer().span_tokenize(lines))

        word_list = lib.get_entities()
        print(word_list)
        t_word_list = lib.get_t_entities()
        print(t_word_list)
        print(lib.get_phrase_tokens())
        print('')

        entity_positions = {}
        token_spans = list(zip(tokens, spans))

        t_phrase = []
        t_phrase_start = -1
        t_phrase_end = -1
        for token_span in token_spans:
            token_word = token_span[0]
            start_idx = token_span[1][0]
            end_idx = token_span[1][1]
            entity_id = -1
            if lib.token_part_of_phrase(token_word):
                t_phrase.append(token_word)
                if t_phrase_start < 0:
                    t_phrase_start = start_idx
                t_phrase_end = end_idx
            else:
                if len(t_phrase) > 0:
                    # End phrase and test it
                    entity_id = lib.t_phrase_is_entity(t_phrase)
                    if entity_id > -1:
                        # if entity save positions
                        word = lib.get_entity(entity_id)[0]
                        if word not in entity_positions:
                            entity_positions[word] = [(t_phrase_start, t_phrase_end)]
                        else:
                            entity_positions[word].append((t_phrase_start, t_phrase_end))
                    # clear phrase
                    t_phrase_start = -1
                    t_phrase_end = -1
                    t_phrase = []
                # Test the word that is not part of phrase
                entity_id = lib.phrase_is_entity(token_word)
                if entity_id > -1:
                    word = lib.get_entity(entity_id)[0]
                    if word not in entity_positions:
                        entity_positions[word] = [(start_idx, end_idx)]
                    else:
                        entity_positions[word].append((start_idx, end_idx))

        print(list(entity_positions.items()))
        print('')
        for key in entity_positions:
            print(key + ": " + str(len(entity_positions[key])))

        window(lines, entity_positions.items())
