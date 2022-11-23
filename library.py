import nltk


def clear_token(token):
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

    def contains_token(self, token):
        return token in self.tokens

    def has_form(self, form):
        return form in self.forms

    def has_t_form(self, t_form):
        return t_form in self.t_forms

    def __str__(self):
        return f"[{self.id}: {self.name}]"


class Library:

    def __init__(self, file):
        self.__file = file

        with open(file) as f:
            entities = f.readlines()
            entities = filter(lambda e: not e.startswith('#'), entities)
            entities = [clear_token(e) for e in entities]
            entities = [e.split(';') for e in entities]

            self.__entities = []
            self.__no_entities = len(entities)
            for i in range(len(entities)):
                entity = Entity(i, entities[i])
                self.__entities.append(entity)

    def get_entities(self):
        return self.__entities

    def get_entity(self, entity_id):
        if -1 < entity_id < self.__no_entities:
            return self.__entities[entity_id]
        else:
            return None

    def phrase_is_entity(self, entity_id, phrase):
        phrase = [clear_token(t) for t in phrase]
        entity = self.__entities[entity_id]
        return phrase in entity.t_forms

    def eval_token(self, token):
        entity_ids = []
        token = clear_token(token)
        for entity in self.__entities:
            if token in entity.tokens:
                entity_ids.append(entity.id)
        return entity_ids

    def eval_tokens(self, tokens):
        return [self.eval_token(t) for t in tokens]
