
class Library:

    def __init__(self, file):
        self.file = file
        with open(file) as f:
            words = f.readlines()
            words = [w.replace('\n', '') for w in words]
            words = [w.lower() for w in words]
            self.__words = {}
            for i in range(len(words)):
                self.__words[words[i]] = i

    def get_words(self):
        return self.__words.keys()

    def is_word(self, word):
        w = word.lower()
        if w in self.__words.keys():
            return self.__words[w]
        else:
            return -1

