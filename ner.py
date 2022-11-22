import nltk
import itertools
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

    def eval_token_phrase(self, entity_id, phrase):
        t_phrase, span = phrase.get()
        if self._lib.check_phrase_if_entity(entity_id, t_phrase):
            word = self._lib.get_entity(entity_id).name
            if word not in self._entity_positions:
                self._entity_positions[word] = [(span[0], span[1])]
            else:
                self._entity_positions[word].append((span[0], span[1]))
            return True
        return False

    def recognize_in(self, lines, overlapping=False):
        self._entity_positions = {}

        tokens = nltk.TreebankWordTokenizer().tokenize(lines)
        spans = list(nltk.TreebankWordTokenizer().span_tokenize(lines))
        token_spans = list(zip(tokens, spans))
        ids = self._lib.eval_tokens(tokens)
        token_spans_ids = list(zip(token_spans, ids))

        phrases = {}
        new_phrases = []
        for token_span_ids in token_spans_ids:
            token_span = token_span_ids[0]
            ids = token_span_ids[1]
            for entity_id in list(phrases):
                if entity_id not in ids:
                    phrase = phrases.pop(entity_id)
                    new_phrases.append((entity_id, phrase))
            if len(phrases) == 0:
                if overlapping:
                    for entity_id, phrase in new_phrases:
                        self.eval_token_phrase(entity_id, phrase)
                elif len(new_phrases) > 0:
                    new_phrases.sort(key=lambda id_phrase: len(id_phrase[1]), reverse=True)
                    entity_id, phrase = new_phrases[0]
                    self.eval_token_phrase(entity_id, phrase)
                new_phrases = []
            for entity_id in ids:
                if entity_id not in phrases:
                    phrases[entity_id] = TokenPhrase()
                phrases[entity_id].add(token_span)
        return self._entity_positions




