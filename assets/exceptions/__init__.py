class CommandDisabled(Exception):
    """Thrown if a parameter is missing"""

    def __init__(self, message="This command is disabled!"):
        self.message = message
        super(CommandDisabled, self).__init__(self.message)


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


class InvalidTargetException(Exception):
    """Thrown if the target is invalid"""

    def __init__(self, message="Target is invalid!"):
        self.message = message
        super(InvalidTargetException, self).__init__(self.message)


class RequiredParameterMissingException(Exception):
    """Thrown if a parameter is missing"""

    def __init__(self, message="A required parameter unfilled!"):
        self.message = message
        super(RequiredParameterMissingException, self).__init__(self.message)
