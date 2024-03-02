class Stack(object):
    def __init__(self):
        self.__elements = []
        self.__nElements = 0


    def push(self, element):
        self.__elements.append(element)
        self.__nElements += 1


    def pop(self):
        n = self.top()
        if not self.isEmpty():
            del self.__elements[self.__nElements - 1]
            self.__nElements -= 1
        return n


    def top(self):
        n = None
        if not self.isEmpty():
            n = self.__elements[self.__nElements - 1]
        return n


    def isEmpty(self):
        return self.__nElements == 0


    def size(self):
        return self.__nElements