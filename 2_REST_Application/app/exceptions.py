class DuplicateValueError(Exception):
    """
    Raised when there is a duplicate value in a collection.

    Attributes:
        value -- the duplicate value
        collection -- the collection where the duplicate value was found
    """

    pass

    def __init__(self, value, collection):
        self.value = value
        self.collection = collection


class NotExistError(Exception):
    """
    Raised when there is a duplicate value in a collection.

    Attributes:
        value -- the duplicate value
        collection -- the collection where the duplicate value was found
    """

    pass

    def __init__(self, value, collection):
        self.value = value
        self.collection = collection
