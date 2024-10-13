
class FLException(Exception):
    def __init__(self, message: str, status_code=400):
        self.message = message
        self.status_code = status_code
        super(FLException, self).__init__(message)
