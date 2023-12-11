from .utils import *

class Value(object):
    def __init__(self, attribute, value):
        self.__attribute = deepcopy(attribute)
        self.__value = deepcopy(value)

    def isValidRawValue(self, value):
        return self.__attribute.isCorrectRawType(value)

    def __deepcopy__(self, memo):
        return Value(deepcopy(self.__attribute), deepcopy(self.__value))

    def __copy__(self):
        return self.__deepcopy__(None)

    def getRawValue(self):
        return self.__value

    def __getValueInstance(self, oth):
        if oth is None:
            return Value(self.__attribute, None)

        if isinstance(oth, Value) and not self.__attribute.hasSameRawType(oth.__attribute):
            raise AttributeRawTypeMismatchException("Error: raw type mismatch between value %s and %s (%s vs %s)" % (str(self.getRawValue()), str(oth.getRawValue()), self.__attribute.getRawType().__name__, oth.__attribute.getRawType().__name__,))

        if not isinstance(oth, Value) and self.isValidRawValue(oth):
            return Value(self.__attribute, oth)

        return oth


    def __eq__(self, oth):
        othV = self.__getValueInstance(oth)
        return self.__attribute.equalityCheck(self.__value, othV.__value)

    def __gt__(self, oth):
        othV = self.__getValueInstance(oth)
        return self.__attribute.greaterThanCheck(self.__value, othV.__value)

    def __lt__(self, oth):
        othV = self.__getValueInstance(oth)
        return self.__attribute.lowerThanCheck(self.__value, othV.__value)

    def __neq__(self, oth):
        othV = self.__getValueInstance(oth)
        return self.__attribute.inequalityCheck(self.__value, othV.__value)

    def __ge__(self, oth):
        othV = self.__getValueInstance(oth)
        return self.__attribute.greaterEqualThanCheck(self.__value, othV.__value)

    def __le__(self, oth):
        othV = self.__getValueInstance(oth)
        return self.__attribute.lowerEqualThanCheck(self.__value, othV.__value)

    def isNull(self):
        return self.__attribute.nullCheck(self.__value)

    def isNotNull(self):
        return self.__attribute.notNullCheck(self.__value)

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return str(self.__value) + ", " + str(self.__attribute)
