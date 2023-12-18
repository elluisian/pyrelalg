class CustomException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class UndefinedOperationException(Exception):
    def __init__(self, message):
        CustomException.__init__(self, message)


class NotAValidParameterException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class TupleCreationException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class AttributeRawTypeMismatchException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class AttributeRawTypeIntegrityCheckException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class AttributesNotFoundException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class MissingAttributesException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class NonExistentTupleException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)


class WIPException(CustomException):
    def __init__(self, message):
        CustomException.__init__(self, message)