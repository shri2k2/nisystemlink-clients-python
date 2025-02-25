class UserException(Exception):
    """Exception for general application errors like validation failures or type mismatches."""

    def __init__(self, message: str) -> None:
        """Args:
        message (str): The message to be displayed.
        """
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """Returns a string representation of the error message."""
        return self.message
