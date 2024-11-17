class DownloadError(Exception):
    """Raised when a download operation fails."""
    def __init__(self, message="Download operation failed."):
        super().__init__(message)

class ConfigurationError(Exception):
    """Raised when configuration settings are missing or invalid."""
    def __init__(self, message="Configuration settings are missing or invalid."):
        super().__init__(message)

class FileError(Exception):
    """Raised when there is an issue with file handling."""
    def __init__(self, message="File handling issue encountered."):
        super().__init__(message)
