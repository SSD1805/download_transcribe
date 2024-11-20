from threading import Lock
from dependency_injector.wiring import inject, Provide
from src.infrastructure.app_container import AppContainer


class ErrorRegistryException(Exception):
    """Custom exception for error registry issues."""
    pass


class ErrorRegistry:
    """Registry for managing error handlers."""

    _lock = Lock()

    @inject
    def __init__(self, logger=Provide[AppContainer.logger]):
        """
        Initialize the ErrorRegistry.

        Args:
            logger: The logger instance from the AppContainer.
        """
        self._errors = {}
        self._default_handler = None
        self.logger = logger

    def register_error(self, error_type, handler):
        """
        Register an error handler for a specific type of exception.

        Args:
            error_type (type): The exception type to register the handler for.
            handler (callable): The handler function to be called for the exception type.

        Raises:
            ErrorRegistryException: If handler is not a callable.
        """
        if not callable(handler):
            raise ErrorRegistryException("Handler must be a callable.")

        with self._lock:
            self._errors[error_type] = handler
            self.logger.info(f"Handler registered for error type: {error_type.__name__}")

    def set_default_handler(self, handler):
        """
        Set a default error handler to be used when no specific handler is registered.

        Args:
            handler (callable): The default handler function to be called for exceptions.

        Raises:
            ErrorRegistryException: If handler is not a callable.
        """
        if not callable(handler):
            raise ErrorRegistryException("Default handler must be a callable.")

        with self._lock:
            self._default_handler = handler
            self.logger.info("Default error handler registered.")

    def handle_error(self, error, **context):
        """
        Handle an error by calling the appropriate handler.

        Args:
            error (Exception): The error to handle.
            context: Additional context to pass to the handler function.

        Returns:
            Any: The return value from the error handler, if any.

        Raises:
            Exception: If no appropriate handler is registered.
        """
        error_type = type(error)

        with self._lock:
            handler = self._errors.get(error_type)

        if handler:
            self.logger.info(f"Handling {error_type.__name__} with registered handler.")
            return handler(error, **context)

        if self._default_handler:
            self.logger.warning(f"No handler registered for {error_type.__name__}. Using default handler.")
            return self._default_handler(error, **context)

        self.logger.error(f"Unhandled error: {error_type.__name__}. Raising exception.")
        raise error


# Example Usage (if needed)
if __name__ == "__main__":
    from dependency_injector import containers

    # Initialize the AppContainer and wire dependencies for this module
    container = AppContainer()
    container.wire(modules=[__name__])

    # Use the ErrorRegistry instance
    error_registry = container.error_registry()
