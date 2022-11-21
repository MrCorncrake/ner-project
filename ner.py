import nltk
from library import Library, Entity


class TokenPhrase:

    def __init__(self):
        self.t_spans = []
        self.phrase = []
        self.start = -1
        self.end = -1

    def add(self, token_span: (str, (int, int))):
        self.t_spans.append(token_span)
        self.phrase.append(token_span[0])
        if self.start < 0:
            self.start = token_span[1][0]
        self.end = token_span[1][1]

    def get(self):
        return self.phrase, (self.start, self.end)

    def get_sub_phrase(self, start, end):
        phrase = []
        for i in range(start, end):
            phrase.append(self.phrase[i])
        return phrase, (self.t_spans[start][1][0], self.t_spans[end][1][1])

    def __len__(self):
        return len(self.phrase)


class NamedEntityRecognizer:

    def __init__(self, lib: Library):
        self._lib = lib
        self._entity_positions = {}

    def _add_e_pos_if_valid(self, entity_id, token_span):
        if entity_id != -1:
            word = self._lib.get_entity(entity_id).name
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
                    # TODO: make it better
                    entity_ids = self._lib.t_phrase_is_entity(t_phrase.get()[0])
                    eval_t_phrase = self._lib.eval_t_phrase(t_phrase.get()[0])
                    if len(entity_ids) > 0:
                        entity_ids.sort(key=lambda x: x[1], reverse=True)
                        entity_id = entity_ids[0][0]
                        length = len(eval_t_phrase)
                        start = length
                        end = -1
                        for i in range(length):
                            if entity_id in eval_t_phrase[i]:
                                if i < start:
                                    start = i
                                if i > end:
                                    end = i
                        self._add_e_pos_if_valid(entity_id, t_phrase.get_sub_phrase(start, end))
                    t_phrase = TokenPhrase()
                entity_id = self._lib.phrase_is_entity(token_span[0])
                self._add_e_pos_if_valid(entity_id, token_span)

        return self._entity_positions




