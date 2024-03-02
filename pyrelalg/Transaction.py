from pyrelalg.utils.Stack import *
from pyrelalg.Operators import *
from abc import abstractmethod, ABC


class GenericNode(ABC):
    def __init__(self, parent=None):
        self.__parent = parent


class OperationNode(GenericNode):
    def __init__(self, operation, firstChild, otherChildren, furtherParameters, parent=None):
        GenericNode.__init__(self, parent)
        self.operation = operation
        self.firstChild = firstChild
        self.otherChildren = otherChildren
        self.furtherParameters = furtherParameters


    def hasInnerOperations(self):
        if isinstance(self.__firstChild, OperationNode):
            return True

        for i in self.__otherChildren:
            if isinstance(i, OperationNode):
                return True

        return False


    def __str__(self):
        return str(self.operation)



class DBRelationNode(GenericNode):
    def __init__(self, dbRelationInst, parent=None):
        GenericNode.__init__(self, parent)
        self.dbRelationInst = dbRelationInst




class Transaction(object):
    def __init__(self, startingNode):
        self.__currNode = None

        if isinstance(startingNode, Transaction):
            self.__currNode = startingNode.__currNode

        elif isinstance(startingNode, OperationNode) or\
            isinstance(startingNode, DBRelationNode):
            self.__currNode = startingNode

        elif isinstance(startingNode, DBRelation):
            self.__currNode = DBRelationNode(startingNode)


    def select(self, condition):
        return self.__addOperation(select, None, (condition,))

    def project(self, attributeNames):
        return self.__addOperation(project, None, (attributeNames,))

    def rename(self, newAttrs, oldAttrs):
        return self.__addOperation(rename, None, (newAttrs, oldAttrs,))

    def union(self, elem2):
        return self.__addOperation(union, (elem2,))

    def intersect(self, elem2):
        return self.__addOperation(intersect, (elem2,))

    def difference(self, elem2):
        return self.__addOperation(difference, (elem2,))

    def cross_product(self, elem2):
        return self.__addOperation(cross_product, (elem2,))

    def self_join(self, suffix="'"):
        return self.__addOperation(self_join, None, (suffix,))

    def theta_join(self, elem2, condition):
        return self.__addOperation(theta_join, (elem2,), (condition,))

    def natural_join(self, elem2):
        return self.__addOperation(natural_join, (elem2,))

    def left_semijoin(self, elem2):
        return self.__addOperation(left_semijoin, (elem2,))

    def right_semijoin(self, elem2):
        return self.__addOperation(right_semijoin, (elem2,))

    def left_antijoin(self, elem2):
        return self.__addOperation(left_antijoin, (elem2,))

    def right_antijoin(self, elem2):
        return self.__addOperation(right_antijoin, (elem2,))

    def left_outerjoin(self, elem2):
        return self.__addOperation(left_outerjoin, (elem2,))

    def right_outerjoin(self, elem2):
        return self.__addOperation(right_outerjoin, (elem2,))

    def full_outerjoin(self, elem2):
        return self.__addOperation(full_outerjoin, (elem2,))

    def division(self, elem2):
        return self.__addOperation(division, (elem2,))


    def __addOperation(self, operation, otherOperands=None, furtherParameters=None):
        t = OperationNode(operation, self.__currNode, otherOperands, furtherParameters)
        self.__currNode.__parent = t
        self.__currNode = t
        return self




    def resolve(self, steps=0):
        elementsStack = Stack()
        elementsStack.push(self.__currNode)

        operationsStack = Stack()
        #operationsStack.push(self.__currNode)

        while not elementsStack.isEmpty():
            t = elementsStack.top()

            print(t)

            if isinstance(t, OperationNode):
                operationsStack.push(self.__currNode)
                elementsStack.pop()

                print(t.otherChildren)

                nOtherChildren = len(t.otherChildren)
                for i in reversed(range(0, nOtherChildren)):
                    elementsStack.push(t.otherChildren)
                elementsStack.push(t.firstChild)

            elif isinstance(t, DBRelationNode):
                elementsStack.pop()
                elementsStack.push(t.dbRelationInst)

        """
        while not operationsStack.isEmpty():
            t = operationsStack.top()
            if t.__operation in (
        """


    def __repr__(self):
        return "WIP"


    def __str__(self):
        return self.resolve()