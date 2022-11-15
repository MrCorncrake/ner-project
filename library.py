import nltk


class Library:

    def __init__(self, file):
        self.__file = file

        with open(file) as f:
            entities = f.readlines()
            entities = [self._clear_token(e) for e in entities]
            entities = [e.split(';') for e in entities]
            self.__forms = {}
            self.__entities = []
            self.__t_entities = []
            self.__phrase_tokens = []
            self.__no_entities = len(entities)
            for i in range(len(entities)):
                self.__entities.append(entities[i])
                self.__t_entities.append([])
                for form in entities[i]:
                    t_form = nltk.TreebankWordTokenizer().tokenize(form)
                    if len(t_form) > 1:
                        self.__phrase_tokens.extend(t_form)
                    self.__t_entities[i].append(t_form)
                    self.__forms[form] = i
            self.__phrase_tokens = list(set(self.__phrase_tokens))

    @staticmethod
    def _clear_token(token):
        token = token.replace('\n', '')
        token = token.replace('.', '')
        token = token.lower()
        return token

    def get_entities(self):
        return self.__entities

    def get_t_entities(self):
        return self.__t_entities

    def get_phrase_tokens(self):
        return self.__phrase_tokens

    def get_entity(self, entity_id):
        if -1 < entity_id < self.__no_entities:
            return self.__entities[entity_id]
        else:
            return []

    def get_t_entity(self, entity_id):
        if -1 < entity_id < self.__no_entities:
            return self.__t_entities[entity_id]
        else:
            return []

    def phrase_is_entity(self, phrase):
        w = self._clear_token(phrase)
        if w in self.__forms.keys():
            return self.__forms[w]
        else:
            return -1

    def token_part_of_phrase(self, token):
        return self._clear_token(token) in self.__phrase_tokens

    def t_phrase_is_entity(self, phrase):
        phrase = [self._clear_token(t) for t in phrase]
        for i in range(self.__no_entities):
            if phrase in self.__t_entities[i]:
                return i
        return -1
