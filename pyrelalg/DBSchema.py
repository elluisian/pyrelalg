from .Attribute import *


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
    def __init__(self, attrData1, attrData2=None):
        self.__attrNamesOrder = ()
        self.__attrData = {}
        self.__nAttrs = 0
        self.__extractParameters(attrData1, attrData2)


    def __extractParameters(self, attrData1, attrData2):
        attrDataStats = {}

        for i in range(0, 2):
            currAttrData = attrData1 if i == 0 else attrData2
            d = {
                "is_attr_or_type_coll": is_attr_or_type_coll(currAttrData),
                "is_attr_or_type_dict": is_attr_or_type_dict(currAttrData),
                "is_attribute": is_attribute(currAttrData),
                "is_attribute_coll": is_attribute_coll(currAttrData),
                "is_type": is_type(currAttrData),
                "is_type_coll": is_type_coll(currAttrData),
                "is_attr_or_str_coll": is_attr_or_str_coll(currAttrData),
                "is_attr_or_str_dict": is_attr_or_str_dict(currAttrData),
                "is_none": currAttrData is None
            }

            # Establish if the order tuple/list is NOT needed, for the schema to be correctly created
            d["order_not_needed"] = d["is_attr_or_type_dict"] or\
                d["is_attribute"] or\
                d["is_attribute_coll"]

            # Establish if the order tuple/list IS ACTUALLY needed, for the schema to be correctly created
            d["order_needed"] = d["is_attr_or_type_coll"] or\
                d["is_type_coll"] or d["is_type"]

            # Finally, establish if the current tuple/list is data or (d["is_data"] = True) or it's just the order of the attributes (d["is_data"] = False)
            d["is_data"] = d["order_not_needed"] or d["order_needed"]

            # Finally, establish if the current tuple/list is a list/tuple of ordered attribute names (d["is_order"] = True) or it's just the data (d["is_order"] = False)
            d["is_order"] = d["is_attr_or_str_coll"] or d["is_attr_or_str_dict"]

            attrDataStats[i] = d


        validParameterModes = (
            ("is_data", "is_order",),
            ("order_not_needed", "is_none",),
        )
        parameterModeFound = -1

        attrData = None
        attrOrder = None
        dataStats = None
        nameStats = None

        for idx, i in enumerate(validParameterModes):
            mode1, mode2 = i
            if attrDataStats[0][mode1] and attrDataStats[1][mode2]:
                attrData = attrData1
                attrOrder = attrData2
                dataStats = attrDataStats[0]
                nameStats = attrDataStats[1]
                parameterModeFound = idx
                break

            elif attrDataStats[0][mode2] and attrDataStats[1][mode1]:
                attrData = attrData2
                attrOrder = attrData1
                dataStats = attrDataStats[1]
                nameStats = attrDataStats[0]
                parameterModeFound = idx
                break


        if parameterModeFound == -1:
            raise WIPException("WIP #45")

        attrDataNames = None

        if dataStats["is_attr_or_type_dict"]:
            attrDataNames = tuple(attrData.keys())

        elif dataStats["is_attribute_coll"]:
            attrDataNames = get_attribute_names(attrData)

        elif dataStats["is_attribute"]:
            attrDataNames = tuple(attrData.getName(),)
            attrData = tuple(attrData)

        elif dataStats["is_type"] or dataStats["is_type_coll"] or dataStats["is_attr_or_type_coll"]:
            attrDataNames = tuple(attrOrder)
            attrData = tuple(attrData)

        attrOrder = ExtendedCollectible(attrDataNames if nameStats["is_none"] else attrOrder)

        if not attrOrder.looseEquality(attrDataNames):
            raise WIPException("WIP #2")

        self.__attrNamesOrder = attrOrder
        for idx, cur in enumerate(attrData):
            if dataStats["is_attr_or_type_dict"]:
                name = cur
                rawType = attrData[cur]
                if is_attribute(rawType):
                    rawType = rawType.getRawType()

            elif dataStats["is_attr_or_type_coll"] or dataStats["is_attribute"] or dataStats["is_type"]:
                if is_attribute(cur):
                    name = cur.getName()
                    rawType = cur.getRawType()
                else:
                    name = attrOrder[idx]
                    rawType = cur

            self.__attrData[name] = Attribute(name, rawType, self)
            self.__nAttrs += 1



    def getAttributeNames(self):
        return tuple(self.__attrNamesOrder)


    def getAttributes(self, attrNames=None):
        if attrNames is None:
            attrNames = self.__attrNamesOrder

        elif is_string(attrNames):
            attrNames = (attrNames,)

        elif not is_string_coll(attrNames):
            raise WIPException("WIP Exception #3")

        attrL = []
        for i in attrNames:
            attrL.append(self.__attrData[i])

        return attrL


    def getAttributeRawTypes(self, attrNames=None):
        attrInsts = self.getAttributes(attrNames)

        attrL = []
        for i in attrInsts:
            attrL.append(i.getRawType())

        return attrL


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
        rawTypes = self.getAttributeRawTypes()
        return DBSchema(rawTypes, self.__attrNamesOrder)

    def __copy__(self):
        return self.__deepcopy__(None)

    def __iter__(self):
        return DBSchemaIterator(self)

    def __eq__(self, othSch):
        return (self is othSch) or self.attributeEquality(othSch.__attrNamesOrder)

    def __str__(self):
        return str(self.getAttributes())

    def __repr__(self):
        return self.__str__()
