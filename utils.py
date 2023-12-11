from copy import deepcopy, copy


NULL = None
INTEGER = int
STRING = str
BOOLEAN = bool
FLOAT = float



class CustomException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class UndefinedOperationException(Exception):
    def __init__(self, message):
        CustomException.__init__(self, message)

        
class NotAValidParameterException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)

