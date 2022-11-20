import nltk
from library import Library


class TokenPhrase:

    def __init__(self):
        self.phrase = []
        self.start = -1
        self.end = -1

    def add(self, token_span: (str, (int, int))):
        self.phrase.append(token_span[0])
        if self.start < 0:
            self.start = token_span[1][0]
        self.end = token_span[1][1]

    def get(self):
        return self.phrase, (self.start, self.end)

    def __len__(self):
        return len(self.phrase)


class NamedEntityRecognizer:

    def __init__(self, lib: Library):
        self._lib = lib
        self._entity_positions = {}

    def _add_e_pos_if_valid(self, entity_id, token_span):
        if entity_id != -1:
            word = self._lib.get_entity(entity_id)[0]
            if word not in self._entity_positions:
                self._entity_positions[word] = [(token_span[1][0], token_span[1][1])]
            else:
                self._entity_positions[word].append((token_span[1][0], token_span[1][1]))

    def get_last_results(self):
        return self._entity_positions

    def recognize_in(self, lines):
        self._entity_positions = {}

        tokens = nltk.TreebankWordTokenizer().tokenize(lines)
        spans = list(nltk.TreebankWordTokenizer().span_tokenize(lines))
        token_spans = list(zip(tokens, spans))

        t_phrase = TokenPhrase()
        for token_span in token_spans:
            if self._lib.token_part_of_phrase(token_span[0]):
                t_phrase.add(token_span)
            else:
                if len(t_phrase) > 0:
                    entity_id = self._lib.t_phrase_is_entity(t_phrase.get()[0])
                    self._add_e_pos_if_valid(entity_id, t_phrase.get())
                    t_phrase = TokenPhrase()
                entity_id = self._lib.phrase_is_entity(token_span[0])
                self._add_e_pos_if_valid(entity_id, token_span)

        return self._entity_positions




