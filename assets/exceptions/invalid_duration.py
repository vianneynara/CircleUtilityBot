class InvalidDurationException(Exception):
    """Thrown if the duration is invalid"""
    def __init__(self, message="Duration is invalid!"):
        self.message = message
        super(InvalidDurationException, self).__init__(self.message)
