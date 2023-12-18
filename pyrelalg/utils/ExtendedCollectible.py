"""
Class useful to extend the notion of list/tuple (based on list though)
"""
from .utils import is_collectible


class ExtendedCollectible(list):
    def __init__(self, inst=[]):
        list.__init__(self, inst)


    def looseEquality(self, othList):
        if not is_collectible(othList):
            return False

        occ1 = ExtendedCollectible.getElementsOccurrences(self)
        occ2 = ExtendedCollectible.getElementsOccurrences(othList)

        return occ1 == occ2


    def isEmpty(self):
        return len(self) == 0


    def isSameSizeOf(self, othLs):
        if not is_collectible(othList):
            return False

        return len(self) == len(othLs)


    def find(self, v):
        occ = []
        for i in range(0, len(self)):
            if self[i] == v:
                occ.append(v)
        return occ



    def union(self, othList): # Add everything
        occ1 = ExtendedCollectible.getElementsOccurrences(self)
        vals1 = occ1.keys()

        occ2 = ExtendedCollectible.getElementsOccurrences(othList)
        vals2 = occ2.keys()

        ls = list(self)

        for i in vals2:
            if i in vals1:
                num = occ2[i] - occ1[i]
                for j in range(0, num):
                    ls.append(i)
            else:
                for j in range(0, occ2[i]):
                    ls.append(i)

        return ls



    def intesect(self, othList): # Get the most common denominator
        occ1 = ExtendedCollectible.getElementsOccurrences(self)
        vals1 = occ1.keys()

        occ2 = ExtendedCollectible.getElementsOccurrences(othList)
        vals2 = occ2.keys()

        ls = []

        for i in vals2:
            if i in vals1:
                num = min(occ1[i], occ2[i])
                for j in range(0, num):
                    ls.append(i)

        return ls


    def diff(self, othList):
        occ1 = ExtendedCollectible.getElementsOccurrences(self)
        vals1 = occ1.keys()

        occ2 = ExtendedCollectible.getElementsOccurrences(othList)
        vals2 = occ2.keys()

        ls = list(self)

        for i in vals2:
            if i in vals1:
                num = min(occ1[i], occ2[i])
                for j in range(0, num):
                    ls.remove(i)

        return ls


    def getDuplicates(self):
        dups = []

        occ = ExtendedCollectible.getElementsOccurrences(self)
        for val in occ.keys():
            if occ[val] > 1:
                dups.append((val, occ[val],))

        return dups


    def removeDuplicates(self):
        dups = self.getDuplicates()
        for occ in dups:
            for val, num in occ:
                for i in range(0, num - 1):
                    self.remove(val)


    def hasDuplicates(self):
        dups = self.getDuplicates()
        return len(dups) > 0


    @staticmethod
    def getElementsOccurrences(ls):
        if not is_collectible(ls):
            return {}

        occ = {}
        for idx, val in enumerate(ls):
            if val in occ.keys():
                occ[val] += 1
            else:
                occ[val] = 1

        return occ