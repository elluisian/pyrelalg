from .utils import *
from .AttributeUtils import *


class Attribute(object):
    def __init__(self, name, rawType):
        self.__name = name
        self.__rawType = rawType


    def isCorrectRawType(self, val):
        return val is None or isinstance(val, self.__rawType)

    def areCorrectRawTypes(self, val1, val2):
        return self.isCorrectRawType(val1) and self.isCorrectRawType(val2)

    def getName(self):
        return self.__name

    def getRawType(self):
        return self.__rawType

    def hasSameRawType(self, oth):
        if self is oth:
            return True

        if oth is None:
            return False

        return self.__rawType == oth.__rawType


    """
    Value comparisons
    """
    def __comparisonCheck(self, val1, val2, op):
        v = False
        if val1 is not None and val2 is not None and self.areCorrectRawTypes(val1, val2):
            v = op(val1, val2)
        return v

    def equalityCheck(self, val1, val2):
        return self.__comparisonCheck(val1, val2, lambda x, y: x == y)

    def lowerThanCheck(self, val1, val2):
        return self.__comparisonCheck(val1, val2, lambda x, y: x < y)

    def greaterThanCheck(self, val1, val2):
        return self.__comparisonCheck(val1, val2, lambda x, y: x > y)

    def inequalityCheck(self, val1, val2):
        return self.__comparisonCheck(val1, val2, lambda x, y: x != y)

    def lowerEqualThanCheck(self, val1, val2):
        return self.__comparisonCheck(val1, val2, lambda x, y: x <= y)

    def greaterEqualThanCheck(self, val1, val2):
        return self.__comparisonCheck(val1, val2, lambda x, y: x >= y)

    def nullCheck(self, val):
        return val is None

    def notNullCheck(self, val):
        return val is not None




    def __deepcopy__(self, memo):
        return Attribute(self.__name, self.getRawType())

    def __copy__(self):
        return self.__deepcopy__(None)

    def __eq__(self, oth):
        if self is oth:
            return True

        if oth is None or not isinstance(oth, Attribute):
            return False

        return self.__name == oth.__name and self.hasSameRawType(oth)

    def __neq__(self, oth):
        return not self.__eq__(oth)

    def __str__(self):
        return self.__name + ": " + "rawtype(" + self.__rawType.__name__ + ")"

    def __repr__(self):
        return self.__str__()
