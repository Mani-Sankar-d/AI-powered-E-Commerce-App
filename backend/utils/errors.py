# errors.py
class ApiError(Exception):
    def __init__(self, status_code: int, message="Something went wrong", errors=None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.success = False
        self.errors = errors or []
