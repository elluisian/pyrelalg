from .utils import *


class AttributeRawTypeMismatchException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class AttributeRawTypeIntegrityCheckException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)




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








class AttributeUtils(object):
    @staticmethod
    def attrsRawTypeIntegrityCheck(attrNames1, attrNames2, rawTypes1, rawTypes2):
        commonAttributes = AttributeUtils.attrIntersect(attrNames1, attrNames2)[0]
        
        for i in commonAttributes:
            try:
                attrIdx1 = attrNames1.index(i)
                attrIdx2 = attrNames2.index(i)

                rawT1 = rawTypes1[attrIdx1]
                rawT2 = rawTypes2[attrIdx2]

                if rawT1 != rawT2:
                    raise AttributeRawTypeIntegrityCheckException("Common attribute \"%s\" reported as different types (first type is \"%s\", second is \"%s\")!" % (i, rawT1.__name__, rawT2.__name__,))

            except ValueError as ex:
                pass



    @staticmethod
    def __isRawMode(rawTypes1=None, rawTypes2=None):
        return rawTypes1 is not None and rawTypes2 is not None



    @staticmethod
    def attrUnion(attrsNames1, attrsNames2, rawTypes1=None, rawTypes2=None):
        rawMode = AttributeUtils.__isRawMode(rawTypes1, rawTypes2)
        if rawMode:
            AttributeUtils.attrsRawTypeIntegrityCheck(attrsNames1, attrsNames2, rawTypes1, rawTypes2)

        names = list(attrsNames1)
        rawTypes = list(rawTypes1) if rawMode else None

        for idx, currAttrName in enumerate(attrsNames2):
            if currAttrName not in names:
                names.append(currAttrName)
                if rawMode:
                    rawTypes.append(rawTypes2[idx])

        return (names, rawTypes,)



    @staticmethod
    def attrIntersect(attrs1, attrs2, rawTypes1=None, rawTypes2=None):
        rawMode = AttributeUtils.__isRawMode(rawTypes1, rawTypes2)
        if rawMode:
            AttributeUtils.attrsRawTypeIntegrityCheck(attrsNames1, attrsNames2, rawTypes1, rawTypes2)

        names = []
        rawTypes = [] if rawMode else None

        for i in attrs1:
            if i in attrs2:
                idx = attrs2.index(i)
                names.append(i)
                if rawMode:
                    rawTypes.append(rawTypes2[idx])

        return (names, rawTypes,)



    @staticmethod
    def attrDiff(attrs1, attrs2, rawTypes1=None, rawTypes2=None):
        rawMode = AttributeUtils.__isRawMode(rawTypes1, rawTypes2)
        if rawMode:
            AttributeUtils.attrsRawTypeIntegrityCheck(attrs1, attrs2, rawTypes1, rawTypes2)

        names = []
        rawTypes = [] if rawMode else None

        for idx, i in enumerate(attrs1):
            if i not in attrs2:
                names.append(i)
                if rawMode:
                    rawTypes.append(rawTypes1[idx])

        return (names, rawTypes,)



    @staticmethod
    def attrEquality(attrs1, attrs2, rawTypes1=None, rawTypes2=None):
        attrInt = AttributeUtils.attrIntersect(attrs1, attrs2, rawTypes1, rawTypes2)[0]
        return AttributeUtils.attrSameNumber(attrs1, attrs2) and\
            AttributeUtils.attrSameNumber(attrs1, attrInt)



    @staticmethod
    def attrDuplicates(attrs):
        duplicates = []

        for i in attrs:
            if attrs.count(i) > 1:
                duplicates.append(i)

        return duplicates


    @staticmethod
    def attrSameNumber(attrs1, attrs2):
        attrs1Num = len(attrs1)
        attrs2Num = len(attrs2)
        return attrs1Num == attrs2Num
