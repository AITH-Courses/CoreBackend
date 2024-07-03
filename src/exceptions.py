class ApplicationException(Exception):
    def __init__(self, message: str, status: int):
        self.message = message
        self.status = status
