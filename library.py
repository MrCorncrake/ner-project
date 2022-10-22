
class Library:

    def __init__(self, file):
        self.file = file
        with open(file) as f:
            words = f.readlines()
            self.__words = [w.replace('\n', '') for w in words]

    def get_words(self):
        return self.__words

    def is_word(self, word):
        if word in self.__words:
            return True
        else:
            return False

