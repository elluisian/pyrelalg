class DBElementIterator(object):
    def __init__(self, dbElement):
        self.__dbElement = dbElement
        self.__idx = 0
        self.__max = len(self.__dbElement)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__idx == self.__max:
            raise StopIteration

        el = self.__dbElement[self.__idx]
        self.__idx += 1
        return el