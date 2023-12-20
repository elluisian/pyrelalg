from .utils.utils import *
from .DBSchema import *
from .Value import *




class Tuple(object):
    def __init__(self, attrData, rawValues):
        nVals = len(rawValues)
        nAttrs = len(attrData)

        if nVals != nAttrs:
            raise TupleCreationException("Attributes and values number mismatch (%s vs %s, %d vs %d)!" % (str(attributes), str(values), nAttrs, nVals,))

        self.__attrNames = tuple(map(lambda x : x.getName(), attrData))
        self.__nAttrs = len(self.__attrNames)
        self.__values = {}

        for idx, i in enumerate(self.__attrNames):
            self.__values[i] = Value(attrData[idx], rawValues[idx])


    def getValue(self, attrName):
        return self.getValues(attrName)[0]


    def getValues(self, attrNames=None):
        if attrNames is None:
            attrNames = self.__attrNames

        elif isinstance(attrNames, str):
            attrNames = (attrNames,)

        newTup = []
        for a in attrNames:
            newTup.append(deepcopy(self.__values[a]))

        return newTup


    def getAttributeNames(self, attrNames=None):
        if attrNames is None:
            attrNames = self.__attrNames
        
        return tuple(self.__attrNames)


    def asPythonTupleValues(self, attrNames=None):
        if attrNames is None:
            attrNames = self.__attrNames

        t = []
        for i in attrNames:
            t.append(deepcopy(self.__values[i].getRawValue()))
        return tuple(t)


    def getCommonAttributeNames(self, attrNames):
        return AttributeUtils.attrIntersect(self.__attrNames, attrNames)[0]

    def getCommonAttributeNamesToTuple(self, othTpl):
        return self.getCommonAttributeNames(othTpl.__attrNames)

    def hasAttributeNames(self, attrNames):
        szAttrsRequested = len(attrNames)
        attrsFound = self.getCommonAttributeNames(attrNames)
        szAttrsFound = len(attrsFound)
        return szAttrsFound == szAttrsRequested


    def __copy__(self):
        return self.__deepcopy__(None)

    def __deepcopy__(self, memo):
        t = Tuple(self.getAttributes(), self.asPythonTupleValues())

    def __eq__(self, othTpl):
        return self is othTpl or (AttributeUtils.attrEquality(self.__attrNames, othTpl.__attrNames) and self.__values == othTpl.__values)

    def __str__(self):
        return "(%s)" % (", ".join(list(map(str, self.asPythonTupleValues()))),)

    def __repr__(self):
        return "Tupla(%s | %s)" % (", ".join(self.__attrNames), ", ".join(list(map(str, self.asPythonTupleValues()))),)


    def __len__(self):
        return self.__nAttrs


    def __contains__(self, t):
        return t in self.__values


    """
    Get item facilities
    """
    def __getitem__(self, sel):
        return genericGetItem(self, sel, Tuple.__noneFunct, Tuple.__intFunct, Tuple.__stringFunct, Tuple.__solveSlice)




    def __noneFunct(self, sel, isSingle, isStart):
        return 0 if isStart else self.__nAttrs


    def __intFunct(self, sel, isSingle, isStart=None):
        if isSingle:
            if sel < 0 or sel > self.__nAttrs:
                raise IndexError("Error: Attribute n. %d does not exist!" % (sel,))
            sel = self.__attrNames[sel]
            return self.__values[sel]

        else:
            if (isStart and sel < 0) or (not isStart and sel > self.__nAttrs):
                raise IndexError("Error: Attribute n. %d does not exist!" % (sel,))

        return sel


    def __stringFunct(self, sel, isSingle, isStart=None):
        if sel not in self.__attrNames:
            raise IndexError("Error: Attribute \"%s\" does not exist!" % (sel,))

        if isSingle:
            return self.__values[sel]

        return self.__attrNames.index(sel)


    def __solveSlice(self, start, end):
        needReverse = start > end
        mn = end if needReverse else start
        mx = start if needReverse else end

        ls = []
        for i in range(mn, mx):
            attrName = self.__attrNames[i]
            ls.append(self.__values[attrName])

        if needReverse:
            ls = list(reversed(ls))

        return ls