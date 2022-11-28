import nltk
from library import Library


class _TokenPhrase:

    def __init__(self):
        self.phrase = []
        self.start = -1
        self.end = -1

    def add(self, token_span: (str, (int, int))):
        self.phrase.append(token_span[0])
        if self.start < 0:
            self.start = token_span[1][0]
        self.end = token_span[1][1]

    def get(self) -> ([str], (int, int)):
        return self.phrase, (self.start, self.end)

    def __len__(self):
        return len(self.phrase)


class NamedEntityRecognizer:

    def __init__(self, lib: Library):
        self._lib = lib
        self._entity_positions = {}

    def _eval_token_phrase(self, entity_id, phrase) -> bool:
        t_phrase, span = phrase.get()
        if self._lib.tokens_are_entity(t_phrase, entity_id):
            word = self._lib.get_entity(entity_id).name
            if word not in self._entity_positions:
                self._entity_positions[word] = [(span[0], span[1])]
            else:
                self._entity_positions[word].append((span[0], span[1]))
            return True
        return False

    def get_last_results(self) -> {str: [(int, int)]}:
        return self._entity_positions

    def recognize_in(self, lines, overlapping=False) -> {str: [(int, int)]}:
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
                new_phrases.sort(key=lambda id_phrase: len(id_phrase[1]), reverse=True)
                for entity_id, phrase in new_phrases:
                    result = self._eval_token_phrase(entity_id, phrase)
                    if result and not overlapping:
                        break
                new_phrases = []
            for entity_id in ids:
                if entity_id not in phrases:
                    phrases[entity_id] = _TokenPhrase()
                phrases[entity_id].add(token_span)
        return self._entity_positions




