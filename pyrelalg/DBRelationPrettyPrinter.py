from .utils.utils import justify_multiple, is_null

class DBRelationPrettyPrinter(object):
    def __init__(self, dbInst):
        self.__dbInst = dbInst

    def prettyPrint(self):
        header = []
        rows = []
        cellTextWidths = []

        # Get attribute information (Schema)
        for idx, attr in enumerate(self.__dbInst.getDBSchema()):
            currTextWidth = 0
            cellTextWidths.append(currTextWidth)

            name = attr.getName()
            sName = len(name)
            currTextWidth = sName if sName > currTextWidth else currTextWidth
            cellTextWidths[idx] = currTextWidth
            header.append(name)

        # Get tuple information
        for tup in self.__dbInst:
            currRow = []
            for idx, col in enumerate(tup):
                currTextWidth = cellTextWidths[idx]

                v = "NULL" if is_null(col) else str(col)
                vSize = len(v)
                currTextWidth = vSize if vSize > currTextWidth else currTextWidth
                cellTextWidths[idx] = currTextWidth
                currRow.append(v)
            rows.append(currRow)

        # Put it all together
        justify_multiple(header, cellTextWidths)

        headerText = "| %s |" % (" | ".join(header),)
        lenHeaderText = len(headerText)
        headerSeparatorText = "+%s+" % ("=" * (lenHeaderText - 2),)
        bottomSeparatorText = "+%s+" % ("-" * (lenHeaderText - 2),)

        totalText = ["%s\n%s\n%s" % (headerSeparatorText, headerText, headerSeparatorText,),]

        for i in range(0, len(rows)):
            justify_multiple(rows[i], cellTextWidths)
            totalText.append("| %s |" % (" | ".join(rows[i]),))

        totalText.append(bottomSeparatorText)

        return "\n".join(totalText)