from .DBRelation import *


"""
Relational Algebra standard operations
"""
def select(rel, condition):
    n = DBInstance(rel.getDBSchema())
    for t in rel:
        if condition(t) and not n.hasTuple(t):
            n.insert(t.asPythonTupleValues())

    return n




def project(rel, attrNames):
    sch = rel.getDBSchema()

    commonAttrNames = sch.getCommonAttributeNames(attrNames)
    szCommonAttrNames = len(commonAttrNames)

    if not AttributeUtils.attrSameNumber(attrNames, commonAttrNames):
        if szCommonAttrNames == 0:
            raise MissingAttributesException("No attribute has been specified!")
        else:
            missingAttrs = AttributeUtils.attrDiff(attrNames, commonAttrNames)[0]
            raise AttributesNotFoundException("Attributes with names \"%s\" do not exist in this relation!" % (", ".join(missingAttrs),))


    if sch.attributeEquality(attrNames):
        return deepcopy(rel)

    sch = DBSchema(sch.getAttributeRawTypes(attrNames), attrNames)
    n = DBRelation(sch)
    for t in rel:
        vals = t.asPythonTupleValues(attrNames)
        if not n.hasPythonTupleValues(vals):
            n.insert(vals)

    return n




def rename(rel, newAttrs, oldAttrs):
    if len(newAttrs) == len(oldAttrs) == 0:
        raise NotAValidParameterException("Error: no new and old attributes have been specified!")

    if not AttributeUtils.attrSameNumber(newAttrs, oldAttrs):
        raise NotAValidParameterException("Error: number of old and new attributes must match (%d old attributes vs %d new ones)!" % (len(oldAttrs), len(newAttrs),))

    commonAttrNames = AttributeUtils.attrIntersect(newAttrs, oldAttrs)[0]
    if len(commonAttrNames) > 0:
        raise UndefinedOperationException("Error: renaming is defined only over different old and new attributes, but common attributes were found (%s)!" % (", ".join(commonAttrNames),))


    sch = rel.getDBSchema()
    commonAttrNames = sch.getCommonAttributeNames(oldAttrs)

    if not AttributeUtils.attrSameNumber(commonAttrNames, oldAttrs):
        missingAttrs = AttributeUtils.attrDiff(oldAttrs, commonAttrNames)[0]
        raise AttributesNotFoundException("Attributes with names \"%s\" do not exist in this relation!" % (", ".join(missingAttrs),))


    schAttrs = sch.getAttributeNames()
    attrRawTypes = sch.getAttributeRawTypes(schAttrs)
    newSchAttrs = list(schAttrs)

    for currAttr in schAttrs:
        if currAttr in oldAttrs:
            try:
                idxParamAttrName = oldAttrs.index(currAttr)
                idxCurrAttrName = newSchAttrs.index(currAttr)
                newSchAttrs[idxCurrAttrName] = newAttrs[idxParamAttrName]
            except ValueError as ex:
               pass

    r = DBRelation(DBSchema(attrRawTypes, newSchAttrs))
    for t in rel:
        r.insert(t.asPythonTupleValues())

    return r




"""
Set-theory operations
"""
def union(rel1, rel2):
    if not rel1.hasSameSchema(rel2):
        raise UndefinedOperationException("Union is not defined over relations with different schemas!")

    n = deepcopy(rel1)
    for t in rel2:
        if not n.hasTuple(t):
            n.insert(t.asPythonTupleValues())

    return n


def intersect(rel1, rel2):
    if not rel1.hasSameSchema(rel2):
        raise UndefinedOperationException("Intersection is not defined over relations with different schemas!")

    n = DBRelation(rel1.getDBSchema())
    for t in rel1:
        if rel1.hasTuple(t) and rel2.hasTuple(t) and not n.hasTuple(t):
            n.insert(t.asPythonTupleValues())

    for t in rel2:
        if rel1.hasTuple(t) and rel2.hasTuple(t) and not n.hasTuple(t):
            n.insert(t.asPythonTupleValues())

    return n



def difference(rel1, rel2):
    if not rel1.hasSameSchema(rel2):
        raise UndefinedOperationException("Difference is not defined over relations with different schemas!")

    n = DBRelation(rel1.getDBSchema())
    for t in rel1:
        #print(str(t) + ", " + str(rel2.hasTuple(t)))
        if not rel2.hasTuple(t):
            n.insert(t.asPythonTupleValues())

    return n



"""
Relational algebra join operations
"""

