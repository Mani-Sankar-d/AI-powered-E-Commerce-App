# utils/responses.py

from typing import Any

class ApiResponse:
    def __init__(self, status: int, data: Any = None, message: str = ""):
        self.status = status
        self.data = data
        self.message = message
        self.success = status < 400

    def dict(self):
        return {
            "success": self.success,
            "status": self.status,
            "message": self.message,
            "data": self.data,
        }
