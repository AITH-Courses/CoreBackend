class ApplicationError(Exception):

    """Base class with http-response fields."""

    def __init__(self, message: str, status: int) -> None:
        """Initialize object.

        :param message: human text about error
        :param status: http status code
        """
        self.message = message
        self.status = status
