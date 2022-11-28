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

    def contains_token(self, token) -> bool:
        return token in self.tokens

    def has_form(self, form) -> bool:
        return form in self.forms

    def has_t_form(self, t_form) -> bool:
        return t_form in self.t_forms

    def __str__(self):
        return '[' + self.id + ': ' + self.name + ']'


class Library:

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
        return self.__entities

    def get_entity(self, entity_id) -> Entity or None:
        if -1 < entity_id < self.__no_entities:
            return self.__entities[entity_id]
        else:
            return None

    def tokens_are_entity(self, tokens, entity_id) -> bool:
        tokens = [_clear_token(t) for t in tokens]
        entity = self.__entities[entity_id]
        return entity.has_t_form(tokens)

    def eval_token(self, token) -> [int]:
        entity_ids = []
        token = _clear_token(token)
        for entity in self.__entities:
            if entity.contains_token(token):
                entity_ids.append(entity.id)
        return entity_ids

    def eval_tokens(self, tokens) -> [[int]]:
        return [self.eval_token(t) for t in tokens]
