from src.utils.structlog_logger import StructLogger

logger = StructLogger.get_logger()

class ErrorRegistryException(Exception):
    pass

class ErrorRegistry:
    _errors = {}
    _default_handler = None

    @staticmethod
    def register_error(error_type, handler):
        if not callable(handler):
            raise ErrorRegistryException("Handler must be a callable.")
        ErrorRegistry._errors[error_type] = handler
        logger.info(f"Handler registered for error type: {error_type.__name__}")

    @staticmethod
    def set_default_handler(handler):
        if not callable(handler):
            raise ErrorRegistryException("Default handler must be a callable.")
        ErrorRegistry._default_handler = handler
        logger.info("Default error handler registered.")

    @staticmethod
    def handle_error(error, **context):
        error_type = type(error)
        handler = ErrorRegistry._errors.get(error_type)

        if handler:
            logger.info(f"Handling {error_type.__name__} with registered handler.")
            return handler(error, **context)

        if ErrorRegistry._default_handler:
            logger.warning(f"No handler registered for {error_type.__name__}. Using default handler.")
            return ErrorRegistry._default_handler(error, **context)

        logger.error(f"Unhandled error: {error_type.__name__}. Raising exception.")
        raise error
