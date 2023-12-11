from Attribute import *


class DBSchemaIterator(object):
    def __init__(self, dbSchema):
        self.__dbSchema = dbSchema
        self.__attrs = dbSchema.getAttributeNames()
        self.__idx = 0
        self.__max = len(self.__attrs)

    def __iter__(self):
        return self

    def __next__(self):
        if self.__idx == self.__max:
            raise StopIteration

        attrName = self.__attrs[self.__idx]
        el = self.__dbSchema.getAttribute(attrName)
        self.__idx += 1
        return el



class DBSchema(object):
    def __init__(self, attrNames, attrRawTypes):
        self.__attrNames = tuple(attrNames)
        self.__attrData = {}

        for idx, attrName in enumerate(attrNames):
            self.__attrData[attrName] = Attribute(attrName, attrRawTypes[idx])


    def getAttributeNames(self):
        return tuple(self.__attrNames)


    def getAttributes(self, attrNames=None):
        if attrNames is None:
            attrNames = self.__attrNames

        elif isinstance(attrNames, str):
            attrNames = (attrNames,)
        
        attrL = []
        for i in attrNames:
            attrL.append(deepcopy(self.__attrData[i]))

        return tuple(attrL)


    def getAttributeRawTypes(self, attrNames=None):
        if attrNames is None:
            attrNames = self.__attrNames

        elif isinstance(attrNames, str):
            attrNames = (attrNames,)
        
        attrInsts = self.getAttributes(attrNames)
        attrL = []
        for i in attrInsts:
            attrL.append(i.getRawType())

        return tuple(attrL)


    def getCommonAttributeNames(self, attrNames):
        return AttributeUtils.attrIntersect(self.getAttributeNames(), attrNames)[0]

    def getCommonAttributeNamesToSchema(self, othSch):
        return self.getCommonAttributeNames(othSch.getAttributeNames())

    """
    def hasAttributeNames(self, attrNames):
        szAttrsRequested = len(attrNames)
        attrsFound = self.getCommonAttributeNames(attrNames)
        szAttrsFound = len(attrsFound)
        return szAttrsFound == szAttrsRequested
    """

    def attributeEquality(self, attrNames):
        return AttributeUtils.attrEquality(self.getAttributeNames(), attrNames)



    def __deepcopy__(self, memo):
        return DBSchema(self.__attrNames, tuple(self.getAttributeRawTypes(self.__attrNames)))

    def __copy__(self):
        return self.__deepcopy__(None)

    def __iter__(self):
        return DBSchemaIterator(self)            

    def __eq__(self, othSch):
        return (self is othSch) or self.attributeEquality(othSch.__attrNames)

    def __str__(self):
        return str(self.getAttributes())

    def __repr__(self):
        return self.__str__()
