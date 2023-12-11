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
