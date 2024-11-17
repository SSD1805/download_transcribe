from src.core.services import CoreServices

# Logger via CoreServices
logger = CoreServices.get_logger()


class ErrorRegistryException(Exception):
    """Custom exception for errors within the ErrorRegistry."""
    pass


class ErrorRegistry:
    """
    Registry to manage and handle errors with dynamically registered handlers.
    """
    _errors = {}
    _default_handler = None

    @staticmethod
    def register_error(error_type, handler):
        """
        Register a handler for a specific error type.

        Args:
            error_type (type): The type of the error (e.g., ValueError).
            handler (callable): A callable to handle the error.
        """
        if not callable(handler):
            raise ErrorRegistryException("Handler must be a callable.")
        ErrorRegistry._errors[error_type] = handler
        logger.info(f"Handler registered for error type: {error_type.__name__}")

    @staticmethod
    def set_default_handler(handler):
        """
        Set a default handler for unregistered errors.

        Args:
            handler (callable): A callable to handle errors not explicitly registered.
        """
        if not callable(handler):
            raise ErrorRegistryException("Default handler must be a callable.")
        ErrorRegistry._default_handler = handler
        logger.info("Default error handler registered.")

    @staticmethod
    def handle_error(error, **context):
        """
        Handle an error using its registered handler.

        Args:
            error (Exception): The error instance to handle.
            **context: Additional arguments for the handler.

        Returns:
            Any: The result of the error handler.

        Raises:
            Exception: If no handler is registered and no default handler is set.
        """
        error_type = type(error)
        handler = ErrorRegistry._errors.get(error_type)

        if handler:
            logger.info(f"Handling {error_type.__name__} with registered handler.")
            return handler(error, **context)

        if ErrorRegistry._default_handler:
            logger.warning(
                f"No handler registered for {error_type.__name__}. Using default handler."
            )
            return ErrorRegistry._default_handler(error, **context)

        logger.error(f"Unhandled error: {error_type.__name__}. Raising exception.")
        raise error


# Custom Exceptions
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


# Error Handlers
def handle_download_error(error, **context):
    logger.error(f"DownloadError handled: {error}")
    return f"Download issue: {error}"


def handle_configuration_error(error, **context):
    logger.error(f"ConfigurationError handled: {error}")
    return f"Configuration issue: {error}"


def handle_file_error(error, **context):
    logger.error(f"FileError handled: {error}")
    return f"File handling issue: {error}"


def default_error_handler(error, **context):
    logger.error(f"Default handler used for error: {error}")
    return f"An unexpected error occurred: {error}"


# Register Custom Exceptions and Default Handler in the Registry
ErrorRegistry.register_error(DownloadError, handle_download_error)
ErrorRegistry.register_error(ConfigurationError, handle_configuration_error)
ErrorRegistry.register_error(FileError, handle_file_error)
ErrorRegistry.set_default_handler(default_error_handler)
