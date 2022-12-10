class InvalidDurationException(Exception):
    """Thrown if the duration is invalid"""
    def __init__(self, message="Duration is invalid!"):
        self.message = message
        super(InvalidDurationException, self).__init__(self.message)


class DurationTooLongException(Exception):
    """Thrown if the duration is too long"""
    def __init__(self, message="Duration is too long!"):
        self.message = message
        super(DurationTooLongException, self).__init__(self.message)
