import nltk


def _clear_token(token):
    token = token.replace('\n', '')
    token = token.replace('.', '')
    token = token.lower()
    return token


class Entity:

    def __init__(self, entity_id, forms):
        self.id = entity_id
        self.name = forms[0]
        self.forms = forms
        self.t_forms = []
        tokens = []
        for form in forms:
            t_form = nltk.TreebankWordTokenizer().tokenize(form)
            self.t_forms.append(t_form)
            tokens.extend(t_form)
        self.tokens = set(tokens)

    def contains_token(self, token: str) -> bool:
        """ Returns True if the entity can contain provided token """
        return token in self.tokens

    def has_form(self, form: str) -> bool:
        """ Returns True if the entity can be expressed by the provided form """
        return form in self.forms

    def has_t_form(self, t_form: [str]) -> bool:
        """ Returns True if the entity can be expressed by the provided tokenized form """
        return t_form in self.t_forms

    def __str__(self):
        return '[' + self.id + ': ' + self.name + ']'


class EntityLibrary:

    def __init__(self, file):
        self.__file = file

        with open(file) as f:
            entities = f.readlines()
            entities = filter(lambda e: not e.startswith('#'), entities)
            entities = [_clear_token(e) for e in entities]
            entities = [e.split(';') for e in entities]

            self.__entities = []
            self.__no_entities = len(entities)
            for i in range(len(entities)):
                entity = Entity(i, entities[i])
                self.__entities.append(entity)

    def get_entities(self) -> [Entity]:
        """ Returns all the entities in the library """
        return self.__entities

    def get_entity(self, entity_id) -> Entity or None:
        """ Returns entity with given entity_id """
        if -1 < entity_id < self.__no_entities:
            return self.__entities[entity_id]
        else:
            return None

    def tokens_are_entity(self, tokens, entity_id) -> bool:
        """ Checks if the given list of tokens represents entity with provided entity_id """
        tokens = [_clear_token(t) for t in tokens]
        entity = self.__entities[entity_id]
        return entity.has_t_form(tokens)

    def eval_token(self, token) -> [int]:
        """ Returns list of ids of entities that the token can be a part of """
        entity_ids = []
        token = _clear_token(token)
        for entity in self.__entities:
            if entity.contains_token(token):
                entity_ids.append(entity.id)
        return entity_ids

    def eval_tokens(self, tokens) -> [[int]]:
        """ Evaluates all the tokens from the list using eval_token method """
        return [self.eval_token(t) for t in tokens]


class _TokenPhrase:

    def __init__(self):
        self.phrase = []
        self.start = -1
        self.end = -1

    def add(self, token_span: (str, (int, int))):
        """ Adds token span to the token phrase """
        self.phrase.append(token_span[0])
        if self.start < 0:
            self.start = token_span[1][0]
        self.end = token_span[1][1]

    def get(self) -> ([str], (int, int)):
        """ Returns complete token phrase and its total span """
        return self.phrase, (self.start, self.end)

    def __len__(self):
        return len(self.phrase)


class NamedEntityRecognizer:

    def __init__(self, lib: EntityLibrary):
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
        """ Returns last result of recognize_in method call """
        return self._entity_positions

    def recognize_in(self, text, overlapping=False) -> {str: [(int, int)]}:
        """ Recognizes Entities from provided EntityLibrary in the given text.
            Returns dictionary that maps entity names with its locations within the text.
            If overlapping is set to True overlapping entities will be returned.
            If overlapping is set to False only the longest complete entity will be returned.
        """
        self._entity_positions = {}

        tokens = nltk.TreebankWordTokenizer().tokenize(text)
        spans = list(nltk.TreebankWordTokenizer().span_tokenize(text))
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




