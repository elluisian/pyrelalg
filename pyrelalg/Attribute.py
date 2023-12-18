from .utils.utils import *
from .AttributeUtils import *


class Attribute(object):
    def __init__(self, name, rawType, belongingSchema=None):
        self.__name = name
        self.__rawType = rawType
        self.__belongingSchema = belongingSchema


    def getBelongingSchema(self):
        return self.__belongingSchema

    def isInSameSchema(self, oth):
        if self is oth:
            return True

        if oth is None:
            return False

        return self.__belongingSchema == oth.__belongingSchema

    def isInstanceOfRawType(self, val):
        return is_of_type(val, self.__rawType)

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
        if val1 is not None and\
            val2 is not None and\
            self.isInstanceOfRawType(val1) and\
            self.isInstanceOfRawType(val2):
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
        return not nullCheck(val)



    def __deepcopy__(self, memo):
        return Attribute(self.__name, self.__rawType)

    def __copy__(self):
        return self.__deepcopy__(None)

    def __eq__(self, oth):
        return self.looseEqual(oth) and self.hasSameRawType(oth)


    """
    Comparison only by name
    """
    def looseEqual(self, oth):
        if self is oth:
            return True

        if oth is None or not is_attribute(oth):
            return False

        return self.__name == oth.__name


    def __neq__(self, oth):
        return not self.__eq__(oth)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return str(self) + ": " + self.__rawType.__name__

    def __hash__(self):
        return hash((self.__name, self.__rawType,))




is_attribute         = lambda x : is_of_type(x, Attribute)
is_attr_or_str       = lambda x : is_attribute(x) or is_string(x)
is_attr_or_type      = lambda x : is_attribute(x) or is_type(x)
is_attribute_coll    = lambda x : is_collectible_of_type(x, Attribute)
is_attr_or_str_coll  = lambda x : is_collectible_conditional(x, lambda y : is_attr_or_str(y))
is_attr_or_type_coll = lambda x : is_collectible_conditional(x, lambda y : is_attr_or_type(y))
is_attribute_dict    = lambda x : is_dict_of_types(str, Attribute, x)
is_attr_or_str_dict  = lambda x : is_dict_conditional(x, lambda k, v : is_string(k) and is_attr_or_str(v))
is_attr_or_type_dict = lambda x : is_dict_conditional(x, lambda k, v : is_string(k) and is_attr_or_type(v))




get_attribute_names    = lambda x : tuple(map(lambda y : y if is_string(y) else y.getName(), x))
get_attribute_raw_types = lambda x : tuple(map(lambda y : y if is_type(y) else y.getRawType(), x))