from .DBSchema import *
from .Tuple import *
from .DBRelationPrettyPrinter import *
from .DBElementIterator import *


class DBRelation(object):
    def __init__(self, dbSchema):
        self.__dbSchema = dbSchema
        self.__tuples = []
        self.__nTuples = 0


    # dict attr inst -> rawValue
    # tuple inst
    # collectible of Values
    # collectible of raw Value
    # dict of string -> rawValue
    def insert(self, pythonTupleValues):
        if not isinstance(pythonTupleValues, tuple) and not isinstance(pythonTupleValues, list):
            raise NotAValidParameterException("Error: expected python tuple or list, but got %s!" % (type(pythonTupleValues),))

        pythonTupleValues = tuple(pythonTupleValues)
        attrNames = self.__dbSchema.getAttributeNames()
        attrData = self.__dbSchema.getAttributes(attrNames)

        self.__tuples.append(Tuple(attrData, pythonTupleValues))
        self.__nTuples += 1



    def getTuple(self, key):
        return self[key]


    def getDBSchema(self):
        return self.__dbSchema


    def getSize(self):
        return len(self)

    def __len__(self):
        return self.__nTuples

    def __contains__(self, t):
        return t in self.__tuples


    def hasSameSchema(self, othRel):
        return self.__dbSchema == othRel.__dbSchema


    def hasTuple(self, t):
        return t in self


    def hasPythonTupleValues(self, ptv):
        attrNames = self.__dbSchema.getAttributeNames()
        attrData = self.__dbSchema.getAttributes(attrNames)

        t = Tuple(attrData, ptv)
        return self.hasTuple(t)


    def __eq__(self, othInst):
        if self is othInst:
            return True

        isEqual = True

        if not self.hasSameSchema(othInst):
            isEqual = False

        if isEqual:
            for i in range(0, othInst.getSize()):
                t = othInst[i]
                if not self.hasTuple(t):
                    isEqual = False
                    break

        return isEqual

    def __iter__(self):
        return DBElementIterator(self)

    def __deepcopy__(self, memo):
        r = DBRelation(self.getDBSchema())
        for t in self:
            r.insert(t.asPythonTupleValues())
        return r


    def __copy__(self):
        return self.__deepcopy__(None)


    def __str__(self):
        dbRelPP = DBRelationPrettyPrinter(self)
        return dbRelPP.prettyPrint()


    def __repr__(self):
        return self.__str__()


    """
    Get item facilities
    """
    def __getitem__(self, sel):
        return genericGetItem(self, sel, DBRelation.__noneFunct, DBRelation.__intFunct, None, DBRelation.__solveSlice)


    def __noneFunct(self, sel, isSingle, isStart=None):
        return 0 if isStart else self.__nTuples


    def __intFunct(self, sel, isSingle, isStart=None):
        if isSingle:
            if (isStart and sel < 0) or (not isStart and sel > self.__nTuples):
                raise IndexError("Error: Tuple n. %d does not exist!" % (sel,))
        else:
            if sel < 0 or sel > self.__nTuples:
                raise IndexError("Error: Tuple n. %d does not exist!" % (sel,))

        return self.__tuples[sel]


    def __solveSlice(self, start, end):
        needReverse = start > end
        mn = end if needReverse else start
        mx = start if needReverse else end

        ls = self.__tuples[mn:mx]
        if needReverse:
            ls = list(reversed(ls))

        return ls




DBInstance = DBRelation
