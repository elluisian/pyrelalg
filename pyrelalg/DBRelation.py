from .DBSchema import *
from .Tuple import *


class NonExistentTupleException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)



class DBRelationIterator(object):
    def __init__(self, dbInst):
        self.__dbInst = dbInst
        self.__idx = 0
        self.__max = self.__dbInst.getSize()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__idx == self.__max:
            raise StopIteration

        el = self.__dbInst[self.__idx]
        self.__idx += 1
        return el



    

    


class DBRelation(object):
    def __init__(self, dbSchema):
        self.__dbSchema = deepcopy(dbSchema)
        self.__tuples = []
        self.__nTuples = 0


    def insert(self, pythonTupleValues):
        if not isinstance(pythonTupleValues, tuple) and not isinstance(pythonTupleValues, list):
            raise NotAValidParameterException("Error: expected python tuple or list, but got %s!" % (type(pythonTupleValues),))

        pythonTupleValues = tuple(pythonTupleValues)
        attrNames = self.__dbSchema.getAttributeNames()
        attrData = self.__dbSchema.getAttributes(attrNames)

        self.__tuples.append(Tuple(attrData, pythonTupleValues))
        self.__nTuples += 1



    def getTuple(self, key):
        if key not in range(0, self.getSize()):
            raise NonExistentTupleException("Error: only %d tuplas are present in this relation! idx %d requested!" % (self.getSize(), key,))

        return self.__tuples[key]


    def getDBSchema(self):
        return self.__dbSchema


    def getSize(self):
        return self.__nTuples

    def __len__(self):
        return self.getSize()

    def __contains__(self, t):
        return self.hasTuple(t)
    
    def hasSameSchema(self, othRel):
        return self.__dbSchema == othRel.__dbSchema


    def hasTuple(self, t):
        return t in self.__tuples
    

    def hasPythonTupleValues(self, ptv):
        attrNames = self.__dbSchema.getAttributeNames()
        attrData = self.__dbSchema.getAttributes(attrNames)

        t = Tuple(attrData, ptv)
        return self.hasTuple(t)

    
    def __getitem__(self, key):
        return self.getTuple(key)


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
        return DBRelationIterator(self)

    def __deepcopy__(self, memo):
        r = DBRelation(self.getDBSchema())
        for t in self:
            r.insert(t.asPythonTupleValues())
        return r

    def __copy__(self):
        return self.__deepcopy__(None)

    
    """
    String rendition of relation instance
    """
    def __str__(self):
        attrs = self.getDBSchema().getAttributeNames()
        nAttrs = len(attrs)
        
        maxCellTextWidths = []

        #
        # Convert to string both header and single rows
        #
        headerRow = DBRelation.__calculateStringRow(attrs)

        for colName in headerRow:
            maxCellTextWidths.append(len(colName))
        
        rows = []
        currRow = []

        for t in self:
            values = t.asPythonTupleValues()
            currRow = DBRelation.__calculateStringRow(values)
            rows.append(currRow)

            for idx, cell in enumerate(currRow):
                cellSize = len(cell)
                currCellTextWidth = maxCellTextWidths[idx]
                maxCellTextWidths[idx] = cellSize if cellSize > currCellTextWidth else currCellTextWidth


        # Perform all the needed justifications...
        for i in range(0, len(headerRow)):
            currElem = headerRow[i]
            headerRow[i] = DBRelation.__justifyString(currElem, maxCellTextWidths[i])

        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                currElem = rows[i][j]
                rows[i][j] = DBRelation.__justifyString(currElem, maxCellTextWidths[j])


        # Return the final result
        return DBRelation.__getFinalStringTable(headerRow, rows)
        

    def __repr__(self):
        return self.__str__()


    @staticmethod
    def __calculateStringRow(values):
        row = []
        for v in values:
            if v is None:
                vStr = "NULL"
            else:
                vStr = str(v)
    
            vLen = len(vStr)
            row.append(vStr)

        return row


    @staticmethod
    def __justifyString(string, totalSpace):
        return string.ljust(totalSpace)
    

    @staticmethod
    def __getFinalStringTable(headerRow, rows):
        headerStr = "| " + " | ".join(headerRow) + " |"
        lHeaderStr = len(headerStr) - 2
        dashes = "+{minus:-<{lHeaderStr}}+".format(minus="-", lHeaderStr=lHeaderStr)
        finalHeader = dashes + "\n" + headerStr + "\n" + dashes

        finalRows = ""
        for i in rows:
            finalRows += "| " + " | ".join(i) + " |\n"

        return finalHeader + "\n" + finalRows + dashes



DBInstance = DBRelation
