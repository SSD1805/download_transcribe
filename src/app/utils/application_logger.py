# src/app/utils/application_logger.py
import logging
import sys
import threading
import structlog


class ApplicationLogger:
    """
    Singleton Logger using structlog.
    """

    _instance = None
    _lock = threading.Lock()
    _is_configured = False
    _logger = None

    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:  # Double-checked locking
                    cls._instance = super(ApplicationLogger, cls).__new__(cls)
        return cls._instance

    @classmethod
    def configure(cls, log_level="INFO"):
        """
        Configures the structlog logger for the application.
        """
        if cls._is_configured:
            return  # Prevent reconfiguration
        cls._is_configured = True

        # Configure structlog
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="ISO"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.dev.ConsoleRenderer(),  # Console renderer
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Configure stdlib logger to integrate with structlog
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=log_level,
        )

        cls._logger = structlog.get_logger()

    @staticmethod
    def get_logger():
        """
        Returns the singleton logger instance.
        """
        if ApplicationLogger._logger is None:
            raise RuntimeError(
                "Logger is not configured. Call `ApplicationLogger.configure()` first."
            )
        return ApplicationLogger._logger


# Convenience functions for direct use throughout the application
def log_info(message):
    """
    Logs an informational message using the singleton logger instance.
    """
    logger = ApplicationLogger.get_logger()
    logger.info(message)


def log_error(message):
    """
    Logs an error message using the singleton logger instance.
    """
    logger = ApplicationLogger.get_logger()
    logger.error(message)


def log_warning(message):
    """
    Logs a warning message using the singleton logger instance.
    """
    logger = ApplicationLogger.get_logger()
    logger.warning(message)
