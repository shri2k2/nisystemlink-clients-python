from typing import Any, Optional


class ApiException(Exception):
    """Exception for API-related errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        request_info: Optional[Any] = None,
        response: Optional[Any] = None,
    ) -> None:
        """Args:
        message (str): The error message.
        status_code (int, optional): HTTP status code (default: None).
        request_info (dict, optional): Additional error details - in this case the request info (default: None).
        """
        self.message = message
        self.status_code = status_code
        self.request_info = request_info
        self.response = response
        super().__init__(message)

    def __str__(self) -> str:
        """Returns a string representation of the error."""
        return (
            f"{self.status_code}: {self.message}" if self.status_code else self.message
        )