# DO NOT USE DIRECTLY, used by the different join operators
def __generic_join(rel1, rel2, leftOuter=False, rightOuter=False):
    sch1 = rel1.getDBSchema()
    sch2 = rel2.getDBSchema()

    commonAttrNames = sch1.getCommonAttributeNamesToSchema(sch2)

    # In caso di nessun attributo comune (len(commonAttrNames) == 0), tutto il fatto degenera in un cross-product.

    commonAttrRawTypes = sch1.getAttributeRawTypes(commonAttrNames)

    attrNames1 = sch1.getAttributeNames()
    attrRawTypes1 = sch1.getAttributeRawTypes()
    attrNames2 = sch2.getAttributeNames()
    attrRawTypes2 = sch2.getAttributeRawTypes()

    attrNames = list(attrNames1)
    attrRawTypes = list(attrRawTypes1)

    # Se non ci sono attributi comuni, questa differenza non fa nulla...
    attrNamesRemainder, attrRawTypesRemainder = AttributeUtils.attrDiff(attrNames2, commonAttrNames, attrRawTypes2, commonAttrRawTypes)
    attrNames.extend(attrNamesRemainder)
    attrRawTypes.extend(attrRawTypesRemainder)

    sch = DBSchema(attrRawTypes, attrNames)
    r = DBRelation(sch)

    for t1 in rel1:
        v1 = t1.getValues(commonAttrNames)
        tupVal1 = t1.asPythonTupleValues()

        leftMatches = False

        for t2 in rel2:
            v2 = t2.getValues(commonAttrNames)

            # In caso di nessun attributo comune, si avrà [] == [], ergo, sempre verificato
            if v1 == v2:
                leftMatches = True # Condizione verificata, la parte di sinistra ha un match non nullo
                tupVal2 = t2.asPythonTupleValues(attrNamesRemainder)
                tupVal = list(tupVal1)
                tupVal.extend(tupVal2)
                if not r.hasPythonTupleValues(tupVal):
                    r.insert(tupVal)
                #r.insert(tupVal)

        if leftOuter and not leftMatches: # Match nullo, se left outer è abilitato, aggiungi
            tupVal2 = len(attrNamesRemainder) * [None,]
            tupVal = list(tupVal1)
            tupVal.extend(tupVal2)
            if not r.hasPythonTupleValues(tupVal):
                r.insert(tupVal)
            #r.insert(tupVal)


    if rightOuter: # Esegui sezione se right outer è abilitato
        for t2 in rel2:
            v2 = t2.getValues(commonAttrNames)
            rightMatches = False

            for t1 in rel1:
                v1 = t1.getValues(commonAttrNames)

                if v1 == v2:
                    rightMatches = True # Condizione verificata, la parte di destra ha un match non nullo
                    break # Interrompi, non è necessario processare altro

            if not rightMatches: # Match nullo, aggiungi
                tupVal = len(attrNames1) * [None,]
                for idx, i in enumerate(commonAttrNames):
                    try:
                        idxAttr1 = attrNames1.index(i)
                        tupVal[idxAttr1] = v2[idx].getRawValue()
                    except ValueError:
                        pass

                tupVal2 = t2.asPythonTupleValues(attrNamesRemainder)
                tupVal.extend(tupVal2)
                #r.insert(tupVal)
                if not r.hasPythonTupleValues(tupVal):
                    r.insert(tupVal)

    return r



"""
Inner joins
"""
def cross_product(rel1, rel2):
    sch1 = rel1.getDBSchema()
    sch2 = rel2.getDBSchema()

    commonAttrNames = sch1.getCommonAttributeNamesToSchema(sch2)
    if len(commonAttrNames) > 0:
        raise UndefinedOperationException("Cross product is not defined over relations with common attributes")

    return __generic_join(rel1, rel2)


cross_join = cross_product


def self_join(rel1, suffix="'"):
    attrNames = rel1.getDBSchema().getAttributeNames()
    rel2 = rename(rel1, tuple(map(lambda x : x + suffix, attrNames)), attrNames)
    return cross_join(rel1, rel2)


def theta_join(rel1, rel2, condition):
    r = cross_product(rel1, rel2)
    return select(r, condition)





"""
Natural joins
"""
def natural_join(rel1, rel2):
    return __generic_join(rel1, rel2)


def left_semijoin(rel1, rel2):
    sch1 = rel1.getDBSchema()
    return project(natural_join(rel1, rel2), sch1.getAttributeNames())


def right_semijoin(rel1, rel2):
    sch2 = rel2.getDBSchema()
    return project(natural_join(rel1, rel2), sch2.getAttributeNames())


def left_antijoin(rel1, rel2):
    lsj = left_semijoin(rel1, rel2)
    return difference(rel1, lsj)


def right_antijoin(rel1, rel2):
    rsj = right_semijoin(rel1, rel2)
    return difference(rel2, rsj)



"""
Outer joins
"""
def left_outerjoin(rel1, rel2):
    return __generic_join(rel1, rel2, True)


def right_outerjoin(rel1, rel2):
    return __generic_join(rel1, rel2, False, True)


def full_outerjoin(rel1, rel2):
    return __generic_join(rel1, rel2, True, True)


"""
Division (?)
"""
def division(rel1, rel2):
    pass
