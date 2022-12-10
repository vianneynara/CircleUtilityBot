class InvalidTargetException(Exception):
    """Thrown if the target is invalid"""
    def __init__(self, message="Target is invalid!"):
        self.message = message
        super(InvalidTargetException, self).__init__(self.message)
